# Python Patterns for Scrapers

Idiomatic Python patterns for documentation scraping.

## Import Organization

```python
"""Module docstring."""

# Standard library
import re
from datetime import datetime
from pathlib import Path

# Third-party
import httpx
import yaml
from pydantic import BaseModel, Field
from selectolax.parser import HTMLParser, Node

# Local
from .models import APIDocumentation, Endpoint
from .sections import API_SECTIONS
```

## Data Classes with Pydantic

### Basic Model

```python
class Parameter(BaseModel):
    """API parameter with validation."""
    name: str
    type: str = "string"
    required: bool = False
    description: str = ""
    location: str = "query"

    def __str__(self) -> str:
        req = "*" if self.required else ""
        return f"{self.name}{req}: {self.type}"
```

### Model with Factory Defaults

```python
class Endpoint(BaseModel):
    """API endpoint."""
    method: str
    path: str
    description: str = ""
    parameters: list[Parameter] = Field(default_factory=list)
    examples: list[Example] = Field(default_factory=list)
```

### Model with Computed Properties

```python
class Endpoint(BaseModel):
    method: str
    path: str

    @property
    def path_params(self) -> list[str]:
        """Extract path parameter names."""
        return re.findall(r":(\w+)|\{(\w+)\}", self.path)

    @property
    def operation_id(self) -> str:
        """Generate OpenAPI operationId."""
        path_clean = re.sub(r"[/:{}]", "_", self.path)
        return f"{self.method.lower()}{path_clean}".replace("__", "_")
```

## Dictionary and List Patterns

### Defaultdict for Grouping

```python
from collections import defaultdict

def group_by_method(endpoints: list[Endpoint]) -> dict[str, list[Endpoint]]:
    """Group endpoints by HTTP method."""
    grouped: dict[str, list[Endpoint]] = defaultdict(list)
    for ep in endpoints:
        grouped[ep.method].append(ep)
    return dict(grouped)
```

### Dictionary Comprehension

```python
# Section ID to URL mapping
urls = {sid: f"{BASE_URL}/{sid}.html" for sid in sections}

# Filter valid endpoints
valid = {(ep.method, ep.path): ep for ep in endpoints if ep.path.startswith("/")}
```

### List Comprehension with Filter

```python
# Get required parameters
required = [p for p in endpoint.parameters if p.required]

# Get JSON examples only
json_examples = [ex for ex in endpoint.examples if ex.language == "json"]

# Flatten nested lists
all_params = [p for ep in endpoints for p in ep.parameters]
```

## String Patterns

### F-strings

```python
# Basic interpolation
path = f"/api/{section_id}/endpoints"

# Expression in f-string
status = f"Found {len(endpoints)} endpoint{'s' if len(endpoints) != 1 else ''}"

# Alignment
for ep in endpoints:
    print(f"{ep.method:6} {ep.path}")
```

### Multiline Strings

```python
# Template strings
template = """
# {title}

## Authentication
{auth_description}

## Endpoints
{endpoint_list}
""".strip()

content = template.format(
    title=doc.metadata.title,
    auth_description=doc.authentication.description,
    endpoint_list=render_endpoints(doc.endpoints)
)
```

### String Cleaning

```python
def clean_text(text: str) -> str:
    """Normalize whitespace in text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing
    text = text.strip()
    return text

def slugify(text: str) -> str:
    """Convert to URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text
```

## Iteration Patterns

### Enumerate with Start

```python
for i, endpoint in enumerate(endpoints, start=1):
    print(f"{i}. {endpoint.method} {endpoint.path}")
```

### Zip for Parallel Iteration

```python
headers = ["Name", "Type", "Required"]
cells = [name_cell, type_cell, req_cell]

for header, cell in zip(headers, cells):
    print(f"{header}: {cell.text(strip=True)}")
```

### Iterate with Look-ahead

```python
def process_with_next(items: list[Node]):
    """Process items knowing what comes next."""
    for i, item in enumerate(items):
        next_item = items[i + 1] if i + 1 < len(items) else None
        process(item, next_item)
```

## Function Patterns

### Early Return

```python
def extract_anchor_id(cell: Node) -> str:
    """Extract anchor ID from link in cell."""
    anchor = cell.css_first("a")
    if not anchor:
        return ""

    href = anchor.attributes.get("href") or ""
    if not href:
        return ""

    if "#" not in href:
        return ""

    return href.split("#")[-1]
```

### Guard Clauses

```python
def parse_table(table: Node) -> list[dict]:
    """Parse table into list of dicts."""
    # Guard: need headers
    headers = table.css("th")
    if not headers:
        return []

    # Guard: need data rows
    rows = table.css("tr")[1:]
    if not rows:
        return []

    # Main logic
    return [row_to_dict(row, headers) for row in rows]
```

### Generator Functions

```python
def iter_endpoints(tree: HTMLParser):
    """Yield endpoints as they're discovered."""
    for table in tree.css("table.endpoints"):
        for row in table.css("tr")[1:]:
            endpoint = parse_row(row)
            if endpoint:
                yield endpoint
```

## Context Managers

### File Writing

```python
def write_output(content: str, path: Path) -> None:
    """Write content to file, creating directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
```

### Temporary State

```python
from contextlib import contextmanager

@contextmanager
def verbose_mode(scraper):
    """Temporarily enable verbose output."""
    old_verbose = scraper.verbose
    scraper.verbose = True
    try:
        yield
    finally:
        scraper.verbose = old_verbose
```

## Error Handling

### Try-Except with Specific Errors

```python
def fetch_section(section_id: str) -> str | None:
    """Fetch section HTML, returning None on failure."""
    try:
        return fetch_html(get_section_url(section_id))
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error for {section_id}: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request failed for {section_id}: {e}")
        return None
```

### Re-raising with Context

```python
def parse_section(section_id: str, html: str) -> APIDocumentation:
    """Parse section with enhanced error messages."""
    try:
        return parse_documentation(html, section_id)
    except Exception as e:
        raise ValueError(f"Failed to parse {section_id}: {e}") from e
```

## Logging

### Basic Setup

```python
import logging

logger = logging.getLogger(__name__)

def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )
```

### Usage

```python
logger.debug(f"Parsing table with {len(rows)} rows")
logger.info(f"Found {len(endpoints)} endpoints")
logger.warning(f"Missing description for {endpoint.path}")
logger.error(f"Failed to extract from {url}")
```

## Path Handling

```python
from pathlib import Path

# Build paths
output_dir = Path("output") / section_id
output_file = output_dir / f"{section_id}_api.json"

# Create directories
output_dir.mkdir(parents=True, exist_ok=True)

# Write file
output_file.write_text(content)

# Read file
html = Path("cached.html").read_text()
```
