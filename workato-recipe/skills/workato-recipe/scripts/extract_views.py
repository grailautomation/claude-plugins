#!/usr/bin/env python3
"""Extract focused view files from Workato recipe JSON exports.

Strips ~90-98% of UI/schema bloat and produces focused view files:
  summary.json      — recipe metadata, trigger, stats, connections
  unified_logic.md  — complete top-down control flow, queries, conditions, and mutations

Usage:
  uv run python extract_views.py path/to/recipe.json
  uv run python extract_views.py --recipe path/to/recipe.json
  uv run python extract_views.py --all [--include-archived]
  uv run python extract_views.py --force path/to/recipe.json
"""

import argparse
import json
import re
import sys
import shutil
import uuid
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

EXTRACTOR_VERSION = "10"

# Keys to strip from block nodes (peers of 'input')
BLOCK_BLOAT_KEYS = {
    "toggleCfg",
    "dynamicPickListSelection",
    "visible_config_fields",
    "hidden_config_fields",
    "job_report_schema",
    "extended_output_schema",
    "extended_input_schema",
}

# Keys to strip from input dicts
INPUT_BLOAT_KEYS = {
    "extended_input_schema",
    "extended_output_schema",
    "list_item_schema_json",
    "parameters_schema_json",
    "result_schema_json",
    "output_schema",
}

# Known child block keywords
KNOWN_KEYWORDS = {
    "action", "if", "elsif", "else", "try", "catch",
    "stop", "foreach", "repeat", "while_condition",
}

DATAPILL_RE = re.compile(r"""_dp\('(\{[^']*\})'\)""")


# ---------------------------------------------------------------------------
# DatapillRenderer
# ---------------------------------------------------------------------------
class DatapillRenderer:
    """Resolves _dp() datapill JSON into human-readable references."""

    def __init__(self) -> None:
        # as_id (hex) → BlockInfo
        self._block_lookup: dict[str, "BlockInfo"] = {}

    def register_block(self, block_info: "BlockInfo") -> None:
        if block_info.as_id:
            self._block_lookup[block_info.as_id] = block_info

    def render(self, text: str) -> str:
        """Replace all _dp() calls in text with rendered references."""
        if not text or "_dp(" not in str(text):
            return text if isinstance(text, str) else json.dumps(text)

        text = str(text)

        def replace_pill(match: re.Match) -> str:
            raw_json = match.group(1)
            try:
                pill = json.loads(raw_json)
            except json.JSONDecodeError:
                return f"[?:parse_error]"
            return self._render_pill(pill)

        # Strip #{...} interpolation wrapper
        result = text
        # Handle formula mode: =_dp(...) — don't strip the = prefix
        # Handle interpolation mode: #{_dp(...)} — strip #{ and }
        result = re.sub(r'#\{(_dp\([^)]*\))\}', r'\1', result)

        # Replace all _dp() calls
        result = DATAPILL_RE.sub(replace_pill, result)

        return result

    def _render_pill(self, pill: dict) -> str:
        pill_type = pill.get("pill_type", "unknown")
        if pill_type == "output":
            return self._render_output_pill(pill)
        elif pill_type == "project_property":
            name = pill.get("property_name", "?")
            return f"[project:{name}]"
        elif pill_type == "job_context":
            path_parts = self._render_path(pill.get("path", []))
            return f"[job:{path_parts}]"
        elif pill_type == "account_property":
            name = pill.get("property_name", pill.get("name", "?"))
            return f"[account:{name}]"
        elif pill_type == "foreach_meta":
            line = pill.get("line", "")
            key = pill.get("key", "?")
            block = self._block_lookup.get(line)
            if block:
                return f"[foreach_{block.number}:{key}]"
            return f"[foreach_?:{key}]"
        else:
            summary = json.dumps(pill, separators=(",", ":"))
            if len(summary) > 80:
                summary = summary[:77] + "..."
            return f"[{pill_type}:{summary}]"

    def _render_output_pill(self, pill: dict) -> str:
        provider = pill.get("provider", "?")
        line = pill.get("line", "")
        path_parts = self._render_path(pill.get("path", []))

        block = self._block_lookup.get(line)
        if block:
            return f"[block_{block.number}:{provider}.{path_parts}]"
        return f"[?:{provider}.{path_parts}]"

    def _render_path(self, path: list) -> str:
        parts = []
        for elem in path:
            if isinstance(elem, dict):
                if elem.get("path_element_type") == "current_item":
                    parts.append("[*]")
                else:
                    parts.append(str(elem))
            else:
                parts.append(str(elem))
        return ".".join(parts)


