#!/usr/bin/env python3
"""Extract focused view files from Workato recipe JSON exports.

Strips ~90-98% of UI/schema bloat and produces 6 focused view files:
  summary.json  — recipe metadata, trigger, stats, connections
  skeleton.md   — one-line-per-block control flow tree
  mappings.md   — field→value mappings per action block
  conditions.md — if/elsif/while/catch conditions
  variables.md  — variable declarations and updates
  errors.md     — try/catch pairs and stop blocks

Usage:
  uv run python extract_views.py path/to/recipe.json
  uv run python extract_views.py --all [--include-archived]
  uv run python extract_views.py --force path/to/recipe.json
"""

import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

EXTRACTOR_VERSION = "1"

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
    as_id: str
    comment: str
    skip: bool
    input: dict
    source: Any  # foreach source (block-level)
    filter: Any  # catch filter (block-level)
    repeat_mode: str  # foreach
    batch_size: str  # foreach
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
        for child in root.get("block", []):
            if child is not None:
                self._walk_block(child, depth=1)
        return self.blocks

    def _process_trigger(self, root: dict) -> None:
        as_id = root.get("as", "")
        number = root.get("number", 0)
        provider = root.get("provider", "")
        name = root.get("name", "")

        # Clean input
        raw_input = root.get("input", {})
        cleaned = self._clean_input(raw_input) if isinstance(raw_input, dict) else {}

        info = BlockInfo(
            number=number,
            keyword="trigger",
            provider=provider,
            name=name,
            depth=0,
            as_id=as_id,
            comment="",
            skip=False,
            input=cleaned,
            source=None,
            filter=None,
            repeat_mode="",
            batch_size="",
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

    def _walk_block(self, block: dict, depth: int) -> None:
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
        repeat_mode = block.get("repeat_mode", "")
        batch_size = str(block.get("batch_size", ""))

        # Block-level filter for catch
        block_filter = block.get("filter")

        info = BlockInfo(
            number=number,
            keyword=keyword,
            provider=provider,
            name=name,
            depth=depth,
            as_id=as_id,
            comment=comment,
            skip=skip,
            input=cleaned,
            source=source,
            filter=block_filter,
            repeat_mode=repeat_mode,
            batch_size=batch_size,
        )
        self.renderer.register_block(info)
        self.blocks.append(info)

        # Recurse into children (pre-order: parent before children)
        children = block.get("block", [])
        child_numbers = []
        for child in children:
            if child is not None:
                child_numbers.append(child.get("number", -1))
                self._walk_block(child, depth + 1)
        info.child_numbers = child_numbers

    def _clean_input(self, inp: dict) -> dict:
        return {k: v for k, v in inp.items() if k not in INPUT_BLOAT_KEYS}


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

    # Scan for project property references
    raw_text = json.dumps(recipe.get("code", {}))
    for m in re.finditer(r'"pill_type"\s*:\s*"project_property"\s*,\s*"property_name"\s*:\s*"([^"]+)"', raw_text):
        project_props.add(m.group(1))

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
    summary["connections"] = connections
    summary["statistics"] = {
        "total_blocks": len(blocks),
        "max_depth": max_depth,
        "by_keyword": dict(sorted(keyword_counts.items())),
        "by_provider": dict(sorted(provider_counts.items())),
    }
    if project_props:
        summary["project_properties"] = sorted(project_props)
    if callable_params:
        summary["callable"] = callable_params

    return summary


def generate_skeleton(blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    """Generate skeleton.md — one line per block with indentation."""
    lines = []
    for b in blocks:
        indent = "  " * b.depth
        kw_upper = b.keyword.upper()

        parts = [f"{indent}{b.number}: {kw_upper}"]

        if b.keyword == "trigger":
            parts.append(f"{b.provider}.{b.name}")
        elif b.keyword == "action" and b.provider:
            parts.append(f"{b.provider}.{b.name}")
        elif b.keyword in ("if", "elsif"):
            cond_str = _format_condition_inline(b.input, renderer)
            if cond_str:
                parts.append(cond_str)
        elif b.keyword == "foreach":
            src = renderer.render(b.source) if b.source else "?"
            mode_info = f"repeat_mode={b.repeat_mode}"
            if b.batch_size:
                mode_info += f" batch_size={b.batch_size}"
            parts.append(f"{src} ({mode_info})")
        elif b.keyword == "catch":
            catch_info = []
            retry = b.input.get("max_retry_count")
            interval = b.input.get("retry_interval")
            if retry and str(retry) != "0":
                catch_info.append(f"retry: {retry}x @ {interval}s")
            if catch_info:
                parts.append(" ".join(catch_info))
        elif b.keyword == "stop":
            err = b.input.get("stop_with_error", "false")
            if err == "true":
                parts.append("[error]")
            else:
                parts.append("[success]")

        line = " ".join(parts)

        # Suffix: skip, comment
        suffixes = []
        if b.skip:
            suffixes.append("[SKIPPED]")
        if b.comment:
            comment_display = b.comment if len(b.comment) <= 80 else b.comment[:77] + "..."
            suffixes.append(f'— "{comment_display}"')
        if b.keyword == "stop":
            reason = b.input.get("stop_reason", "")
            if reason:
                reason = renderer.render(reason)
                reason_display = reason if len(reason) <= 80 else reason[:77] + "..."
                suffixes.append(f'— "{reason_display}"')

        if suffixes:
            line += "  " + "  ".join(suffixes)

        lines.append(line)

    return "\n".join(lines) + "\n"


def _format_condition_inline(inp: dict, renderer: DatapillRenderer, max_len: int = 120) -> str:
    """Format if/elsif condition inline for skeleton."""
    conditions = inp.get("conditions", [])
    operand = inp.get("operand", "and").upper()

    parts = []
    for cond in conditions:
        lhs = renderer.render(cond.get("lhs", ""))
        op = cond.get("operand", "?")
        rhs = cond.get("rhs", "")
        if rhs:
            rhs = renderer.render(rhs)
            parts.append(f"{lhs} {op.upper()} {rhs}")
        else:
            parts.append(f"{lhs} {op.upper()}")

    result = f" {operand} ".join(parts)
    if len(result) > max_len:
        result = result[:max_len - 3] + "..."
    return result


def generate_mappings(blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    """Generate mappings.md — field→value mappings per action block."""
    sections = []

    for b in blocks:
        if b.keyword == "trigger":
            # Show trigger inputs if interesting
            if b.input and b.provider == "workato_recipe_function":
                continue  # Callable params shown in summary
            if b.input:
                key_inputs = {k: v for k, v in b.input.items() if isinstance(v, str) and v.strip()}
                if key_inputs:
                    lines = [f"## Block {b.number}: TRIGGER {b.provider}.{b.name}\n"]
                    for k, v in key_inputs.items():
                        rendered = renderer.render(v)
                        if "\n" in rendered or len(rendered) > 100:
                            lines.append(f"**{k}:**\n```\n{rendered}\n```\n")
                        else:
                            lines.append(f"- **{k}:** `{rendered}`")
                    sections.append("\n".join(lines))
            continue

        if b.keyword != "action" or not b.input:
            continue

        # Variable declarations
        if b.name == "declare_variable":
            lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
            variables = b.input.get("variables", {})
            if isinstance(variables, dict):
                schema_json = variables.get("schema", "")
                data = variables.get("data", {})
                if isinstance(schema_json, str) and schema_json:
                    try:
                        schema = json.loads(schema_json)
                        lines.append("| Variable | Type | Initial Value |")
                        lines.append("|----------|------|---------------|")
                        for var_def in schema:
                            vname = var_def.get("name", "?")
                            vtype = var_def.get("type", "string")
                            val = data.get(vname, "") if isinstance(data, dict) else ""
                            if val:
                                val = renderer.render(str(val))
                            lines.append(f"| {vname} | {vtype} | {_truncate(val, 80)} |")
                    except json.JSONDecodeError:
                        lines.append(f"Schema (raw): `{schema_json[:200]}`")
            sections.append("\n".join(lines))
            continue

        # Declare list
        if b.name == "declare_list":
            lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
            list_name = b.input.get("name", "")
            if list_name:
                lines.append(f"**Name:** {list_name}\n")
            list_items = b.input.get("list_items", {})
            if isinstance(list_items, dict):
                source = list_items.get("____source", "")
                if source:
                    lines.append(f"**Source:** `{renderer.render(source)}`\n")
                field_mappings = {k: v for k, v in list_items.items() if k != "____source"}
                if field_mappings:
                    for k, v in field_mappings.items():
                        rendered = renderer.render(str(v))
                        lines.append(f"- **{k}:** `{_truncate(rendered, 120)}`")
            sections.append("\n".join(lines))
            continue

        # Update variables
        if b.name == "update_variables":
            lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
            # Parse the name field: {uuid}:{as_id}:{field_name}
            var_name_raw = b.input.get("name", "")
            parts_split = var_name_raw.split(":")
            var_field = parts_split[-1] if parts_split else var_name_raw

            for k, v in b.input.items():
                if k == "name":
                    continue
                rendered = renderer.render(str(v))
                lines.append(f"- **{k}:** `{_truncate(rendered, 120)}`")
            if var_field and var_field != var_name_raw:
                lines.insert(1, f"**Target variable:** {var_field}\n")
            sections.append("\n".join(lines))
            continue

        # Insert to list batch
        if b.name == "insert_to_list_batch":
            lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
            for k, v in b.input.items():
                rendered = renderer.render(str(v))
                lines.append(f"- **{k}:** `{_truncate(rendered, 120)}`")
            sections.append("\n".join(lines))
            continue

        # Recipe calls
        if b.name == "call_recipe":
            lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
            flow_id = b.input.get("flow_id")
            if isinstance(flow_id, dict):
                lines.append(f"**Recipe:** {flow_id.get('name', flow_id.get('zip_name', '?'))}")
                lines.append(f"**Folder:** {flow_id.get('folder', '?')}\n")
            elif flow_id:
                lines.append(f"**Flow ID:** {flow_id}\n")
            params = b.input.get("parameters", {})
            if isinstance(params, dict):
                for k, v in params.items():
                    rendered = renderer.render(str(v))
                    lines.append(f"- **{k}:** `{_truncate(rendered, 120)}`")
            sections.append("\n".join(lines))
            continue

        # Generic action with non-empty input
        interesting = {k: v for k, v in b.input.items()
                       if v is not None and v != "" and v != {} and v != []}
        if not interesting:
            continue

        lines = [f"## Block {b.number}: {b.provider}.{b.name}\n"]
        for k, v in interesting.items():
            if isinstance(v, dict):
                rendered_dict = _render_dict_values(v, renderer)
                if rendered_dict:
                    lines.append(f"**{k}:**")
                    for dk, dv in rendered_dict.items():
                        lines.append(f"- {dk}: `{_truncate(dv, 120)}`")
                    lines.append("")
            elif isinstance(v, str):
                rendered = renderer.render(v)
                if "\n" in rendered or len(rendered) > 100:
                    lines.append(f"**{k}:**\n```\n{rendered}\n```\n")
                else:
                    lines.append(f"- **{k}:** `{rendered}`")
            elif isinstance(v, list):
                rendered = renderer.render(json.dumps(v, separators=(",", ":")))
                lines.append(f"- **{k}:** `{_truncate(rendered, 120)}`")
            else:
                lines.append(f"- **{k}:** `{v}`")

        sections.append("\n".join(lines))

    return "# Mappings\n\n" + "\n\n---\n\n".join(sections) + "\n" if sections else "# Mappings\n\nNo mappings found.\n"


def generate_conditions(blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    """Generate conditions.md — detailed condition breakdown."""
    sections = []

    for b in blocks:
        if b.keyword in ("if", "elsif", "while_condition"):
            conditions = b.input.get("conditions", [])
            operand = b.input.get("operand", "and").upper()

            lines = [f"## Block {b.number}: {b.keyword.upper()}\n"]
            lines.append(f"**Compound operator:** {operand}\n")

            for i, cond in enumerate(conditions, 1):
                lhs = renderer.render(cond.get("lhs", ""))
                op = cond.get("operand", "?").upper()
                rhs = cond.get("rhs", "")
                if rhs:
                    rhs = renderer.render(rhs)
                    lines.append(f"{i}. `{lhs}` **{op}** `{rhs}`")
                else:
                    lines.append(f"{i}. `{lhs}` **{op}**")

            # Show first child
            if b.child_numbers:
                first_child = b.child_numbers[0]
                child_block = next((bl for bl in blocks if bl.number == first_child), None)
                if child_block:
                    lines.append(f"\n→ First child: block {child_block.number} ({child_block.keyword}"
                                 + (f" {child_block.provider}.{child_block.name}" if child_block.provider else "")
                                 + ")")
            else:
                lines.append("\n→ [empty branch]")

            sections.append("\n".join(lines))

        elif b.keyword == "catch" and b.filter:
            filt = b.filter
            conditions = filt.get("conditions", [])
            operand = filt.get("operand", "and").upper()

            lines = [f"## Block {b.number}: CATCH (with filter)\n"]
            lines.append(f"**Compound operator:** {operand}\n")

            for i, cond in enumerate(conditions, 1):
                lhs = renderer.render(cond.get("lhs", ""))
                op = cond.get("operand", "?").upper()
                rhs = cond.get("rhs", "")
                if rhs:
                    rhs = renderer.render(rhs)
                    lines.append(f"{i}. `{lhs}` **{op}** `{rhs}`")
                else:
                    lines.append(f"{i}. `{lhs}` **{op}**")

            sections.append("\n".join(lines))

    return "# Conditions\n\n" + "\n\n---\n\n".join(sections) + "\n" if sections else "# Conditions\n\nNo conditions found.\n"


def generate_variables(blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    """Generate variables.md — declarations and updates."""
    declarations: list[str] = []
    updates: dict[str, list[str]] = {}  # var_name → list of update descriptions

    for b in blocks:
        if b.keyword != "action":
            continue

        if b.name == "declare_variable":
            variables = b.input.get("variables", {})
            if isinstance(variables, dict):
                schema_json = variables.get("schema", "")
                data = variables.get("data", {})
                if isinstance(schema_json, str) and schema_json:
                    try:
                        schema = json.loads(schema_json)
                        for var_def in schema:
                            vname = var_def.get("name", "?")
                            vtype = var_def.get("type", "string")
                            val = data.get(vname, "") if isinstance(data, dict) else ""
                            if val:
                                val = renderer.render(str(val))
                            declarations.append(f"| {vname} | {vtype} | {_truncate(val, 60)} | block {b.number} |")
                    except json.JSONDecodeError:
                        pass

        elif b.name == "declare_list":
            list_name = b.input.get("name", "?")
            source = b.input.get("list_items", {})
            src_dp = ""
            if isinstance(source, dict):
                src_dp = renderer.render(source.get("____source", ""))
            declarations.append(f"| {list_name} (list) | list | {_truncate(src_dp, 60)} | block {b.number} |")

        elif b.name == "update_variables":
            var_name_raw = b.input.get("name", "")
            parts_split = var_name_raw.split(":")
            var_field = parts_split[-1] if parts_split else var_name_raw

            # Find the actual value being set
            values = {k: v for k, v in b.input.items() if k != "name"}
            val_strs = []
            for k, v in values.items():
                rendered = renderer.render(str(v))
                val_strs.append(f"{k} = {_truncate(rendered, 80)}")

            desc = f"block {b.number}: " + "; ".join(val_strs) if val_strs else f"block {b.number}"
            updates.setdefault(var_field, []).append(desc)

        elif b.name == "insert_to_list" or b.name == "insert_to_list_batch":
            list_name_raw = b.input.get("name", b.input.get("list_name", ""))
            parts_split = list_name_raw.split(":")
            list_field = parts_split[-1] if len(parts_split) > 1 else list_name_raw

            desc = f"block {b.number}: {b.name}"
            updates.setdefault(list_field, []).append(desc)

    lines = ["# Variables\n"]

    if declarations:
        lines.append("## Declarations\n")
        lines.append("| Name | Type | Initial Value | Block |")
        lines.append("|------|------|---------------|-------|")
        lines.extend(declarations)
        lines.append("")

    if updates:
        lines.append("## Updates\n")
        for var_name, update_list in sorted(updates.items()):
            lines.append(f"### {var_name}\n")
            for u in update_list:
                lines.append(f"- {u}")
            lines.append("")

    if not declarations and not updates:
        lines.append("No variables found.\n")

    return "\n".join(lines) + "\n"


def generate_errors(blocks: list[BlockInfo], renderer: DatapillRenderer) -> str:
    """Generate errors.md — try/catch pairs and stop blocks."""
    sections = []

    # Build try→catch mapping
    # Try blocks and their corresponding catch blocks are siblings
    # We need to find catch blocks that follow try blocks at the same depth
    try_catch_pairs: list[tuple[BlockInfo, BlockInfo | None]] = []

    # Group blocks by their parent (using depth/sequence)
    block_by_number = {b.number: b for b in blocks}

    # Find try blocks and match with following catch
    for b in blocks:
        if b.keyword == "try":
            # Find the catch that follows this try at the same depth
            # Look for a catch in the same parent's children
            parent = _find_parent(blocks, b.number)
            if parent:
                siblings = parent.child_numbers
                try_idx = siblings.index(b.number) if b.number in siblings else -1
                if try_idx >= 0 and try_idx + 1 < len(siblings):
                    next_num = siblings[try_idx + 1]
                    next_block = block_by_number.get(next_num)
                    if next_block and next_block.keyword == "catch":
                        try_catch_pairs.append((b, next_block))
                        continue
            try_catch_pairs.append((b, None))

    if try_catch_pairs:
        for try_block, catch_block in try_catch_pairs:
            lines = [f"## Try block {try_block.number}"]
            if catch_block:
                lines[0] += f" / Catch block {catch_block.number}\n"

                # Retry settings
                retry = catch_block.input.get("max_retry_count", "0")
                interval = catch_block.input.get("retry_interval", "")
                if retry and str(retry) != "0":
                    lines.append(f"**Retry:** {retry}x @ {interval}s\n")
                else:
                    lines.append("**Retry:** none\n")

                # Filter
                if catch_block.filter:
                    filt = catch_block.filter
                    conditions = filt.get("conditions", [])
                    operand = filt.get("operand", "and").upper()
                    lines.append(f"**Filter ({operand}):**")
                    for cond in conditions:
                        lhs = renderer.render(cond.get("lhs", ""))
                        op = cond.get("operand", "?").upper()
                        rhs = cond.get("rhs", "")
                        if rhs:
                            rhs = renderer.render(rhs)
                            lines.append(f"- `{lhs}` {op} `{rhs}`")
                        else:
                            lines.append(f"- `{lhs}` {op}")
                    lines.append("")

                # Catch children
                if catch_block.child_numbers:
                    lines.append(f"**Catch actions:** blocks {', '.join(str(n) for n in catch_block.child_numbers)}")
                else:
                    lines.append("**Catch actions:** [empty — error suppressed]")
            else:
                lines.append("\n**Catch:** not found (orphaned try)\n")

            sections.append("\n".join(lines))

    # Stop blocks
    stop_blocks = [b for b in blocks if b.keyword == "stop"]
    if stop_blocks:
        for b in stop_blocks:
            err = b.input.get("stop_with_error", "false")
            status = "ERROR" if err == "true" else "SUCCESS"
            reason = b.input.get("stop_reason", "")
            if reason:
                reason = renderer.render(reason)

            lines = [f"## Stop block {b.number} [{status}]\n"]
            if reason:
                lines.append(f"**Reason:** {reason}\n")
            sections.append("\n".join(lines))

    return "# Error Handling\n\n" + "\n\n---\n\n".join(sections) + "\n" if sections else "# Error Handling\n\nNo error handling found.\n"


def _find_parent(blocks: list[BlockInfo], child_number: int) -> BlockInfo | None:
    """Find the parent block that contains child_number in its child_numbers."""
    for b in blocks:
        if child_number in b.child_numbers:
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
    skeleton = generate_skeleton(blocks, renderer)
    mappings = generate_mappings(blocks, renderer)
    conditions = generate_conditions(blocks, renderer)
    variables = generate_variables(blocks, renderer)
    errors = generate_errors(blocks, renderer)

    # Write output
    views_dir.mkdir(parents=True, exist_ok=True)

    with open(views_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(views_dir / "skeleton.md", "w") as f:
        f.write(skeleton)

    with open(views_dir / "mappings.md", "w") as f:
        f.write(mappings)

    with open(views_dir / "conditions.md", "w") as f:
        f.write(conditions)

    with open(views_dir / "variables.md", "w") as f:
        f.write(variables)

    with open(views_dir / "errors.md", "w") as f:
        f.write(errors)

    write_meta(views_dir, recipe_path)

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


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    project_root = Path.cwd()
    force = "--force" in args
    include_archived = "--include-archived" in args
    all_mode = "--all" in args

    # Strip flags
    positional = [a for a in args if not a.startswith("--")]

    if all_mode:
        recipes = discover_recipes(project_root, include_archived)
        print(f"Found {len(recipes)} recipes", file=sys.stderr)
        errors = []
        for recipe_path in recipes:
            try:
                views_dir = extract_views(recipe_path, project_root, force)
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
    elif positional:
        recipe_path = Path(positional[0])
        if not recipe_path.exists():
            print(f"ERROR: File not found: {recipe_path}", file=sys.stderr)
            sys.exit(1)
        views_dir = extract_views(recipe_path, project_root, force)
        print(views_dir)
    else:
        print("ERROR: Provide a recipe path or --all", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
