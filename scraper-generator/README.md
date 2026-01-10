# Scraper Generator

A Claude Code plugin that automates the creation of API documentation scrapers.

## What It Does

Given an API documentation URL, this plugin guides Claude through:

1. **Analyzing** the documentation site structure and patterns
2. **Designing** a scraper architecture tailored to that structure
3. **Generating** a complete Python scraper package
4. **Validating** the generated code works correctly

The result is a standalone scraper that runs forever without AI assistance.

## Usage

```
/create-scraper https://docs.example.com/api/users.html
```

This generates a complete Python scraper package similar to the [workato_scraper reference implementation](https://github.com/kreitter/workato-api-docs/tree/main/workato_scraper).

## Components

### Skills

| Skill | Purpose |
|-------|---------|
| `doc-site-analysis` | How to analyze API documentation structure |
| `scraper-architecture` | How to design scraper components |
| `code-generation` | How to write Python scraper code |

### Agents

| Agent | Role |
|-------|------|
| `site-analyzer` | Discovers documentation structure |
| `code-generator` | Writes the Python code |
| `scraper-validator` | Tests generated scraper |

### Commands

| Command | Description |
|---------|-------------|
| `/create-scraper <url>` | Generate a scraper for the given documentation URL |

## Output

The plugin generates a complete Python package:

```
{name}_scraper/
├── __init__.py
├── models.py         # Pydantic data models
├── scraper.py        # HTTP fetching
├── parser.py         # HTML parsing
├── sections.py       # Section registry
├── cli.py            # Command-line interface
└── formatters/       # JSON, Markdown, OpenAPI output
```

## Installation

Add this plugin via the Claude Code marketplace or install directly:

```bash
claude plugins install kreitter/scraper-generator
```

## License

MIT
