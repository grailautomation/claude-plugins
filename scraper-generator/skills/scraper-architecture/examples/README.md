# Reference Implementation

The `workato_scraper` reference implementation is available at:

**GitHub:** https://github.com/kreitter/workato-api-docs/tree/main/workato_scraper

This is a complete, working example of a scraper generated using the patterns documented in this skill. Study its structure:

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

When generating a new scraper, use this as your template and adapt the patterns for the target documentation structure.
