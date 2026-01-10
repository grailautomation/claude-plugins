# Code Generation Skill

When generating Python code for an API documentation scraper, follow these patterns and best practices.

## Core Objective

Write clean, maintainable Python code that reliably extracts API documentation from HTML. The code should be:

1. **Robust** - Handle edge cases and malformed HTML
2. **Readable** - Clear logic that can be understood and modified
3. **Type-safe** - Full type annotations for IDE support and validation
4. **Testable** - Pure functions where possible

## Library Choices

### HTTP Requests: httpx

Use httpx for modern async-capable HTTP:

```python
import httpx

def fetch_html(url: str) -> str:
    """Fetch HTML content from URL with error handling."""
    response = httpx.get(
        url,
        timeout=30.0,
        follow_redirects=True,
        headers={"User-Agent": "API-Doc-Scraper/1.0"}
    )
    response.raise_for_status()
    return response.text
```

For retries, use tenacity:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_with_retry(url: str) -> str:
    return fetch_html(url)
```

### HTML Parsing: selectolax

Use selectolax for fast CSS selector-based parsing:

```python
from selectolax.parser import HTMLParser, Node

def parse_page(html: str) -> HTMLParser:
    """Parse HTML content."""
    return HTMLParser(html)
```

Key selectolax patterns:

```python
# Single element
element = tree.css_first("selector")

# Multiple elements
elements = tree.css("selector")

# Text content
text = element.text(strip=True)

# Attribute access
href = element.attributes.get("href", "")

# Safe navigation
if element and element.next:
    sibling = element.next
```

### Data Models: Pydantic

Use Pydantic v2 for validated data structures:

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Parameter(BaseModel):
    """API endpoint parameter."""
    name: str
    type: str = "string"
    required: bool = False
    description: str = ""
    location: str = "query"
```

## Code Patterns

### Multi-Strategy Extraction

Use multiple fallback strategies for reliability:

```python
def extract_endpoints(tree: HTMLParser) -> list[Endpoint]:
    """Extract endpoints using multiple strategies."""
    endpoints: list[Endpoint] = []
    seen: set[tuple[str, str]] = set()  # Dedup by (method, path)

    # Strategy 1: Quick reference tables (most reliable)
    endpoints.extend(extract_from_tables(tree, seen))

    # Strategy 2: Section headings
    endpoints.extend(extract_from_headings(tree, seen))

    # Strategy 3: Code examples (last resort)
    if not endpoints:
        endpoints.extend(extract_from_code(tree, seen))

    return endpoints
```

### Safe Text Extraction

Always handle None and missing content:

```python
def clean_text(node: Node | None) -> str:
    """Extract and clean text from node."""
    if not node:
        return ""
    raw = node.text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', raw).strip()

def get_attribute(node: Node, attr: str) -> str:
    """Safely get attribute value."""
    if not node:
        return ""
    return node.attributes.get(attr) or ""
```

### Table Parsing

Generic table-to-dict conversion:

```python
def parse_table(table: Node) -> list[dict[str, str]]:
    """Convert HTML table to list of dictionaries."""
    headers = [
        th.text(strip=True).lower()
        for th in table.css("th")
    ]

    if not headers:
        return []

    rows = []
    for tr in table.css("tr")[1:]:  # Skip header
        cells = tr.css("td")
        if len(cells) == len(headers):
            row = {
                headers[i]: cells[i].text(strip=True)
                for i in range(len(headers))
            }
            rows.append(row)

    return rows
```

### Section Boundary Detection

Collect content until next heading:

```python
def get_section_content(heading: Node) -> list[Node]:
    """Get all content nodes until next same-level heading."""
    content: list[Node] = []
    sibling = heading.next
    heading_level = heading.tag  # "h2", "h3", etc.

    while sibling:
        # Stop at same or higher level heading
        if sibling.tag in ["h1", "h2", "h3"] and sibling.tag <= heading_level:
            break
        content.append(sibling)
        sibling = sibling.next

    return content
```

