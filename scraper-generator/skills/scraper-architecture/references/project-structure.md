# Project Structure Reference

Complete layout and configuration for a scraper package.

## Directory Layout

```
{name}_scraper/
├── __init__.py
├── models.py
├── scraper.py
├── parser.py
├── sections.py
├── cli.py
└── formatters/
    ├── __init__.py
    ├── json_formatter.py
    ├── md_formatter.py
    └── openapi_formatter.py
```

Plus project files:

```
project_root/
├── {name}_scraper/       # The package
├── output/               # Generated output (gitignored)
├── main.py               # Entry point
├── pyproject.toml        # Package configuration
├── .gitignore
└── README.md
```

## File Templates

### `__init__.py`

```python
"""API documentation scraper package."""

from .models import APIDocumentation, Endpoint, Parameter, Example
from .parser import parse_documentation
from .scraper import fetch_html

__all__ = [
    "APIDocumentation",
    "Endpoint",
    "Parameter",
    "Example",
    "parse_documentation",
    "fetch_html",
]
```

### `sections.py`

Registry of documentation sections to scrape:

```python
"""API documentation sections registry."""

# Section ID → Display Name
API_SECTIONS: dict[str, str] = {
    "users": "Users",
    "connections": "Connections",
    "recipes": "Recipes",
    # Add all sections...
}

BASE_URL = "https://docs.example.com/api"

def get_section_url(section_id: str) -> str:
    """Get the URL for a documentation section."""
    return f"{BASE_URL}/{section_id}.html"

def get_section_name(section_id: str) -> str:
    """Get the display name for a section."""
    return API_SECTIONS.get(section_id, section_id.replace("-", " ").title())
```

### `cli.py`

Command-line interface:

```python
"""Command-line interface for the scraper."""

import argparse
import sys
from pathlib import Path

from .scraper import fetch_html
from .parser import parse_documentation
from .sections import API_SECTIONS
from .formatters import format_as_json, format_as_markdown, format_as_openapi


def main():
    parser = argparse.ArgumentParser(
        description="Scrape API documentation"
    )
    parser.add_argument(
        "--section",
        default="all",
        help="Section to scrape (or 'all')"
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "openapi", "all"],
        default="all",
        help="Output format"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Output directory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List available sections and exit"
    )

    args = parser.parse_args()

    if args.list_sections:
        print("Available sections:")
        for sid, name in sorted(API_SECTIONS.items()):
            print(f"  {sid}: {name}")
        return 0

    # Scrape sections
    sections = API_SECTIONS.keys() if args.section == "all" else [args.section]

    for section_id in sections:
        if args.verbose:
            print(f"Scraping {section_id}...")

        try:
            process_section(section_id, args)
        except Exception as e:
            print(f"Error processing {section_id}: {e}", file=sys.stderr)
            if not args.section == "all":
                return 1

    return 0


def process_section(section_id: str, args):
    """Process a single section."""
    # Fetch and parse
    html = fetch_html(section_id)
    doc = parse_documentation(html, section_id)

    # Prepare output directory
    if args.section == "all":
        out_dir = args.output_dir / section_id
    else:
        out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write outputs
    formats = ["json", "markdown", "openapi"] if args.format == "all" else [args.format]

    for fmt in formats:
        if fmt == "json":
            content = format_as_json(doc)
            suffix = "_api.json"
        elif fmt == "markdown":
            content = format_as_markdown(doc)
            suffix = "_api.md"
        elif fmt == "openapi":
            content = format_as_openapi(doc)
            suffix = "_openapi.yaml"

        out_file = out_dir / f"{section_id}{suffix}"
        out_file.write_text(content)

        if args.verbose:
            print(f"  Wrote {out_file}")


if __name__ == "__main__":
    sys.exit(main())
```

### `main.py`

Simple entry point:

```python
#!/usr/bin/env python3
"""Main entry point for the scraper."""

from {name}_scraper.cli import main

if __name__ == "__main__":
    main()
```

### `formatters/__init__.py`

Export all formatters:

```python
"""Output formatters."""

from .json_formatter import format_as_json
from .md_formatter import format_as_markdown
from .openapi_formatter import format_as_openapi

__all__ = ["format_as_json", "format_as_markdown", "format_as_openapi"]
```

## Configuration Files

### `pyproject.toml`

```toml
[project]
name = "{name}-scraper"
version = "0.1.0"
description = "API documentation scraper for {Name}"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.27",
    "selectolax>=0.3",
    "pydantic>=2.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
]

[project.scripts]
{name}-scraper = "{name}_scraper.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"
```

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
*.egg-info/

# Output
output/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

### `README.md`

```markdown
# {Name} API Scraper

Scrapes API documentation from {source} and outputs JSON, Markdown, and OpenAPI formats.

## Installation

```bash
uv venv
uv pip install -e .
```

## Usage

```bash
# List available sections
python main.py --list-sections

# Scrape specific section
python main.py --section users --verbose

# Scrape all sections
python main.py --all --verbose

# Output specific format
python main.py --section users --format openapi
```

## Output

Generated files are written to `output/`:

- `*_api.json` - Structured JSON
- `*_api.md` - Human-readable Markdown
- `*_openapi.yaml` - OpenAPI 3.0 specification
```

## Output Organization

### Single Section

When scraping one section:

```
output/
├── section_api.json
├── section_api.md
└── section_openapi.yaml
```

### All Sections

When scraping all:

```
output/
├── users/
│   ├── users_api.json
│   ├── users_api.md
│   └── users_openapi.yaml
├── recipes/
│   └── ...
└── connections/
    └── ...
```

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Package | `{source}_scraper` | `workato_scraper` |
| Module | lowercase_snake | `parser.py` |
| Class | PascalCase | `APIDocumentation` |
| Function | lowercase_snake | `parse_documentation` |
| Constant | UPPERCASE_SNAKE | `API_SECTIONS` |
