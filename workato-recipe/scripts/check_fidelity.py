#!/usr/bin/env python3
"""Check one raw recipe JSON file against one extracted summary.json file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from fidelity_projection import (
        ProjectionError,
        diff_values,
        load_schema_validator,
        project_expected_summary,
        project_extracted_summary,
        validate_projection,
    )
except ModuleNotFoundError as exc:
    if exc.name == "jsonschema":
        print(
            "ERROR: Missing dependency 'jsonschema'. Run this command with "
            "`uv run --project /path/to/workato-recipe python /path/to/workato-recipe/cli.py check-fidelity ...`.",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    raise

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = PLUGIN_ROOT / "schemas" / "summary_fidelity_v2.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", required=True, help="Path to the raw .recipe.json file")
    parser.add_argument("--summary", required=True, help="Path to the extracted summary.json file")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Path to the fidelity schema")
    parser.add_argument("--output", help="Write result JSON to this path")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="stdout format")
    return parser.parse_args()


def slug_from_recipe(recipe_path: Path) -> str:
    name = recipe_path.name
    return name[:-12] if name.endswith(".recipe.json") else recipe_path.stem


def build_result(recipe_path: Path, summary_path: Path, schema_path: Path) -> dict[str, Any]:
    recipe_slug = slug_from_recipe(recipe_path)
    schema_errors: list[str] = []
    projection_errors: list[str] = []
    mismatches: list[dict[str, Any]] = []
    validator = load_schema_validator(schema_path)

    if not recipe_path.exists():
        projection_errors.append(f"raw recipe missing: {recipe_path}")
    if not summary_path.exists():
        projection_errors.append(f"extracted summary missing: {summary_path}")
    if projection_errors:
        return {
            "recipe_slug": recipe_slug,
            "recipe_path": str(recipe_path),
            "summary_path": str(summary_path),
            "pass": False,
            "schema_errors": schema_errors,
            "projection_errors": projection_errors,
            "mismatches": mismatches,
        }

    expected: dict[str, Any] | None = None
    actual: dict[str, Any] | None = None

    try:
        recipe = json.loads(recipe_path.read_text())
        expected = project_expected_summary(recipe)
    except ProjectionError as exc:
        projection_errors.extend([f"expected: {error}" for error in exc.errors])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        projection_errors.append(f"expected projection failed: {exc}")

    try:
        summary = json.loads(summary_path.read_text())
        actual = project_extracted_summary(summary)
    except ProjectionError as exc:
        projection_errors.extend([f"actual: {error}" for error in exc.errors])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        projection_errors.append(f"extractor projection failed: {exc}")

    if expected is not None:
        schema_errors.extend(validate_projection(expected, validator, "expected"))
    if actual is not None:
        schema_errors.extend(validate_projection(actual, validator, "actual"))

    if not projection_errors and not schema_errors and expected is not None and actual is not None:
        mismatches = diff_values(expected, actual)

    return {
        "recipe_slug": recipe_slug,
        "recipe_path": str(recipe_path),
        "summary_path": str(summary_path),
        "pass": not projection_errors and not schema_errors and not mismatches,
        "schema_errors": schema_errors,
        "projection_errors": projection_errors,
        "mismatches": mismatches,
    }


def main() -> None:
    args = parse_args()
    result = build_result(Path(args.recipe).resolve(), Path(args.summary).resolve(), Path(args.schema).resolve())

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        if result["pass"]:
            print(f"PASS: {result['recipe_slug']}")
        else:
            print(f"FAIL: {result['recipe_slug']}")
            for error in result["projection_errors"]:
                print(f"  projection: {error}")
            for error in result["schema_errors"]:
                print(f"  schema: {error}")
            for mismatch in result["mismatches"]:
                print(
                    f"  mismatch: {mismatch['field']}: expected={mismatch['expected']!r} actual={mismatch['actual']!r}"
                )

    if not result["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