# ---------------------------------------------------------------------------
# BlockInfo
# ---------------------------------------------------------------------------
@dataclass
class BlockInfo:
    number: int
    keyword: str
    provider: str
    name: str
    depth: int
    parent_number: int | None
    as_id: str
    comment: str
    skip: bool
    input: dict
    source: Any  # foreach source (block-level)
    filter: Any  # catch filter (block-level)
    repeat_mode: str  # foreach
    batch_size: str  # foreach
    clear_scope: str  # foreach/repeat
    child_numbers: list[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# BlockWalker
# ---------------------------------------------------------------------------
class BlockWalker:
    """Single-pass recursive walk producing flat list[BlockInfo]."""

    def __init__(self, renderer: DatapillRenderer) -> None:
        self.renderer = renderer
        self.blocks: list[BlockInfo] = []
        self.trigger_info: dict | None = None

    def walk(self, root: dict) -> list[BlockInfo]:
        # Root is the trigger block
        self._process_trigger(root)
        children = root.get("block", [])
        child_numbers = []
        for child in children:
            if child is not None:
                child_numbers.append(child.get("number", -1))
                self._walk_block(child, depth=1, parent_number=self.blocks[0].number)
        # Populate trigger's child_numbers so _find_parent() can find it
        if self.blocks:
            self.blocks[0].child_numbers = child_numbers
        return self.blocks

    def _process_trigger(self, root: dict) -> None:
        as_id = root.get("as", "")
        number = root.get("number", 0)
        provider = root.get("provider", "")
        name = root.get("name", "")

        # Clean input
        raw_input = root.get("input", {})
        cleaned = self._clean_input(raw_input) if isinstance(raw_input, dict) else {}

        # Block-level filter for trigger (same pattern as catch filter in _walk_block)
        trigger_filter = root.get("filter")

        info = BlockInfo(
            number=number,
            keyword="trigger",
            provider=provider,
            name=name,
            depth=0,
            parent_number=None,
            as_id=as_id,
            comment="",
            skip=False,
            input=cleaned,
            source=None,
            filter=trigger_filter,
            repeat_mode="",
            batch_size="",
            clear_scope="",
        )
        self.renderer.register_block(info)
        self.blocks.append(info)

        # Extract trigger info for summary
        self.trigger_info = {
            "provider": provider,
            "action": name,
            "key_inputs": {},
        }
        # Capture interesting trigger inputs (SQL queries, schemas, etc.)
        for k, v in cleaned.items():
            if isinstance(v, str) and len(v) > 0:
                self.trigger_info["key_inputs"][k] = v

        # Render trigger filter conditions into trigger_info for summary.json
        if trigger_filter and isinstance(trigger_filter, dict):
            conditions = trigger_filter.get("conditions", [])
            operand = trigger_filter.get("operand", "and")
            rendered_conditions = []
            for cond in conditions:
                lhs = self.renderer.render(cond.get("lhs", ""))
                op = cond.get("operand", "?").upper()
                rhs = cond.get("rhs", "")
                entry: dict[str, str] = {"lhs": lhs, "op": op}
                if rhs:
                    entry["rhs"] = self.renderer.render(rhs)
                rendered_conditions.append(entry)
            self.trigger_info["filter"] = {
                "operand": operand,
                "conditions": rendered_conditions,
            }

    def _walk_block(self, block: dict, depth: int, parent_number: int) -> None:
        number = block.get("number", -1)
        keyword = block.get("keyword", "unknown")
        provider = block.get("provider", "")
        name = block.get("name", "")
        as_id = block.get("as", "")
        comment = block.get("comment", "")
        skip = bool(block.get("skip", False))

        if keyword not in KNOWN_KEYWORDS and keyword != "trigger":
            print(f"WARNING: Unknown block keyword '{keyword}' at block {number}", file=sys.stderr)

        # Clean input
        raw_input = block.get("input", {})
        cleaned = self._clean_input(raw_input) if isinstance(raw_input, dict) else {}

        # Block-level fields for foreach
        source = block.get("source")
        repeat_mode = str(block.get("repeat_mode", ""))
        batch_size = str(block.get("batch_size", ""))
        clear_scope = str(block.get("clear_scope", ""))

        # Block-level filter for catch
        block_filter = block.get("filter")

        info = BlockInfo(
            number=number,
            keyword=keyword,
            provider=provider,
            name=name,
            depth=depth,
            parent_number=parent_number,
            as_id=as_id,
            comment=comment,
            skip=skip,
            input=cleaned,
            source=source,
            filter=block_filter,
            repeat_mode=repeat_mode,
            batch_size=batch_size,
            clear_scope=clear_scope,
        )
        self.renderer.register_block(info)
        self.blocks.append(info)

        # Recurse into children (pre-order: parent before children)
        children = block.get("block", [])
        child_numbers = []
        for child in children:
            if child is not None:
                child_numbers.append(child.get("number", -1))
                self._walk_block(child, depth + 1, parent_number=number)
        info.child_numbers = child_numbers

    def _clean_input(self, inp: dict) -> dict:
        return {k: v for k, v in inp.items() if k not in INPUT_BLOAT_KEYS}


def _collect_project_props(obj: Any, props: set[str]) -> None:
    """Recursively walk all values to find project_property datapill references."""
    if isinstance(obj, dict):
        if obj.get("pill_type") == "project_property":
            name = obj.get("property_name")
            if name:
                props.add(name)
        for v in obj.values():
            _collect_project_props(v, props)
    elif isinstance(obj, list):
        for item in obj:
            _collect_project_props(item, props)
    elif isinstance(obj, str) and "project_property" in obj:
        # Handle serialized JSON inside strings (e.g., datapill references)
        for m in re.finditer(r'"property_name"\s*:\s*"([^"]+)"', obj):
            props.add(m.group(1))


# This duplication is intentional: these helpers must stay behaviorally aligned
# with normalize_optional_string() and normalize_optional_serialized_string() in
# scripts/fidelity_projection.py.
def _normalize_optional_string(value: Any) -> str | None:
    # _walk_block() defaults absent loop metadata fields to "", but the fidelity
    # contract canonicalizes both "" and None to JSON null.
    if value in (None, ""):
        return None
    return str(value)


def _normalize_optional_serialized_string(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


# ---------------------------------------------------------------------------
# View generators
# ---------------------------------------------------------------------------
def generate_summary(recipe: dict, blocks: list[BlockInfo], trigger_info: dict) -> dict:
    """Generate summary.json content."""
    # Count statistics
    keyword_counts: dict[str, int] = {}
    provider_counts: dict[str, int] = {}
    max_depth = 0
    project_props: set[str] = set()

    for b in blocks:
        keyword_counts[b.keyword] = keyword_counts.get(b.keyword, 0) + 1
        if b.provider:
            provider_counts[b.provider] = provider_counts.get(b.provider, 0) + 1
        if b.depth > max_depth:
            max_depth = b.depth

    # Scan for project property references by walking all string values
    _collect_project_props(recipe.get("code", {}), project_props)

    # Connections from config
    connections = []
    for cfg in recipe.get("config", []):
        prov = cfg.get("provider", "")
        if prov:
            conn_info: dict[str, Any] = {"provider": prov}
            acc = cfg.get("account_id")
            if isinstance(acc, dict):
                conn_info["connection"] = acc.get("name", "")
            connections.append(conn_info)

    # Callable recipe params
    callable_params = None
    if trigger_info.get("provider") == "workato_recipe_function":
        params_json = recipe.get("code", {}).get("input", {}).get("parameters_schema_json", "")
        result_json = recipe.get("code", {}).get("input", {}).get("result_schema_json", "")
        callable_params = {}
        if params_json:
            try:
                params = json.loads(params_json)
                callable_params["parameters"] = [
                    {"name": p.get("name", ""), "type": p.get("type", ""), "label": p.get("label", "")}
                    for p in params
                ]
            except json.JSONDecodeError:
                callable_params["parameters_raw"] = params_json
        if result_json:
            try:
                results = json.loads(result_json)
                callable_params["results"] = [
                    {"name": r.get("name", ""), "type": r.get("type", ""), "label": r.get("label", "")}
                    for r in results
                ]
            except json.JSONDecodeError:
                callable_params["results_raw"] = result_json

    summary: dict[str, Any] = {
        "name": recipe.get("name", ""),
        "version": recipe.get("version"),
    }
    vc = recipe.get("version_comment")
    if vc:
        summary["version_comment"] = vc

    summary["trigger"] = trigger_info
    concurrency = recipe.get("concurrency")
    if concurrency is not None:
        summary["concurrency"] = concurrency
    summary["connections"] = connections
    summary["statistics"] = {
        "total_blocks": len(blocks),
        "max_depth": max_depth,
        "by_keyword": dict(sorted(keyword_counts.items())),
        "by_provider": dict(sorted(provider_counts.items())),
    }
    summary["control_flow"] = {
        "blocks": build_control_flow_summary(blocks),
    }
    summary["loop_handling"] = build_loop_handling_summary(blocks)
    summary["error_handling"] = build_error_handling_summary(blocks)
    if project_props:
        summary["project_properties"] = sorted(project_props)
    if callable_params:
        summary["callable"] = callable_params

    return summary


def build_control_flow_summary(blocks: list[BlockInfo]) -> list[dict[str, Any]]:
    return [
        {
            "number": b.number,
            "keyword": b.keyword,
            "provider": b.provider,
            "name": b.name,
            "depth": b.depth,
            "parent_number": b.parent_number,
            "child_numbers": list(b.child_numbers),
            "skip": b.skip,
        }
        for b in blocks
    ]


def build_loop_handling_summary(blocks: list[BlockInfo]) -> dict[str, Any]:
    block_by_number = {block.number: block for block in blocks}
    loop_blocks: list[dict[str, Any]] = []

    for block in blocks:
        if block.keyword not in {"foreach", "repeat"}:
            continue

        while_conditions: list[dict[str, Any]] = []
        body_block_numbers: list[int] = []
        for child_number in block.child_numbers:
            child = block_by_number.get(child_number)
            if child is None:
                continue
            if child.keyword == "while_condition":
                while_conditions.append(
                    {
                        "number": child.number,
                        "filter": _normalize_filter(child.input),
                    }
                )
                continue
            body_block_numbers.append(child.number)

        loop_blocks.append(
            {
                "number": block.number,
                "keyword": block.keyword,
                "skip": block.skip,
                "source_raw": _normalize_optional_serialized_string(block.source),
                "repeat_mode": _normalize_optional_string(block.repeat_mode),
                "batch_size": _normalize_optional_string(block.batch_size),
                "clear_scope": _normalize_optional_string(block.clear_scope),
                "while_conditions": while_conditions,
                "body_block_numbers": body_block_numbers,
            }
        )

    return {
        "loop_blocks": loop_blocks,
    }


def _parse_retry_count(value: Any) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return 0


def _parse_retry_interval_seconds(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _normalize_filter(filter_data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not filter_data:
        return None
    return {
        "operator": str(filter_data.get("operator", filter_data.get("operand", "and"))).upper(),
        "conditions": [
            {
                "lhs": "" if cond.get("lhs") is None else str(cond.get("lhs", "")),
                "op": str(cond.get("op", cond.get("operand", ""))).upper(),
                "rhs": None if "rhs" not in cond or cond.get("rhs") is None else str(cond.get("rhs")),
            }
            for cond in filter_data.get("conditions", [])
        ],
    }


def _build_try_catch_pairs(blocks: list[BlockInfo]) -> list[tuple[BlockInfo, BlockInfo | None]]:
    block_by_number = {b.number: b for b in blocks}
    pairs: list[tuple[BlockInfo, BlockInfo | None]] = []
    for block in blocks:
        if block.keyword != "try":
            continue

        child_catch = next(
            (
                block_by_number[child_number]
                for child_number in block.child_numbers
                if child_number in block_by_number and block_by_number[child_number].keyword == "catch"
            ),
            None,
        )
        if child_catch is not None:
            pairs.append((block, child_catch))
            continue

        sibling_catch: BlockInfo | None = None
        if block.parent_number is not None:
            parent = block_by_number.get(block.parent_number)
            if parent is not None:
                siblings = parent.child_numbers
                try_index = siblings.index(block.number) if block.number in siblings else -1
                if 0 <= try_index + 1 < len(siblings):
                    next_block = block_by_number.get(siblings[try_index + 1])
                    if next_block is not None and next_block.keyword == "catch":
                        sibling_catch = next_block
        pairs.append((block, sibling_catch))
    return pairs


def build_error_handling_summary(blocks: list[BlockInfo]) -> dict[str, Any]:
    return {
        "try_catch_pairs": [
            {
                "try_block": try_block.number,
                "catch_block": catch_block.number if catch_block is not None else None,
                "retry_count": _parse_retry_count(catch_block.input.get("max_retry_count")) if catch_block else 0,
                "retry_interval_seconds": (
                    _parse_retry_interval_seconds(catch_block.input.get("retry_interval")) if catch_block else None
                ),
                "filter": _normalize_filter(catch_block.filter) if catch_block else None,
                "catch_action_numbers": list(catch_block.child_numbers) if catch_block else [],
            }
            for try_block, catch_block in _build_try_catch_pairs(blocks)
        ],
        "stop_blocks": [
            {
                "number": b.number,
                "stop_with_error": str(b.input.get("stop_with_error", "false")).lower() == "true",
                "stop_reason_raw": None if b.input.get("stop_reason") is None else str(b.input.get("stop_reason")),
                "skip": b.skip,
            }
            for b in blocks
            if b.keyword == "stop"
        ],
    }


def indent_text(text: str, level: int) -> str:
    if not text:
        return ""
    indent = "  " * level
    lines = str(text).splitlines()
    if not lines:
        return ""
    if len(lines) == 1:
        return f"{indent}{lines[0]}"
    return "\n".join(f"{indent}{line}" for line in lines)


def _get_branch_annotations(block: BlockInfo, blocks: list[BlockInfo]) -> list[str]:
    annotations = []
    block_by_number = {bl.number: bl for bl in blocks}
    
    if block.child_numbers:
        true_nums = [n for n in block.child_numbers
                     if block_by_number.get(n) and block_by_number[n].keyword not in ("elsif", "else")]
        else_nums = [n for n in block.child_numbers
                     if block_by_number.get(n) and block_by_number[n].keyword in ("elsif", "else")]
        if true_nums:
            annotations.append(f"-> True branch blocks: {', '.join(str(n) for n in true_nums)}")
        if else_nums:
            annotations.append(f"-> Else/ELSIF branch blocks: {', '.join(str(n) for n in else_nums)}")
    else:
        else_nums = []

    parent = _find_parent(blocks, block.number) if block.keyword in ("if", "elsif") else None
    if parent:
        siblings = parent.child_numbers
        my_idx = siblings.index(block.number) if block.number in siblings else -1
        if my_idx >= 0:
            for sib_num in siblings[my_idx + 1:]:
                sib = block_by_number.get(sib_num)
                if sib and sib.keyword in ("elsif", "else"):
                    if sib_num not in else_nums:
                        else_nums.append(sib_num)
                elif sib and sib.keyword == "catch":
                    continue
                else:
                    break
                    
    if not else_nums and parent:
        siblings = parent.child_numbers
        my_idx = siblings.index(block.number) if block.number in siblings else -1
        if my_idx >= 0:
            for sib_num in siblings[my_idx + 1:]:
                sib = block_by_number.get(sib_num)
                if sib and sib.keyword in ("elsif", "else", "catch"):
                    continue
                annotations.append(f"-> Fallthrough next block: {sib_num}")
                break
                
    return annotations


def _format_conditions(filt: dict, renderer: DatapillRenderer) -> list[str]:
    if not filt:
        return []
    conditions = filt.get("conditions", [])
    operand = filt.get("operand", "and").upper()
    lines = [f"[{operand}]:"]
    for i, cond in enumerate(conditions, 1):
        lhs = renderer.render(cond.get("lhs", ""))
        op = cond.get("operand", "?").upper()
        rhs = cond.get("rhs", "")
        if rhs:
            rhs = renderer.render(rhs)
            lines.append(f"  {i}. `{lhs}` **{op}** `{rhs}`")
        else:
            lines.append(f"  {i}. `{lhs}` **{op}**")
    return lines


def generate_unified_logic(recipe: dict, blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    lines = ["# Unified Logic\n"]
    lines.append("Block 0 (TRIGGER) is the root at depth 0. The explicit [depth=... parent=...] metadata is authoritative.\n")
    
    for b in blocks:
        indent_level = b.depth
        kw_upper = b.keyword.upper()
        
        header_parts = []
        if b.skip:
            header_parts.append("[SKIPPED]")
        
        header_parts.append(f"{b.number}: {kw_upper}")
        
        if b.keyword == "trigger":
            header_parts.append(f"{b.provider}.{b.name}")
        elif b.keyword == "action" and b.provider:
            header_parts.append(f"{b.provider}.{b.name}")
            
        parent = _find_parent(blocks, b.number)
        parent_label = f"block_{parent.number}" if parent else "root"
        header_parts.append(f"[depth={b.depth} parent={parent_label}]")
        
        lines.append(indent_text(" ".join(header_parts), indent_level))
        
        if b.comment:
            lines.append(indent_text(f"// {b.comment}", indent_level + 1))
            
        if b.keyword == "trigger":
            if b.filter:
                cond_lines = _format_conditions(b.filter, renderer)
                for line in cond_lines:
                    lines.append(indent_text(line, indent_level + 1))
            if b.input and b.provider != "workato_recipe_function":
                key_inputs = {k: v for k, v in b.input.items() if isinstance(v, str) and v.strip()}
                if key_inputs:
                    lines.append(indent_text("[Inputs]:", indent_level + 1))
                    for k, v in key_inputs.items():
                        rendered = renderer.render(v)
                        if "\n" in rendered or len(rendered) > 100:
                            lines.append(indent_text(f"- **{k}**:", indent_level + 1))
                            lines.append(indent_text("```\n" + rendered + "\n```", indent_level + 2))
                        else:
                            lines.append(indent_text(f"- **{k}**: `{rendered}`", indent_level + 1))
            continue
            
        if b.keyword in ("if", "elsif", "while_condition"):
            if b.input.get("conditions"):
                cond_lines = _format_conditions(b.input, renderer)
                for line in cond_lines:
                    lines.append(indent_text(line, indent_level + 1))
            annotations = _get_branch_annotations(b, blocks)
            for ann in annotations:
                lines.append(indent_text(ann, indent_level + 1))
            continue
            
        if b.keyword == "catch":
            retry = b.input.get("max_retry_count")
            interval = b.input.get("retry_interval")
            if retry and str(retry) != "0":
                lines.append(indent_text(f"Retry: {retry}x @ {interval}s", indent_level + 1))
            else:
                interval_str = f" (interval={interval}s)" if interval else ""
                lines.append(indent_text(f"Retry: none{interval_str}", indent_level + 1))
                
            if b.filter:
                cond_lines = _format_conditions(b.filter, renderer)
                for line in cond_lines:
                    lines.append(indent_text(line, indent_level + 1))
            
            if not b.child_numbers:
                lines.append(indent_text("[Empty Catch Body — error caught, recipe continues]", indent_level + 1))
            continue
            
        if b.keyword == "stop":
            err = b.input.get("stop_with_error", "false")
            status = "ERROR" if err == "true" else "SUCCESS"
            reason = b.input.get("stop_reason", "")
            lines.append(indent_text(f"[Status: {status}]", indent_level + 1))
            if reason:
                rendered = renderer.render(reason)
                lines.append(indent_text(f"[Reason]: {rendered}", indent_level + 1))
            continue
            
        if b.keyword == "foreach":
            src = renderer.render(b.source) if b.source else "?"
            lines.append(indent_text(f"Source: `{src}`", indent_level + 1))
            lines.append(indent_text(f"Repeat Mode: {b.repeat_mode}", indent_level + 1))
            if b.batch_size:
                lines.append(indent_text(f"Batch Size: {b.batch_size}", indent_level + 1))
            continue
            
        if b.keyword == "repeat":
            if b.repeat_mode:
                lines.append(indent_text(f"Repeat Mode: {b.repeat_mode}", indent_level + 1))
            if b.batch_size:
                lines.append(indent_text(f"Batch Size: {b.batch_size}", indent_level + 1))
            continue
            
        if b.keyword == "action":
            if b.name == "declare_variable":
                variables = b.input.get("variables", {})
                if isinstance(variables, dict):
                    data = variables.get("data", {})
                    if data:
                        lines.append(indent_text("-> DECLARES:", indent_level + 1))
                        for k, v in data.items():
                            val = renderer.render(str(v)) if v else ""
                            lines.append(indent_text(f"- {k} = `{_truncate(val, 80)}`", indent_level + 2))
                continue
                
            if b.name == "update_variables":
                var_name_raw = b.input.get("name", "")
                parts_split = var_name_raw.split(":")
                var_field = parts_split[-1] if parts_split else var_name_raw
                values = {k: v for k, v in b.input.items() if k != "name"}
                if values:
                    target = var_field if var_field else "variables"
                    lines.append(indent_text(f"-> MUTATES [{target}]:", indent_level + 1))
                    for k, v in values.items():
                        rendered = renderer.render(str(v))
                        lines.append(indent_text(f"- {k} = `{_truncate(rendered, 120)}`", indent_level + 2))
                continue
                
            if b.name == "declare_list":
                list_name = b.input.get("name", "?")
                lines.append(indent_text(f"-> DECLARES LIST [{list_name}]:", indent_level + 1))
                list_items = b.input.get("list_items", {})
                if isinstance(list_items, dict):
                    source = list_items.get("____source", "")
                    if source:
                        lines.append(indent_text(f"Source: `{renderer.render(source)}`", indent_level + 2))
                    field_mappings = {k: v for k, v in list_items.items() if k != "____source"}
                    if field_mappings:
                        for k, v in field_mappings.items():
                            rendered = renderer.render(str(v))
                            lines.append(indent_text(f"- {k}: `{_truncate(rendered, 120)}`", indent_level + 2))
                continue
                
            if b.name in ("insert_to_list", "insert_to_list_batch"):
                list_name_raw = b.input.get("name", b.input.get("list_name", ""))
                parts_split = list_name_raw.split(":")
                list_field = parts_split[-1] if len(parts_split) > 1 else list_name_raw
                lines.append(indent_text(f"-> MUTATES LIST [{list_field}]:", indent_level + 1))
                for k, v in b.input.items():
                    if k in ("name", "list_name"): continue
                    rendered = renderer.render(str(v))
                    lines.append(indent_text(f"- {k}: `{_truncate(rendered, 120)}`", indent_level + 2))
                continue
                
            if b.name == "call_recipe":
                flow_id = b.input.get("flow_id")
                if isinstance(flow_id, dict):
                    lines.append(indent_text(f"Recipe: {flow_id.get('name', flow_id.get('zip_name', '?'))}", indent_level + 1))
                    lines.append(indent_text(f"Folder: {flow_id.get('folder', '?')}", indent_level + 1))
                elif flow_id:
                    lines.append(indent_text(f"Flow ID: {flow_id}", indent_level + 1))
                params = b.input.get("parameters", {})
                if isinstance(params, dict) and params:
                    lines.append(indent_text("[Parameters]:", indent_level + 1))
                    for k, v in params.items():
                        rendered = renderer.render(str(v))
                        lines.append(indent_text(f"- {k}: `{_truncate(rendered, 120)}`", indent_level + 2))
                continue
                
            interesting = {k: v for k, v in b.input.items()
                           if v is not None and v != "" and v != {} and v != []}
            if interesting:
                lines.append(indent_text("[Inputs]:", indent_level + 1))
                for k, v in interesting.items():
                    if isinstance(v, dict):
                        rendered_dict = _render_dict_values(v, renderer)
                        if rendered_dict:
                            lines.append(indent_text(f"- **{k}**:", indent_level + 2))
                            for dk, dv in rendered_dict.items():
                                lines.append(indent_text(f"- {dk}: `{_truncate(dv, 120)}`", indent_level + 3))
                    elif isinstance(v, str):
                        rendered = renderer.render(v)
                        if "\n" in rendered or len(rendered) > 100:
                            lines.append(indent_text(f"- **{k}**:", indent_level + 2))
                            lines.append(indent_text("```\n" + rendered + "\n```", indent_level + 3))
                        else:
                            lines.append(indent_text(f"- **{k}**: `{rendered}`", indent_level + 2))
                    elif isinstance(v, list):
                        rendered = renderer.render(json.dumps(v, separators=(",", ":")))
                        truncated = _truncate(rendered, 120)
                        if len(rendered) > 120:
                            truncated += f" [{len(rendered)} chars total]"
                        lines.append(indent_text(f"- **{k}**: `{truncated}`", indent_level + 2))
                    else:
                        lines.append(indent_text(f"- **{k}**: `{v}`", indent_level + 2))

    return "\n".join(lines) + "\n"


def _find_parent(blocks: list[BlockInfo], child_number: int) -> BlockInfo | None:
    """Find the parent block that contains child_number in its child_numbers."""
    child = next((b for b in blocks if b.number == child_number), None)
    if child is None or child.parent_number is None:
        return None
    for b in blocks:
        if b.number == child.parent_number:
            return b
    return None


def _render_dict_values(d: dict, renderer: DatapillRenderer) -> dict[str, str]:
    """Render all string values in a dict through the datapill renderer."""
    result = {}
    for k, v in d.items():
        if isinstance(v, str):
            result[k] = renderer.render(v)
        elif isinstance(v, dict):
            # Flatten nested dicts
            for nk, nv in v.items():
                if isinstance(nv, str):
                    result[f"{k}.{nk}"] = renderer.render(nv)
                else:
                    result[f"{k}.{nk}"] = str(nv)[:120]
        else:
            result[k] = str(v)[:120]
    return result


def _truncate(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len - 3] + "..."
    return s


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------
def get_views_dir(recipe_path: Path, project_root: Path) -> Path:
    """Compute the .scratch/workato-views/ output directory for a recipe."""
    try:
        rel = recipe_path.resolve().relative_to(project_root.resolve())
    except ValueError:
        rel = Path(recipe_path.name)

    # Mirror the directory structure, use recipe stem as .views/ dir name
    parent_parts = rel.parent
    stem = recipe_path.name
    if stem.endswith(".recipe.json"):
        stem = stem[: -len(".recipe.json")]
    elif stem.endswith(".json"):
        stem = stem[: -len(".json")]

    return project_root / ".scratch" / "workato-views" / parent_parts / f"{stem}.recipe.views"


def is_cache_valid(views_dir: Path, recipe_path: Path) -> bool:
    """Check if cached views are still valid."""
    meta_path = views_dir / ".meta.json"
    if not meta_path.exists():
        return False

    try:
        with open(meta_path) as f:
            meta = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False

    # Check extractor version
    if meta.get("extractor_version") != EXTRACTOR_VERSION:
        return False

    # Check source mtime
    source_mtime = recipe_path.stat().st_mtime
    if meta.get("source_mtime") != source_mtime:
        return False

    return True


def write_meta(views_dir: Path, recipe_path: Path) -> None:
    """Write cache metadata."""
    meta = {
        "extractor_version": EXTRACTOR_VERSION,
        "source_mtime": recipe_path.stat().st_mtime,
        "source_path": str(recipe_path),
    }
    with open(views_dir / ".meta.json", "w") as f:
        json.dump(meta, f, indent=2)


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------
def extract_views(recipe_path: Path, project_root: Path, force: bool = False) -> Path:
    """Extract views from a recipe JSON file. Returns views directory path."""
    recipe_path = recipe_path.resolve()
    views_dir = get_views_dir(recipe_path, project_root)

    if not force and is_cache_valid(views_dir, recipe_path):
        print(f"CACHED: {views_dir}", file=sys.stderr)
        return views_dir

    # Load recipe
    with open(recipe_path) as f:
        recipe = json.load(f)

    # Initialize renderer and walker
    renderer = DatapillRenderer()
    walker = BlockWalker(renderer)

    # Walk the block tree
    root = recipe.get("code", {})
    blocks = walker.walk(root)
    trigger_info = walker.trigger_info or {"provider": "?", "action": "?", "key_inputs": {}}

    # Generate views
    summary = generate_summary(recipe, blocks, trigger_info)
    unified_logic = generate_unified_logic(recipe, blocks, renderer)

    # Safe Atomic Write
    temp_dir = views_dir.with_name(f"{views_dir.name}.tmp.{uuid.uuid4().hex[:8]}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(temp_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        with open(temp_dir / "unified_logic.md", "w") as f:
            f.write(unified_logic)
        write_meta(temp_dir, recipe_path)

        # Safely swap with rollback
        if views_dir.exists():
            old_dir = views_dir.with_name(f"{views_dir.name}.old.{uuid.uuid4().hex[:8]}")
            views_dir.rename(old_dir)
            try:
                temp_dir.rename(views_dir)
            except Exception:
                # Rollback: restore the original views_dir if the temp rename fails
                old_dir.rename(views_dir)
                raise
            shutil.rmtree(old_dir, ignore_errors=True)
        else:
            temp_dir.rename(views_dir)
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    print(f"EXTRACTED: {views_dir}", file=sys.stderr)
    return views_dir


def is_archived(path: Path) -> bool:
    """Check if a recipe path is in an archive directory."""
    for part in path.parts:
        lower = part.lower()
        if "archive" in lower:
            return True
    return False


def discover_recipes(project_root: Path, include_archived: bool = False) -> list[Path]:
    """Find all .recipe.json files under global-context/sources/workato/."""
    workato_dir = project_root / "global-context" / "sources" / "workato"
    if not workato_dir.exists():
        print(f"ERROR: Workato directory not found: {workato_dir}", file=sys.stderr)
        return []

    recipes = sorted(workato_dir.rglob("*.recipe.json"))

    if not include_archived:
        recipes = [r for r in recipes if not is_archived(r)]

    return recipes


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract focused view files from Workato recipe JSON exports."
    )
    parser.add_argument(
        "recipe_path",
        nargs="?",
        help="Path to a .recipe.json export",
    )
    parser.add_argument(
        "--recipe",
        dest="recipe_flag",
        help="Path to a .recipe.json export",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all recipes under global-context/sources/workato",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived recipes when used with --all",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract even if cached views are current",
    )

    args = parser.parse_args(argv)

    if args.recipe_flag and args.recipe_path:
        parser.error("Use either a positional recipe path or --recipe, not both.")
    if args.include_archived and not args.all:
        parser.error("--include-archived requires --all.")
    if not args.all and not (args.recipe_flag or args.recipe_path):
        parser.error("Provide a recipe path or --all.")

    return args


def main() -> None:
    args = parse_args(sys.argv[1:])
    project_root = Path.cwd()
    if args.all:
        recipes = discover_recipes(project_root, args.include_archived)
        print(f"Found {len(recipes)} recipes", file=sys.stderr)
        errors = []
        for recipe_path in recipes:
            try:
                views_dir = extract_views(recipe_path, project_root, args.force)
                print(views_dir)
            except Exception as e:
                errors.append((recipe_path, e))
                print(f"ERROR: {recipe_path}: {e}", file=sys.stderr)
        if errors:
            print(f"\n{len(errors)} errors:", file=sys.stderr)
            for p, e in errors:
                print(f"  {p.name}: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"\nProcessed {len(recipes) - len(errors)}/{len(recipes)} recipes", file=sys.stderr)
    else:
        recipe_path = Path(args.recipe_flag or args.recipe_path)
        if not recipe_path.exists():
            print(f"ERROR: File not found: {recipe_path}", file=sys.stderr)
            sys.exit(1)
        views_dir = extract_views(recipe_path, project_root, args.force)
        print(views_dir)


if __name__ == "__main__":
    main()
