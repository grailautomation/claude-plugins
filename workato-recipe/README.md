# workato-recipe

Generic Workato recipe extraction and fidelity utilities for Claude Code.

## Stable CLI Contract

Consumers should call the plugin through the root `cli.py` entry point.
Do not depend on internal paths under `skills/` or `scripts/`.

Examples:

```bash
uv run --project /path/to/workato-recipe python /path/to/workato-recipe/cli.py extract --recipe path/to/file.recipe.json

uv run --project /path/to/workato-recipe python /path/to/workato-recipe/cli.py check-fidelity \
  --recipe path/to/file.recipe.json \
  --summary path/to/file.recipe.views/summary.json \
  --format json

uv run --project /path/to/workato-recipe python /path/to/workato-recipe/cli.py check-compat \
  --require-version ">=1.1.0" \
  --require-schema-major 2

uv run --project /path/to/workato-recipe python /path/to/workato-recipe/cli.py self-test
```

## Contract Files

- Structured output contract: `schemas/summary_fidelity_v2.schema.json`
- Synthetic fixtures: `testdata/`
- Generic unit tests: `tests/`

Breaking-change rule: a schema major version bump requires consumer harness updates.
