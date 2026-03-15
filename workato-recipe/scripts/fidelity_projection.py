from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

INPUT_BLOAT_KEYS = {
    "extended_input_schema",
    "extended_output_schema",
    "list_item_schema_json",
    "parameters_schema_json",
    "result_schema_json",
    "output_schema",
}


class ProjectionError(Exception):
    def __init__(self, errors: str | list[str]) -> None:
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("; ".join(self.errors))


def load_schema_validator(schema_file: Path) -> Draft202012Validator:
    schema = json.loads(schema_file.read_text())
    return Draft202012Validator(schema)


def clean_input(inp: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in inp.items() if key not in INPUT_BLOAT_KEYS}


def normalize_key_inputs(values: dict[str, Any]) -> dict[str, str]:
    normalized = {
        key: value
        for key, value in values.items()
        if isinstance(value, str) and value.strip()
    }
    return dict(sorted(normalized.items()))


def normalize_connections(connections: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for connection in connections:
        item = {"provider": str(connection["provider"])}
        if "connection" in connection:
            item["connection"] = str(connection["connection"])
        normalized.append(item)
    return sorted(normalized, key=lambda item: (item["provider"], item.get("connection", "")))


def normalize_statistics(statistics: dict[str, Any]) -> dict[str, Any]:
    return {
        "total_blocks": int(statistics["total_blocks"]),
        "max_depth": int(statistics["max_depth"]),
        "by_keyword": dict(sorted((str(key), int(value)) for key, value in statistics["by_keyword"].items())),
        "by_provider": dict(sorted((str(key), int(value)) for key, value in statistics["by_provider"].items())),
    }


def normalize_callable(callable_data: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    if "parameters" in callable_data:
        normalized["parameters"] = [
            {
                "name": str(item["name"]),
                "type": str(item["type"]),
                "label": str(item["label"]),
            }
            for item in callable_data["parameters"]
        ]
    if "results" in callable_data:
        normalized["results"] = [
            {
                "name": str(item["name"]),
                "type": str(item["type"]),
                "label": str(item["label"]),
            }
            for item in callable_data["results"]
        ]
    if "parameters_raw" in callable_data:
        normalized["parameters_raw"] = str(callable_data["parameters_raw"])
    if "results_raw" in callable_data:
        normalized["results_raw"] = str(callable_data["results_raw"])
    return normalized


def collect_project_props(obj: Any, props: set[str]) -> None:
    if isinstance(obj, dict):
        if obj.get("pill_type") == "project_property":
            name = obj.get("property_name")
            if name:
                props.add(str(name))
        for value in obj.values():
            collect_project_props(value, props)
        return
    if isinstance(obj, list):
        for item in obj:
            collect_project_props(item, props)
        return
    if isinstance(obj, str) and "project_property" in obj:
        for match in re.finditer(r'"property_name"\s*:\s*"([^"]+)"', obj):
            props.add(match.group(1))


def parse_retry_count(value: Any) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return 0


def parse_retry_interval_seconds(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def normalize_rhs(condition: dict[str, Any]) -> str | None:
    if "rhs" not in condition or condition.get("rhs") is None:
        return None
    return str(condition["rhs"])


def normalize_filter(filter_data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not filter_data:
        return None
    return {
        "operator": str(filter_data.get("operator", filter_data.get("operand", "and"))).upper(),
        "conditions": [
            {
                "lhs": "" if cond.get("lhs") is None else str(cond.get("lhs", "")),
                "op": str(cond.get("op", cond.get("operand", ""))).upper(),
                "rhs": normalize_rhs(cond),
            }
            for cond in filter_data.get("conditions", [])
        ],
    }


def walk_raw_blocks(
    block: dict[str, Any],
    *,
    depth: int = 0,
    parent_number: int | None = None,
) -> list[dict[str, Any]]:
    number = int(block.get("number", 0 if parent_number is None else -1))
    keyword = "trigger" if parent_number is None else str(block.get("keyword", ""))
    current = {
        "number": number,
        "keyword": keyword,
        "provider": str(block.get("provider", "")),
        "name": str(block.get("name", "")),
        "depth": depth,
        "parent_number": parent_number,
        "child_numbers": [],
        "skip": bool(block.get("skip", False)),
        "input": clean_input(block.get("input", {}) if isinstance(block.get("input"), dict) else {}),
        "filter": block.get("filter"),
    }

    walked = [current]
    child_numbers: list[int] = []
    for child in block.get("block", []):
        if child is None:
            continue
        child_number = int(child.get("number", -1))
        child_numbers.append(child_number)
        walked.extend(walk_raw_blocks(child, depth=depth + 1, parent_number=number))
    current["child_numbers"] = child_numbers
    return walked


def build_callable(trigger: dict[str, Any]) -> dict[str, Any] | None:
    if trigger.get("provider") != "workato_recipe_function":
        return None

    params_json = trigger.get("input", {}).get("parameters_schema_json", "")
    results_json = trigger.get("input", {}).get("result_schema_json", "")
    callable_data: dict[str, Any] = {}

    if params_json:
        try:
            params = json.loads(params_json)
            callable_data["parameters"] = [
                {
                    "name": str(item.get("name", "")),
                    "type": str(item.get("type", "")),
                    "label": str(item.get("label", "")),
                }
                for item in params
            ]
        except json.JSONDecodeError:
            callable_data["parameters_raw"] = str(params_json)

    if results_json:
        try:
            results = json.loads(results_json)
            callable_data["results"] = [
                {
                    "name": str(item.get("name", "")),
                    "type": str(item.get("type", "")),
                    "label": str(item.get("label", "")),
                }
                for item in results
            ]
        except json.JSONDecodeError:
            callable_data["results_raw"] = str(results_json)

    return callable_data or None


def build_control_flow_blocks(raw_blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "number": int(block["number"]),
            "keyword": str(block["keyword"]),
            "provider": str(block["provider"]),
            "name": str(block["name"]),
            "depth": int(block["depth"]),
            "parent_number": block["parent_number"],
            "child_numbers": [int(value) for value in block["child_numbers"]],
            "skip": bool(block["skip"]),
        }
        for block in raw_blocks
    ]


def normalize_control_flow_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "number": int(block["number"]),
            "keyword": str(block["keyword"]),
            "provider": str(block.get("provider", "")),
            "name": str(block.get("name", "")),
            "depth": int(block["depth"]),
            "parent_number": None if block.get("parent_number") is None else int(block["parent_number"]),
            "child_numbers": [int(value) for value in block["child_numbers"]],
            "skip": bool(block.get("skip", False)),
        }
        for block in blocks
    ]


def _block_by_number(blocks: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {int(block["number"]): block for block in blocks}


def validate_control_flow_blocks(blocks: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not blocks:
        return ["control_flow.blocks is empty"]

    numbers = [int(block["number"]) for block in blocks]
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    if duplicates:
        errors.append(f"duplicate block numbers: {duplicates}")

    block_by_number = _block_by_number(blocks)
    roots = [block["number"] for block in blocks if block["parent_number"] is None]
    if len(roots) != 1:
        errors.append(f"expected exactly one root block, found {roots}")

    for block in blocks:
        number = int(block["number"])
        parent_number = block["parent_number"]
        depth = int(block["depth"])
        child_numbers = [int(value) for value in block["child_numbers"]]

        if parent_number is None:
            if depth != 0:
                errors.append(f"block {number} has root parent but depth {depth}")
        else:
            parent = block_by_number.get(int(parent_number))
            if parent is None:
                errors.append(f"block {number} references missing parent {parent_number}")
            else:
                if number not in parent["child_numbers"]:
                    errors.append(f"block {number} missing from parent {parent_number} child_numbers")
                if depth != int(parent["depth"]) + 1:
                    errors.append(f"block {number} depth {depth} does not match parent {parent_number}")

        for child_number in child_numbers:
            child = block_by_number.get(child_number)
            if child is None:
                errors.append(f"block {number} references missing child {child_number}")
                continue
            if child["parent_number"] != number:
                errors.append(f"block {number} child {child_number} has parent {child['parent_number']}")

    return errors


def build_try_catch_pairs_from_raw(raw_blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    block_by_number = _block_by_number(raw_blocks)
    paired_catches: set[int] = set()
    pairs: list[dict[str, Any]] = []

    for block in raw_blocks:
        if block["keyword"] != "try":
            continue

        try_number = int(block["number"])
        child_catches = [
            int(child_number)
            for child_number in block["child_numbers"]
            if child_number in block_by_number and block_by_number[child_number]["keyword"] == "catch"
        ]
        if len(child_catches) > 1:
            raise ProjectionError(f"try block {try_number} has multiple child catches: {child_catches}")

        catch_number: int | None = child_catches[0] if child_catches else None
        if catch_number is None and block["parent_number"] is not None:
            parent = block_by_number.get(int(block["parent_number"]))
            if parent is not None:
                siblings = [int(value) for value in parent["child_numbers"]]
                try_index = siblings.index(try_number) if try_number in siblings else -1
                if 0 <= try_index + 1 < len(siblings):
                    next_number = siblings[try_index + 1]
                    next_block = block_by_number.get(next_number)
                    if next_block is not None and next_block["keyword"] == "catch":
                        catch_number = next_number

        if catch_number is not None:
            if catch_number in paired_catches:
                raise ProjectionError(f"catch block {catch_number} is paired more than once")
            paired_catches.add(catch_number)

        catch_block = block_by_number.get(catch_number) if catch_number is not None else None
        pairs.append(
            {
                "try_block": try_number,
                "catch_block": catch_number,
                "retry_count": parse_retry_count(catch_block["input"].get("max_retry_count")) if catch_block else 0,
                "retry_interval_seconds": (
                    parse_retry_interval_seconds(catch_block["input"].get("retry_interval")) if catch_block else None
                ),
                "filter": normalize_filter(catch_block.get("filter")) if catch_block else None,
                "catch_action_numbers": [int(value) for value in (catch_block["child_numbers"] if catch_block else [])],
            }
        )

    catch_numbers = {
        int(block["number"])
        for block in raw_blocks
        if block["keyword"] == "catch"
    }
    unpaired = sorted(catch_numbers - paired_catches)
    if unpaired:
        raise ProjectionError(f"unpaired catch blocks: {unpaired}")

    return pairs


def normalize_try_catch_pairs(pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "try_block": int(pair["try_block"]),
            "catch_block": None if pair.get("catch_block") is None else int(pair["catch_block"]),
            "retry_count": parse_retry_count(pair.get("retry_count")),
            "retry_interval_seconds": parse_retry_interval_seconds(pair.get("retry_interval_seconds")),
            "filter": normalize_filter(pair.get("filter")),
            "catch_action_numbers": [int(value) for value in pair.get("catch_action_numbers", [])],
        }
        for pair in pairs
    ]


def build_stop_blocks_from_raw(raw_blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stops: list[dict[str, Any]] = []
    for block in raw_blocks:
        if block["keyword"] != "stop":
            continue
        stop_with_error = str(block["input"].get("stop_with_error", "false")).lower() == "true"
        stop_reason_raw = block["input"].get("stop_reason")
        stops.append(
            {
                "number": int(block["number"]),
                "stop_with_error": stop_with_error,
                "stop_reason_raw": None if stop_reason_raw is None else str(stop_reason_raw),
                "skip": bool(block["skip"]),
            }
        )
    return stops


def normalize_stop_blocks(stop_blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "number": int(stop_block["number"]),
            "stop_with_error": bool(stop_block["stop_with_error"]),
            "stop_reason_raw": (
                None if stop_block.get("stop_reason_raw") is None else str(stop_block["stop_reason_raw"])
            ),
            "skip": bool(stop_block.get("skip", False)),
        }
        for stop_block in stop_blocks
    ]


def validate_error_handling_projection(
    control_flow_blocks: list[dict[str, Any]],
    error_handling: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    block_by_number = _block_by_number(control_flow_blocks)
    try_numbers = {int(block["number"]) for block in control_flow_blocks if block["keyword"] == "try"}
    catch_numbers = {int(block["number"]) for block in control_flow_blocks if block["keyword"] == "catch"}
    stop_numbers = {int(block["number"]) for block in control_flow_blocks if block["keyword"] == "stop"}

    pair_trys: set[int] = set()
    pair_catches: set[int] = set()
    for pair in error_handling["try_catch_pairs"]:
        try_number = int(pair["try_block"])
        if try_number in pair_trys:
            errors.append(f"try block {try_number} appears more than once in try_catch_pairs")
        pair_trys.add(try_number)

        try_block = block_by_number.get(try_number)
        if try_block is None or try_block["keyword"] != "try":
            errors.append(f"try_catch_pairs references non-try block {try_number}")

        catch_number = pair["catch_block"]
        if catch_number is None:
            if pair["catch_action_numbers"]:
                errors.append(f"try block {try_number} has catch actions but no catch block")
            continue

        catch_number = int(catch_number)
        catch_block = block_by_number.get(catch_number)
        if catch_block is None or catch_block["keyword"] != "catch":
            errors.append(f"try block {try_number} references non-catch block {catch_number}")
            continue
        if catch_number in pair_catches:
            errors.append(f"catch block {catch_number} appears more than once in try_catch_pairs")
        pair_catches.add(catch_number)
        if pair["catch_action_numbers"] != [int(value) for value in catch_block["child_numbers"]]:
            errors.append(f"catch block {catch_number} catch_action_numbers do not match child_numbers")

    missing_tries = sorted(try_numbers - pair_trys)
    if missing_tries:
        errors.append(f"missing try_catch_pairs for try blocks: {missing_tries}")

    unpaired_catches = sorted(catch_numbers - pair_catches)
    if unpaired_catches:
        errors.append(f"unpaired catch blocks: {unpaired_catches}")

    seen_stops: set[int] = set()
    for stop_block in error_handling["stop_blocks"]:
        stop_number = int(stop_block["number"])
        if stop_number in seen_stops:
            errors.append(f"stop block {stop_number} appears more than once in stop_blocks")
        seen_stops.add(stop_number)

        block = block_by_number.get(stop_number)
        if block is None or block["keyword"] != "stop":
            errors.append(f"stop_blocks references non-stop block {stop_number}")
            continue
        if bool(stop_block["skip"]) != bool(block["skip"]):
            errors.append(f"stop block {stop_number} skip does not match control_flow")

    missing_stops = sorted(stop_numbers - seen_stops)
    if missing_stops:
        errors.append(f"missing stop_blocks for stop blocks: {missing_stops}")

    return errors


def project_expected_summary(recipe: dict[str, Any]) -> dict[str, Any]:
    trigger = recipe["code"]
    trigger_input = clean_input(trigger.get("input", {}) if isinstance(trigger.get("input"), dict) else {})
    raw_blocks = walk_raw_blocks(trigger)
    control_flow_blocks = build_control_flow_blocks(raw_blocks)
    control_flow_errors = validate_control_flow_blocks(control_flow_blocks)
    if control_flow_errors:
        raise ProjectionError(control_flow_errors)

    try_catch_pairs = build_try_catch_pairs_from_raw(raw_blocks)
    stop_blocks = build_stop_blocks_from_raw(raw_blocks)
    error_handling = {
        "try_catch_pairs": try_catch_pairs,
        "stop_blocks": stop_blocks,
    }
    error_handling_errors = validate_error_handling_projection(control_flow_blocks, error_handling)
    if error_handling_errors:
        raise ProjectionError(error_handling_errors)

    keyword_counts: dict[str, int] = {}
    provider_counts: dict[str, int] = {}
    max_depth = 0
    for block in raw_blocks:
        keyword = str(block.get("keyword", ""))
        provider = str(block.get("provider", ""))
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        if provider:
            provider_counts[provider] = provider_counts.get(provider, 0) + 1
        max_depth = max(max_depth, int(block["depth"]))

    connections: list[dict[str, Any]] = []
    for cfg in recipe.get("config", []):
        provider = cfg.get("provider", "")
        if not provider:
            continue
        item: dict[str, Any] = {"provider": provider}
        account = cfg.get("account_id")
        if isinstance(account, dict):
            item["connection"] = account.get("name", "")
        connections.append(item)

    projected: dict[str, Any] = {
        "name": recipe["name"],
        "version": recipe["version"],
        "trigger": {
            "provider": trigger["provider"],
            "action": trigger["name"],
            "key_inputs": normalize_key_inputs(trigger_input),
        },
        "connections": normalize_connections(connections),
        "statistics": {
            "total_blocks": len(raw_blocks),
            "max_depth": max_depth,
            "by_keyword": dict(sorted(keyword_counts.items())),
            "by_provider": dict(sorted(provider_counts.items())),
        },
        "control_flow": {
            "blocks": control_flow_blocks,
        },
        "error_handling": error_handling,
    }

    version_comment = recipe.get("version_comment")
    if version_comment:
        projected["version_comment"] = version_comment

    concurrency = recipe.get("concurrency")
    if concurrency is not None:
        projected["concurrency"] = concurrency

    project_props: set[str] = set()
    collect_project_props(recipe.get("code", {}), project_props)
    if project_props:
        projected["project_properties"] = sorted(project_props)

    callable_data = build_callable(trigger)
    if callable_data is not None:
        projected["callable"] = callable_data

    return projected


def project_extracted_summary(summary: dict[str, Any]) -> dict[str, Any]:
    control_flow_blocks = normalize_control_flow_blocks(summary["control_flow"]["blocks"])
    control_flow_errors = validate_control_flow_blocks(control_flow_blocks)
    if control_flow_errors:
        raise ProjectionError(control_flow_errors)

    error_handling = {
        "try_catch_pairs": normalize_try_catch_pairs(summary["error_handling"]["try_catch_pairs"]),
        "stop_blocks": normalize_stop_blocks(summary["error_handling"]["stop_blocks"]),
    }
    error_handling_errors = validate_error_handling_projection(control_flow_blocks, error_handling)
    if error_handling_errors:
        raise ProjectionError(error_handling_errors)

    projected: dict[str, Any] = {
        "name": summary["name"],
        "version": summary["version"],
        "trigger": {
            "provider": summary["trigger"]["provider"],
            "action": summary["trigger"]["action"],
            "key_inputs": normalize_key_inputs(summary["trigger"]["key_inputs"]),
        },
        "connections": normalize_connections(summary["connections"]),
        "statistics": normalize_statistics(summary["statistics"]),
        "control_flow": {
            "blocks": control_flow_blocks,
        },
        "error_handling": error_handling,
    }

    if "version_comment" in summary:
        projected["version_comment"] = summary["version_comment"]
    if "concurrency" in summary:
        projected["concurrency"] = summary["concurrency"]
    if "project_properties" in summary:
        projected["project_properties"] = sorted(str(item) for item in summary["project_properties"])
    if "callable" in summary:
        projected["callable"] = normalize_callable(summary["callable"])

    return projected


def validate_projection(
    projection: dict[str, Any],
    validator: Draft202012Validator,
    source: str,
) -> list[str]:
    return [
        f"{source}: {'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in validator.iter_errors(projection)
    ]


def diff_values(expected: Any, actual: Any, path: str = "") -> list[dict[str, Any]]:
    field = path or "<root>"
    if type(expected) is not type(actual):
        return [{"field": field, "expected": expected, "actual": actual}]

    if isinstance(expected, dict):
        mismatches: list[dict[str, Any]] = []
        for key in sorted(set(expected) | set(actual)):
            child_path = f"{path}.{key}" if path else str(key)
            if key not in expected:
                mismatches.append({"field": child_path, "expected": None, "actual": actual[key]})
                continue
            if key not in actual:
                mismatches.append({"field": child_path, "expected": expected[key], "actual": None})
                continue
            mismatches.extend(diff_values(expected[key], actual[key], child_path))
        return mismatches

    if isinstance(expected, list):
        if len(expected) != len(actual):
            return [{"field": field, "expected": expected, "actual": actual}]
        mismatches: list[dict[str, Any]] = []
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual, strict=True)):
            mismatches.extend(diff_values(expected_item, actual_item, f"{field}[{index}]"))
        return mismatches

    if expected != actual:
        return [{"field": field, "expected": expected, "actual": actual}]
    return []