### Regex Patterns

Common patterns for API docs:

```python
import re

# HTTP method + path in text
ENDPOINT_PATTERN = re.compile(
    r"(GET|POST|PUT|PATCH|DELETE)\s+(/\S+)",
    re.IGNORECASE
)

# Path parameters
PATH_PARAM_PATTERN = re.compile(r":(\w+)|\{(\w+)\}")

# Example path detection (has numeric IDs)
EXAMPLE_PATH_PATTERN = re.compile(r"/\d+(?:/|$)")

# Rate limit patterns
RATE_LIMIT_PATTERN = re.compile(
    r"(\d+)\s*requests?\s*per\s*(minute|second|hour)",
    re.IGNORECASE
)
```

## Error Handling

### Defensive Extraction

Never let one failure stop the whole scrape:

```python
def extract_all_endpoints(tree: HTMLParser) -> list[Endpoint]:
    endpoints = []

    for table in tree.css("table"):
        try:
            eps = extract_from_table(table)
            endpoints.extend(eps)
        except Exception as e:
            logger.warning(f"Failed to parse table: {e}")
            continue  # Try next table

    return endpoints
```

### Validation with Warnings

Report issues without failing:

```python
def validate_endpoint(ep: Endpoint) -> list[str]:
    """Return list of validation warnings."""
    warnings = []

    if not ep.description:
        warnings.append(f"{ep.method} {ep.path}: no description")

    if not ep.examples:
        warnings.append(f"{ep.method} {ep.path}: no examples")

    if not ep.parameters and ep.method in ["POST", "PUT"]:
        warnings.append(f"{ep.method} {ep.path}: no body parameters")

    return warnings
```

## Type Annotations

### Function Signatures

Always annotate parameters and return types:

```python
def parse_documentation(
    html: str,
    section_id: str,
    *,
    strict: bool = False
) -> APIDocumentation:
    """Parse HTML into structured documentation.

    Args:
        html: Raw HTML content
        section_id: Section identifier
        strict: Raise on validation errors

    Returns:
        Parsed API documentation
    """
    ...
```

### Generic Types

Use modern Python 3.12+ syntax:

```python
# Instead of typing.List, typing.Dict
endpoints: list[Endpoint] = []
headers: dict[str, str] = {}
seen: set[tuple[str, str]] = set()

# Optional with | None
def find_heading(tree: HTMLParser, id: str) -> Node | None:
    return tree.css_first(f'[id="{id}"]')
```

## Code Organization

### Function Size

Keep functions focused (under 30 lines typically):

```python
# Good: Single responsibility
def extract_method(cell: Node) -> str:
    """Extract HTTP method from table cell."""
    text = cell.text(strip=True).upper()
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        if method in text:
            return method
    return ""

def extract_path(cell: Node) -> tuple[str, str]:
    """Extract path and anchor ID from table cell."""
    anchor = cell.css_first("a")
    if anchor:
        href = anchor.attributes.get("href") or ""
        anchor_id = href.split("#")[-1] if "#" in href else ""
        return anchor.text(strip=True), anchor_id
    return cell.text(strip=True), ""
```

### Helper Modules

Group related helpers:

```python
# utils.py
def clean_text(node: Node | None) -> str: ...
def safe_int(text: str, default: int = 0) -> int: ...
def normalize_type(type_str: str) -> str: ...

# patterns.py
ENDPOINT_RE = re.compile(...)
PATH_PARAM_RE = re.compile(...)
def is_example_path(path: str) -> bool: ...
```

## Reference Materials

For detailed information:

- `references/python-patterns.md` - Python idioms for scraping
- `references/error-handling.md` - Robust error handling patterns
- `references/testing-patterns.md` - Testing scrapers

For validation:

- `scripts/validate-scraper.sh` - Test generated scraper
