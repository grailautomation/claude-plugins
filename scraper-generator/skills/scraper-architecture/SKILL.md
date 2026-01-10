# Scraper Architecture Skill

When designing an API documentation scraper, follow this architectural guidance to create a maintainable, well-structured codebase.

## Core Objective

Design a scraper that transforms HTML documentation into structured data. The scraper should:

1. Fetch HTML content reliably
2. Parse content into structured models
3. Output in multiple useful formats
4. Handle edge cases gracefully

## Project Structure

A well-organized scraper follows this layout:

```
{name}_scraper/
├── __init__.py           # Package exports
├── models.py             # Pydantic data models
├── scraper.py            # HTTP fetching logic
├── parser.py             # HTML parsing and extraction
├── sections.py           # Section registry (if multi-page)
├── cli.py                # Command-line interface
└── formatters/
    ├── __init__.py
    ├── json_formatter.py
    ├── md_formatter.py
    └── openapi_formatter.py
```

### Responsibilities

| File | Purpose |
|------|---------|
| `models.py` | Data structures representing API documentation |
| `scraper.py` | HTTP requests with retries and error handling |
| `parser.py` | HTML to model transformation logic |
| `sections.py` | Map of sections/pages to scrape |
| `cli.py` | User interface and orchestration |
| `formatters/` | Model to output format transformations |

## Data Models

### Core Models

Design models that capture the essential structure of API documentation:

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Parameter(BaseModel):
    """API endpoint parameter."""
    name: str
    type: str = "string"
    required: bool = False
    description: str = ""
    location: str = "query"  # "query", "path", or "body"

class Example(BaseModel):
    """Request or response example."""
    title: str = ""
    code: str
    language: str = "json"

class Endpoint(BaseModel):
    """API endpoint documentation."""
    method: str              # GET, POST, PUT, DELETE, PATCH
    path: str                # /api/users/:id
    description: str = ""
    parameters: list[Parameter] = Field(default_factory=list)
    request_body: dict | None = None
    response: dict | None = None
    examples: list[Example] = Field(default_factory=list)
    rate_limit: str | None = None
    notes: list[str] = Field(default_factory=list)

class APIDocumentation(BaseModel):
    """Complete API documentation structure."""
    metadata: Metadata
    authentication: Authentication
    rate_limits: dict[str, str] = Field(default_factory=dict)
    endpoints: list[Endpoint] = Field(default_factory=list)
```

### Design Principles

1. **Use Pydantic** - Validation, serialization, and clear structure
2. **Default to optional** - Real docs have gaps; handle gracefully
3. **Flatten where possible** - Avoid deep nesting unless semantically meaningful
4. **Include metadata** - Source URL, scrape time, section info

## Parser Architecture

### Separation of Concerns

The parser should have clear phases:

```python
def parse_documentation(html: str, section_id: str) -> APIDocumentation:
    """Main entry point - orchestrates parsing."""
    tree = HTMLParser(html)

    metadata = _extract_metadata(tree, section_id)
    authentication = _extract_authentication(tree)
    rate_limits = _extract_rate_limits(tree)
    endpoints = _extract_endpoints(tree)

    return APIDocumentation(
        metadata=metadata,
        authentication=authentication,
        rate_limits=rate_limits,
        endpoints=endpoints,
    )
```

### Multi-Strategy Extraction

Real documentation is inconsistent. Use fallback strategies:

```python
def _extract_endpoints(tree: HTMLParser) -> list[Endpoint]:
    """Extract all endpoints using multiple strategies."""
    endpoints = []
    seen = set()  # Dedup by (method, path)

    # Strategy 1: Quick reference tables (most reliable)
    endpoints.extend(_extract_from_reference_table(tree, seen))

    # Strategy 2: Section headings with method patterns
    endpoints.extend(_extract_from_headings(tree, seen))

    # Strategy 3: Curl examples (last resort)
    if not endpoints:
        endpoints.extend(_extract_from_curl_examples(tree, seen))

    return endpoints
```

### Section Boundary Detection

When content flows sequentially under headings:

```python
def _get_section_content(heading: Node) -> list[Node]:
    """Collect all nodes until next same-level heading."""
    content = []
    sibling = heading.next

    while sibling:
        # Stop at next heading of same or higher level
        if sibling.tag in ["h1", "h2", "h3"] and sibling.tag <= heading.tag:
            break
        content.append(sibling)
        sibling = sibling.next

    return content
```

## Formatter Architecture

### Interface Pattern

Each formatter takes a model and returns formatted output:

```python
def format_as_json(doc: APIDocumentation) -> str:
    """Convert to JSON string."""
    return doc.model_dump_json(indent=2)

def format_as_markdown(doc: APIDocumentation) -> str:
    """Convert to Markdown documentation."""
    lines = [f"# {doc.metadata.title}", ""]
    # ... build markdown structure
    return "\n".join(lines)

def format_as_openapi(doc: APIDocumentation) -> str:
    """Convert to OpenAPI 3.0 YAML."""
    spec = _build_openapi_spec(doc)
    return yaml.dump(spec, sort_keys=False)
```

### OpenAPI Considerations

When generating OpenAPI specs:

1. **Infer path parameters** from `:param` or `{param}` patterns
2. **Generate operationIds** from method + path (e.g., `getUser`, `listUsers`)
3. **Include server definitions** for all environments
4. **Preserve rate limits** as `x-rate-limits` extension

## CLI Design

### Argparse Pattern

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Scrape API documentation")
    parser.add_argument("--section", default="all", help="Section to scrape")
    parser.add_argument("--format", choices=["json", "markdown", "openapi", "all"],
                       default="all", help="Output format")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--list-sections", action="store_true",
                       help="List available sections")

    args = parser.parse_args()
    # ... orchestrate scraping
```

### Output Organization

For single section:
```
output/
├── section_api.json
├── section_api.md
└── section_openapi.yaml
```

For all sections:
```
output/
├── section1/
│   ├── section1_api.json
│   ├── section1_api.md
│   └── section1_openapi.yaml
└── section2/
    └── ...
```

## Error Handling

### HTTP Errors

Use retries with exponential backoff:

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_html(url: str) -> str:
    response = httpx.get(url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    return response.text
```

### Parsing Errors

Be defensive, don't fail completely:

```python
def _extract_parameters(section: Node) -> list[Parameter]:
    """Extract parameters, returning empty list on failure."""
    try:
        # parsing logic
    except Exception as e:
        logger.warning(f"Failed to extract parameters: {e}")
        return []
```

### Validation

After extraction, validate completeness:

```python
def validate_endpoints(endpoints: list[Endpoint]) -> list[str]:
    """Return list of validation warnings."""
    warnings = []
    for ep in endpoints:
        if not ep.description:
            warnings.append(f"{ep.method} {ep.path}: missing description")
        if not ep.examples:
            warnings.append(f"{ep.method} {ep.path}: no examples found")
    return warnings
```

## Reference Materials

For detailed information on specific topics:

- `references/data-models.md` - Complete model reference
- `references/parser-patterns.md` - CSS selector strategies
- `references/formatter-patterns.md` - Output format conventions
- `references/project-structure.md` - Full project layout

For a working example:

- `examples/README.md` - Links to the `workato_scraper` reference implementation on GitHub
