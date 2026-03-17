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
    validate_loop_handling_projection,
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

    def test_existing_no_loop_fixtures_project_empty_loop_handling(self) -> None:
        for fixture_name in (
            "nested_filtered.recipe.json",
            "sibling_catch.recipe.json",
            "orphaned_try.recipe.json",
        ):
            with self.subTest(fixture_name=fixture_name):
                projection = project_expected_summary(load_recipe(fixture_name))
                self.assertEqual(projection["loop_handling"], {"loop_blocks": []})

    def test_foreach_batch_projection_contains_loop_handling(self) -> None:
        projection = project_expected_summary(load_recipe("foreach_batch.recipe.json"))
        self.assertEqual(
            projection["loop_handling"],
            {
                "loop_blocks": [
                    {
                        "number": 1,
                        "keyword": "foreach",
                        "skip": False,
                        "source_raw": "#{_dp('{\"pill_type\":\"output\",\"provider\":\"list_source\",\"line\":\"list_rows\",\"path\":[\"items\"]}')}",
                        "repeat_mode": "batch",
                        "batch_size": "500",
                        "clear_scope": "true",
                        "while_conditions": [],
                        "body_block_numbers": [2],
                    }
                ]
            },
        )

    def test_foreach_simple_projection_uses_null_for_missing_batch_size(self) -> None:
        projection = project_expected_summary(load_recipe("foreach_simple.recipe.json"))
        loop_block = projection["loop_handling"]["loop_blocks"][0]
        self.assertEqual(loop_block["keyword"], "foreach")
        self.assertEqual(loop_block["repeat_mode"], "simple")
        self.assertIsNone(loop_block["batch_size"])
        self.assertNotEqual(loop_block["batch_size"], "")
        self.assertEqual(loop_block["clear_scope"], "false")
        self.assertEqual(loop_block["body_block_numbers"], [2])
        self.assertEqual(loop_block["while_conditions"], [])

    def test_repeat_while_projection_contains_loop_handling(self) -> None:
        projection = project_expected_summary(load_recipe("repeat_while.recipe.json"))
        self.assertEqual(
            projection["loop_handling"],
            {
                "loop_blocks": [
                    {
                        "number": 1,
                        "keyword": "repeat",
                        "skip": False,
                        "source_raw": None,
                        "repeat_mode": None,
                        "batch_size": None,
                        "clear_scope": None,
                        "while_conditions": [
                            {
                                "number": 3,
                                "filter": {
                                    "operator": "AND",
                                    "conditions": [
                                        {
                                            "lhs": "#{_dp('{\"pill_type\":\"output\",\"provider\":\"workato_variable\",\"line\":\"cursor_var\",\"path\":[\"cursor\"]}')}",
                                            "op": "PRESENT",
                                            "rhs": "",
                                        }
                                    ],
                                },
                            }
                        ],
                        "body_block_numbers": [2],
                    }
                ]
            },
        )

    def test_nested_loops_preserve_preorder_and_child_partitioning(self) -> None:
        projection = project_expected_summary(load_recipe("nested_loops.recipe.json"))
        loop_blocks = projection["loop_handling"]["loop_blocks"]
        self.assertEqual([item["number"] for item in loop_blocks], [1, 2])
        self.assertEqual(loop_blocks[0]["body_block_numbers"], [2])
        self.assertEqual(loop_blocks[0]["while_conditions"], [])
        self.assertEqual(loop_blocks[1]["body_block_numbers"], [3])
        self.assertEqual(loop_blocks[1]["while_conditions"], [])
        self.assertIsNone(loop_blocks[1]["batch_size"])

    def test_ambiguous_multi_catch_raises_projection_error(self) -> None:
        with self.assertRaises(ProjectionError) as ctx:
            project_expected_summary(load_recipe("ambiguous_multi_catch.recipe.json"))
        self.assertIn("multiple child catches", ctx.exception.errors[0])

    def test_extracted_projection_accepts_valid_v2_summary(self) -> None:
        expected = project_expected_summary(load_recipe("nested_filtered.recipe.json"))
        extracted_like_summary = json.loads(json.dumps(expected))
        self.assertEqual(project_extracted_summary(extracted_like_summary), expected)

    def test_extracted_projection_roundtrips_loop_handling_for_all_loop_fixtures(self) -> None:
        for fixture_name in (
            "foreach_batch.recipe.json",
            "foreach_simple.recipe.json",
            "repeat_while.recipe.json",
            "nested_loops.recipe.json",
        ):
            with self.subTest(fixture_name=fixture_name):
                expected = project_expected_summary(load_recipe(fixture_name))
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
            "loop_handling": {
                "loop_blocks": []
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

    def test_extracted_projection_rejects_invalid_loop_handling_accounting(self) -> None:
        summary = project_expected_summary(load_recipe("repeat_while.recipe.json"))
        summary = json.loads(json.dumps(summary))
        summary["loop_handling"]["loop_blocks"][0]["body_block_numbers"] = [2, 3]

        with self.assertRaises(ProjectionError) as ctx:
            project_extracted_summary(summary)
        self.assertIn("body_block_numbers incorrectly includes while_condition", "; ".join(ctx.exception.errors))

    def test_validate_loop_handling_rejects_while_condition_under_non_loop_parent(self) -> None:
        control_flow_blocks = [
            {
                "number": 0,
                "keyword": "trigger",
                "provider": "clock",
                "name": "scheduled_event",
                "depth": 0,
                "parent_number": None,
                "child_numbers": [1],
                "skip": False,
            },
            {
                "number": 1,
                "keyword": "try",
                "provider": "",
                "name": "",
                "depth": 1,
                "parent_number": 0,
                "child_numbers": [2],
                "skip": False,
            },
            {
                "number": 2,
                "keyword": "while_condition",
                "provider": "",
                "name": "",
                "depth": 2,
                "parent_number": 1,
                "child_numbers": [],
                "skip": False,
            },
        ]

        with self.assertRaises(ProjectionError) as ctx:
            validate_loop_handling_projection(control_flow_blocks, {"loop_blocks": []})
        self.assertIn("non-loop parent", ctx.exception.errors[0])

    def test_schema_validates_loop_handling_for_all_loop_fixtures(self) -> None:
        validator = load_schema_validator(SCHEMA_FILE)
        for fixture_name in (
            "foreach_batch.recipe.json",
            "foreach_simple.recipe.json",
            "repeat_while.recipe.json",
            "nested_loops.recipe.json",
        ):
            with self.subTest(fixture_name=fixture_name):
                projection = project_expected_summary(load_recipe(fixture_name))
                self.assertEqual(validate_projection(projection, validator, "expected"), [])

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
