---
name: workato-recipe
description: >-
  Parse and analyze Workato recipe JSON exports. Use when the user asks about
  a Workato recipe's logic, data flow, field mappings, error handling, or
  control flow. Also use when the user references a .recipe.json file or asks
  to debug a Workato integration.
argument-hint: "<path> [overview|deep|<question>]"
---

# Workato Recipe Analyzer

Preprocesses Workato recipe JSON exports (1K–97K lines) into focused view files,
stripping ~90–98% of UI/schema bloat to expose the actual recipe logic.

## Workflow

### 1. Resolve the recipe path

Determine the `.recipe.json` path from:
- The argument (e.g., `/workato-recipe global-context/sources/workato/.../str_rec_001...recipe.json`)
- A path mentioned in conversation context
- If ambiguous, ask the user or use Glob to search: `global-context/sources/workato/**/*.recipe.json`

### 2. Run preprocessing

Resolve `PLUGIN_ROOT` to the root of this plugin before running commands:
- In Claude Code, use `CLAUDE_PLUGIN_ROOT` when it is available.
- In Codex, infer it from this skill path: `workato-recipe/skills/workato-recipe/SKILL.md` lives two directories below the plugin root.
- If neither is obvious, locate the directory containing `workato-recipe/cli.py`.

Call the stable plugin CLI rather than internal scripts:

```bash
uv run --project "$PLUGIN_ROOT" python "$PLUGIN_ROOT/cli.py" extract --recipe "$RECIPE_PATH"
```

The script outputs the views directory path to stdout. Views are cached in
`.scratch/workato-views/` (invalidated by source mtime or extractor version change).

Use `--force` to regenerate. Use `--all` to process all non-archived recipes.

Developer utilities live at the plugin root `cli.py` entry point. Consumers
should call that stable CLI rather than depending on internal script paths.

### 3. Select analysis depth

Based on the argument or question:

**overview** (default — no depth specified):
- Read `summary.json` from the views directory
- Report: recipe name, version, trigger, connections, block/provider counts
- For callable recipes, show parameters and results

**deep** (argument contains "deep", a specific question, or a block reference):
- Read `summary.json` and `unified_logic.md` from the views directory.
- Answer the question by tracing block numbers, data pills, branches, and variable mutations.
- In Claude Code, you may delegate to the `workato-recipe:recipe-analyzer` subagent if it is available. In Codex, analyze inline; Claude subagent definitions are not a Codex plugin interface.

## View Files

| File | Content | Size (typical) |
|------|---------|----------------|
| `summary.json` | Metadata plus structured control-flow and error-handling contract | ~4-8KB |
| `unified_logic.md` | Single unified document with control flow, mappings, variables, and error handling | ~20-30KB |

## References

- `references/recipe-schema.md` — Recipe JSON structure and datapill syntax
- `references/view-formats.md` — View file formats and cross-referencing
