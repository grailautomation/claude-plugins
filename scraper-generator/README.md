# Scraper Generator

A Claude Code and Codex plugin that automates the creation of API
documentation scrapers.

## What It Does

Given an API documentation URL, this plugin guides Claude Code or Codex through:

1. **Analyzing** the documentation site structure and patterns
2. **Designing** a scraper architecture tailored to that structure
3. **Generating** a complete Python scraper package
4. **Validating** the generated code works correctly

The result is a standalone scraper that runs forever without AI assistance.

## Usage

### Claude Code

```
/scraper-generator:create-scraper https://docs.example.com/api/users.html
```

This generates a complete Python scraper package using the patterns documented in the bundled scraper architecture references.

### Codex

Install the plugin from the repo-local Grail Automation Codex marketplace, then
ask Codex to use `create-scraper` with a documentation URL and output
directory. Codex runs the same phases inline with local shell/file tools instead
of Claude `Task` subagents.

## Components

### Skills

| Skill | Purpose |
|-------|---------|
| `doc-site-analysis` | How to analyze API documentation structure |
| `scraper-architecture` | How to design scraper components |
| `code-generation` | How to write Python scraper code |

### Agents

Claude Code can use these subagents. Codex uses the skills and references
directly unless the user explicitly authorizes Codex subagents.

| Agent | Role |
|-------|------|
| `site-analyzer` | Discovers documentation structure |
| `code-generator` | Writes the Python code |
| `scraper-validator` | Tests generated scraper |

### Commands

| Command | Description |
|---------|-------------|
| `/scraper-generator:create-scraper <url>` | Generate a scraper for the given documentation URL |

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
claude plugin install scraper-generator@grail-automation
```

For Codex, the repository marketplace exposes this plugin through
`.agents/plugins/marketplace.json`.

## License

MIT
