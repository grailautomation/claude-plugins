# Reference Implementation Pattern

The `workato_scraper` pattern is a complete scraper layout generated using the patterns documented in this skill. Study its structure:

```
workato_scraper/
├── __init__.py           # Package exports
├── models.py             # Pydantic data models
├── scraper.py            # HTTP fetching with retries
├── parser.py             # HTML parsing logic
├── sections.py           # API section registry
├── cli.py                # Command-line interface
└── formatters/           # Output formatters (JSON, Markdown, OpenAPI)
```

When generating a new scraper, use this structure as the template and adapt the parser strategies for the target documentation site.
