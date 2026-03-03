---
name: oasb-scaffold
version: 0.1.0
description: >-
  OASBuilder pipeline package conventions for scaffolding new stages. Use when
  creating a new oasb-* package, scaffolding an OASBuilder stage, setting up a
  hatchling Python pipeline package, or following OASBuilder conventions for CLI,
  schema, validation, and LLM call patterns. Also use when adding a new stage to
  the oasb-complete workspace, working in any oasb-* repo, or when the user
  mentions "OASBuilder conventions", "pipeline package", "oasb-scaffold", or asks
  about the standard pattern for oasb packages.
---

# OASBuilder Package Conventions

When creating a new OASBuilder pipeline stage package, follow these conventions
established by oasb-demonstrative and confirmed across oasb-descriptive,
oasb-merge, and oasb-enhance.

## Package Layout

- `src/oasb_{stage}/` with hatchling build backend
- `pyproject.toml` with `[tool.hatch.build.targets.wheel] packages = ["src/oasb_{stage}"]`
- Python `>=3.12`, use `X | None` not `Optional[X]`, `dict[str, str]` not `Dict`
- `from __future__ import annotations` at top of every module

## pyproject.toml Template

```toml
[project]
name = "oasb-{stage}"
version = "0.1.0"
description = "Stage N of OASBuilder: ..."
requires-python = ">=3.12"
dependencies = [
    "oasb-scraper",          # upstream dependency
    "anthropic>=0.52.0",     # omit if stage is deterministic (e.g., merge)
    "pydantic>=2.12.5",
    "python-dotenv>=1.0",
    "click>=8.3.1",
    "rich>=14.3.2",
]

[project.scripts]
oasb-{stage} = "oasb_{stage}.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oasb_{stage}"]
```

## Required Files

| File | Role |
|------|------|
| `__init__.py` | Exports `run_pipeline()` + `{Stage}Result` only |
| `__main__.py` | `from .main import cli; cli()` |
| `schema.py` | Pydantic models (see Schema Conventions below) |
| `main.py` | CLI (`@click.command`) + `run_pipeline()` orchestration |
| `validate.py` | Output validation + Rich summary table |

## Schema Conventions

Every stage result follows this shape:

```python
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class Operation{Stage}(BaseModel):
    """Per-operation summary."""
    method: str
    endpoint_path: str  # or just `path`
    # stage-specific counters...
    errors: list[str] = Field(default_factory=list)

class {Stage}Metadata(BaseModel):
    timestamp: datetime
    source_url: str  # or source_scrape_url
    total_operations: int
    # stage-specific counters...
    llm_calls_made: int  # 0 for deterministic stages

class {Stage}Result(BaseModel):
    source_url: str
    base_url: str | None = None
    partial_oas: dict[str, Any]  # or merged_oas, enhanced_oas
    operations: list[Operation{Stage}]
    metadata: {Stage}Metadata
```

Use `Field(default_factory=list)` for all mutable defaults. Never use bare `[]`.

## Pipeline Function Pattern

```python
async def run_pipeline(
    input: InputModel | str | Path,
    *,
    model: str = "claude-haiku-4-5",
    max_concurrent: int = 5,
    output_dir: Path | None = None,
) -> StageResult | None:
```

- Accepts Pydantic model object OR file path (str/Path)
- Returns `None` on failure, never raises
- `load_dotenv()` inside `run_pipeline()`, not at module level
- Deterministic stages (merge) omit `model` and `max_concurrent` params

## CLI Pattern

```python
@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--model", default="claude-haiku-4-5")
@click.option("--max-concurrent", default=5, type=int)
@click.option("--output-dir", default=None, type=click.Path())
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
def cli(input_file, model, max_concurrent, output_dir, verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    result = asyncio.run(run_pipeline(input_file, model=model, ...))
    if result is None:
        sys.exit(1)
```

Merge stage takes two positional args (demo_file, desc_file) instead of one.

## Error Handling

- Best-effort per operation — individual failures don't crash the pipeline
- Errors collected in `errors: list[str]` on the per-operation model
- `run_pipeline()` returns `None` on complete failure

## LLM Calls

- `anthropic.AsyncAnthropic` with `asyncio.Semaphore(max_concurrent)` for rate limiting
- `LLMCallCounter` (async lock + counter) for tracking total calls
- Retry on `RateLimitError`/`APIConnectionError` with exponential backoff (up to 3 attempts)
- Extract JSON from responses handling: direct parse, ```json``` fences, first-brace-to-last-brace

## Validate Pattern

```python
def validate_file(path: Path) -> StageResult | None:
    """Load, validate, check OAS structure, print Rich summary."""

def _check_oas_structure(oas: dict) -> list[str]:
    """Return list of structural issues."""

def _print_summary(result: StageResult) -> None:
    """Rich table with per-operation stats."""

def main() -> None:
    """CLI: python -m oasb_{stage}.validate <file.json>"""
```

## Output Conventions

- Written to `generated/` (gitignored)
- Filename: `{stage}_{url_slug}.json` where slug is derived from source URL
- Rich progress spinner via `Progress(SpinnerColumn(), TextColumn(...))`
- Final output path printed with `[green]Output written to:[/green]`

## Test Conventions

- Tests in `tests/` directory — **no `__init__.py`** (avoids namespace collisions in workspaces)
- Use `pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml`
- Mock LLM calls with `unittest.mock.AsyncMock` on the Anthropic client
- `logging.getLogger(__name__)` per module; `--verbose` flag for DEBUG
