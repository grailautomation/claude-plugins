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

```bash
uv run python "${CLAUDE_SKILL_DIR}/scripts/extract_views.py" "$RECIPE_PATH"
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
- Spawn the `workato-recipe:recipe-analyzer` subagent with the views directory path and question
- The subagent reads `summary.json` and `unified_logic.md` to provide detailed analysis

## View Files

| File | Content | Size (typical) |
|------|---------|----------------|
| `summary.json` | Metadata plus structured control-flow and error-handling contract | ~4-8KB |
| `unified_logic.md` | Single unified document with control flow, mappings, variables, and error handling | ~20-30KB |

## References

- `${CLAUDE_SKILL_DIR}/references/recipe-schema.md` — Recipe JSON structure and datapill syntax
- `${CLAUDE_SKILL_DIR}/references/view-formats.md` — View file formats and cross-referencing
