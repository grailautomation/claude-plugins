#!/usr/bin/env python3
"""Validate plugin version and schema compatibility for consumers."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-version", help='Minimum version constraint, e.g. ">=1.1.0"')
    parser.add_argument("--require-schema-major", type=int, help="Required schema major version")
    return parser.parse_args()


def parse_version(value: str) -> tuple[int, ...]:
    parts = value.strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(f"invalid semantic version: {value}")
    return tuple(int(part) for part in parts)


def require_min_version(actual: str, requirement: str) -> None:
    match = re.fullmatch(r">=\s*([0-9]+(?:\.[0-9]+){0,2})", requirement.strip())
    if match is None:
        raise ValueError(f"unsupported version requirement: {requirement}")
    required = match.group(1)

    actual_tuple = parse_version(actual)
    required_tuple = parse_version(required)
    max_len = max(len(actual_tuple), len(required_tuple))
    actual_tuple += (0,) * (max_len - len(actual_tuple))
    required_tuple += (0,) * (max_len - len(required_tuple))
    if actual_tuple < required_tuple:
        raise ValueError(f"plugin version {actual} does not satisfy {requirement}")


def main() -> None:
    args = parse_args()
    plugin_meta = json.loads(PLUGIN_JSON.read_text())
    plugin_version = str(plugin_meta.get("version", ""))

    try:
        if args.require_version:
            require_min_version(plugin_version, args.require_version)

        if args.require_schema_major is not None:
            schema_file = PLUGIN_ROOT / "schemas" / f"summary_fidelity_v{args.require_schema_major}.schema.json"
            if not schema_file.exists():
                raise ValueError(f"required schema missing: {schema_file}")
            schema = json.loads(schema_file.read_text())
            schema_id = str(schema.get("$id", ""))
            if f"v{args.require_schema_major}" not in schema_id:
                raise ValueError(
                    f"schema id {schema_id!r} does not advertise required major v{args.require_schema_major}"
                )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        json.dumps(
            {
                "plugin": str(plugin_meta.get("name", "")),
                "version": plugin_version,
                "schema_major": args.require_schema_major,
            }
        )
    )


if __name__ == "__main__":
    main()
