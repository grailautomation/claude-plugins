from __future__ import annotations

import json
import unittest
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

from fidelity_projection import (  # noqa: E402
    ProjectionError,
    diff_values,
    load_schema_validator,
    project_expected_summary,
    project_extracted_summary,
    validate_projection,
)


SCHEMA_FILE = PLUGIN_ROOT / "schemas" / "summary_fidelity_v2.schema.json"
TESTDATA_DIR = PLUGIN_ROOT / "testdata"


def load_recipe(name: str) -> dict:
    return json.loads((TESTDATA_DIR / name).read_text())


class FidelityProjectionTests(unittest.TestCase):
    def test_nested_filtered_projection_contains_structural_fields(self) -> None:
        projection = project_expected_summary(load_recipe("nested_filtered.recipe.json"))

        control_flow = projection["control_flow"]["blocks"]
        self.assertEqual(control_flow[0]["number"], 0)
        self.assertIsNone(control_flow[0]["parent_number"])
        self.assertEqual(control_flow[1]["parent_number"], 0)
        self.assertEqual(control_flow[3]["number"], 3)
        self.assertEqual(control_flow[3]["depth"], 2)
        self.assertEqual(control_flow[3]["parent_number"], 1)
        self.assertTrue(control_flow[3]["skip"])

        error_handling = projection["error_handling"]
        self.assertEqual(len(error_handling["try_catch_pairs"]), 2)
        self.assertEqual(
            error_handling["try_catch_pairs"][0],
            {
                "try_block": 1,
                "catch_block": None,
                "retry_count": 0,
                "retry_interval_seconds": None,
                "filter": None,
                "catch_action_numbers": [],
            },
        )
        self.assertEqual(error_handling["try_catch_pairs"][1]["try_block"], 3)
        self.assertEqual(error_handling["try_catch_pairs"][1]["catch_block"], 5)
        self.assertEqual(error_handling["try_catch_pairs"][1]["retry_count"], 1)
        self.assertEqual(error_handling["try_catch_pairs"][1]["retry_interval_seconds"], 1)
        self.assertEqual(error_handling["try_catch_pairs"][1]["catch_action_numbers"], [])
        self.assertEqual(
            error_handling["try_catch_pairs"][1]["filter"]["conditions"],
            [
                {"lhs": "$.message", "op": "CONTAINS", "rhs": "429"},
                {"lhs": "$.retry_after", "op": "PRESENT", "rhs": None},
                {"lhs": "$.service", "op": "EQUALS", "rhs": ""},
            ],
        )
        self.assertEqual(
            error_handling["stop_blocks"],
            [
                {
                    "number": 6,
                    "stop_with_error": False,
                    "stop_reason_raw": "=_dp('{\"pill_type\":\"output\",\"provider\":\"db\",\"line\":\"db_query\",\"path\":[\"rows_processed\"]}')",
                    "skip": True,
                }
            ],
        )

    def test_sibling_catch_pairs_with_immediate_next_sibling(self) -> None:
        projection = project_expected_summary(load_recipe("sibling_catch.recipe.json"))
        self.assertEqual(
            projection["error_handling"]["try_catch_pairs"],
            [
                {
                    "try_block": 1,
                    "catch_block": 3,
                    "retry_count": 2,
                    "retry_interval_seconds": 5,
                    "filter": None,
                    "catch_action_numbers": [4],
                }
            ],
        )

    def test_orphaned_try_projects_with_null_catch(self) -> None:
        projection = project_expected_summary(load_recipe("orphaned_try.recipe.json"))
        self.assertEqual(
            projection["error_handling"]["try_catch_pairs"],
            [
                {
                    "try_block": 1,
                    "catch_block": None,
                    "retry_count": 0,
                    "retry_interval_seconds": None,
                    "filter": None,
                    "catch_action_numbers": [],
                }
            ],
        )

    def test_ambiguous_multi_catch_raises_projection_error(self) -> None:
        with self.assertRaises(ProjectionError) as ctx:
            project_expected_summary(load_recipe("ambiguous_multi_catch.recipe.json"))
        self.assertIn("multiple child catches", ctx.exception.errors[0])

    def test_extracted_projection_accepts_valid_v2_summary(self) -> None:
        expected = project_expected_summary(load_recipe("nested_filtered.recipe.json"))
        extracted_like_summary = json.loads(json.dumps(expected))
        self.assertEqual(project_extracted_summary(extracted_like_summary), expected)

    def test_extracted_projection_rejects_unpaired_catch(self) -> None:
        summary = {
            "name": "bad",
            "version": 1,
            "trigger": {
                "provider": "clock",
                "action": "scheduled_event",
                "key_inputs": {
                    "cron": "* * * * *"
                }
            },
            "connections": [],
            "statistics": {
                "total_blocks": 4,
                "max_depth": 2,
                "by_keyword": {
                    "trigger": 1,
                    "try": 1,
                    "catch": 2
                },
                "by_provider": {
                    "clock": 1
                }
            },
            "control_flow": {
                "blocks": [
                    {
                        "number": 0,
                        "keyword": "trigger",
                        "provider": "clock",
                        "name": "scheduled_event",
                        "depth": 0,
                        "parent_number": None,
                        "child_numbers": [1],
                        "skip": False
                    },
                    {
                        "number": 1,
                        "keyword": "try",
                        "provider": "",
                        "name": "",
                        "depth": 1,
                        "parent_number": 0,
                        "child_numbers": [2, 3],
                        "skip": False
                    },
                    {
                        "number": 2,
                        "keyword": "catch",
                        "provider": "",
                        "name": "",
                        "depth": 2,
                        "parent_number": 1,
                        "child_numbers": [],
                        "skip": False
                    },
                    {
                        "number": 3,
                        "keyword": "catch",
                        "provider": "",
                        "name": "",
                        "depth": 2,
                        "parent_number": 1,
                        "child_numbers": [],
                        "skip": False
                    }
                ]
            },
            "error_handling": {
                "try_catch_pairs": [
                    {
                        "try_block": 1,
                        "catch_block": 2,
                        "retry_count": 1,
                        "retry_interval_seconds": 3,
                        "filter": None,
                        "catch_action_numbers": []
                    }
                ],
                "stop_blocks": []
            }
        }

        with self.assertRaises(ProjectionError) as ctx:
            project_extracted_summary(summary)
        self.assertIn("unpaired catch blocks", "; ".join(ctx.exception.errors))

    def test_schema_and_diff_helpers_cover_failure_modes(self) -> None:
        validator = load_schema_validator(SCHEMA_FILE)
        expected = project_expected_summary(load_recipe("sibling_catch.recipe.json"))
        self.assertEqual(validate_projection(expected, validator, "expected"), [])

        invalid = {
            "name": "bad"
        }
        self.assertTrue(validate_projection(invalid, validator, "actual"))

        actual = json.loads(json.dumps(expected))
        actual["control_flow"]["blocks"][1]["parent_number"] = 999
        mismatches = diff_values(expected, actual)
        self.assertIn("control_flow.blocks[1].parent_number", [item["field"] for item in mismatches])


if __name__ == "__main__":
    unittest.main()
