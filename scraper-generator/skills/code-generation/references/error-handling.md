# Error Handling Patterns

Robust error handling strategies for documentation scrapers.

## Philosophy

1. **Don't fail completely** - Extract what you can
2. **Report issues clearly** - Log warnings for manual review
3. **Provide fallbacks** - Alternative strategies when primary fails
4. **Validate output** - Check completeness after extraction

## HTTP Errors

### Retry with Backoff

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import httpx

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))
)
def fetch_html(url: str) -> str:
    """Fetch URL with automatic retry."""
    response = httpx.get(url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    return response.text
```

### Graceful Degradation

```python
def fetch_all_sections(section_ids: list[str]) -> dict[str, str | None]:
    """Fetch all sections, continuing on failure."""
    results = {}

    for section_id in section_ids:
        try:
            results[section_id] = fetch_html(get_url(section_id))
        except Exception as e:
            logger.error(f"Failed to fetch {section_id}: {e}")
            results[section_id] = None
            # Continue with next section

    return results
```

## Parsing Errors

### Safe Element Access

```python
def safe_text(node: Node | None) -> str:
    """Get text from node or empty string."""
    if node is None:
        return ""
    try:
        return node.text(strip=True)
    except Exception:
        return ""

def safe_attr(node: Node | None, attr: str) -> str:
    """Get attribute from node or empty string."""
    if node is None:
        return ""
    try:
        return node.attributes.get(attr) or ""
    except Exception:
        return ""
```

### Defensive Table Parsing

```python
def parse_parameter_table(table: Node) -> list[Parameter]:
    """Parse parameter table with error handling."""
    parameters = []

    try:
        headers = [th.text(strip=True).lower() for th in table.css("th")]
    except Exception as e:
        logger.warning(f"Failed to extract headers: {e}")
        return []

    for row in table.css("tr")[1:]:
        try:
            cells = row.css("td")
            if len(cells) < 2:
                continue

            param = extract_parameter(cells, headers)
            if param:
                parameters.append(param)

        except Exception as e:
            logger.debug(f"Failed to parse row: {e}")
            continue

    return parameters
```

### Strategy Fallback

```python
def find_endpoint_section(
    tree: HTMLParser,
    method: str,
    path: str,
    description: str = "",
    anchor_id: str = ""
) -> Node | None:
    """Find section using multiple strategies."""

    # Strategy 1: Direct anchor ID lookup
    if anchor_id:
        try:
            heading = tree.css_first(f'[id="{anchor_id}"]')
            if heading:
                return heading
        except Exception:
            pass  # Try next strategy

    # Strategy 2: Method + path in heading
    try:
        for h in tree.css("h2, h3"):
            text = h.text(strip=True)
            if method in text.upper() and path in text:
                return h
    except Exception:
        pass

    # Strategy 3: Description match
    if description:
        try:
            first_word = description.split()[0].lower().rstrip('s')
            for h in tree.css("h2, h3"):
                if h.text(strip=True).lower().startswith(first_word):
                    return h
        except Exception:
            pass

    return None
```

## Validation Errors

### Validation Result Pattern

```python
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Container for validation results."""
    valid: bool
    errors: list[str]
    warnings: list[str]

def validate_endpoint(ep: Endpoint) -> ValidationResult:
    """Validate endpoint completeness."""
    errors = []
    warnings = []

    # Required fields
    if not ep.path.startswith("/"):
        errors.append(f"Path must start with /: {ep.path}")

    if ep.method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        errors.append(f"Invalid method: {ep.method}")

    # Recommended fields
    if not ep.description:
        warnings.append("Missing description")

    if not ep.examples:
        warnings.append("No examples found")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

### Aggregate Validation

```python
def validate_documentation(doc: APIDocumentation) -> ValidationResult:
    """Validate entire documentation."""
    all_errors = []
    all_warnings = []

    # Check metadata
    if not doc.metadata.source_url:
        all_errors.append("Missing source URL")

    # Check endpoints
    for ep in doc.endpoints:
        result = validate_endpoint(ep)
        if result.errors:
            prefix = f"{ep.method} {ep.path}: "
            all_errors.extend(prefix + e for e in result.errors)
        if result.warnings:
            prefix = f"{ep.method} {ep.path}: "
            all_warnings.extend(prefix + w for w in result.warnings)

    return ValidationResult(
        valid=len(all_errors) == 0,
        errors=all_errors,
        warnings=all_warnings
    )
```

## Logging Best Practices

### Log Levels

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Internal details
logger.debug(f"Checking table with headers: {headers}")

# INFO: Normal progress
logger.info(f"Found {len(endpoints)} endpoints in {section_id}")

# WARNING: Something unexpected but recoverable
logger.warning(f"No examples found for {endpoint.path}")

# ERROR: Something failed
logger.error(f"Failed to parse {section_id}: {e}")
```

### Structured Logging

```python
def log_extraction_result(section_id: str, doc: APIDocumentation):
    """Log extraction summary."""
    logger.info(
        f"Extracted {section_id}",
        extra={
            "section": section_id,
            "endpoint_count": len(doc.endpoints),
            "with_examples": sum(1 for e in doc.endpoints if e.examples),
            "with_params": sum(1 for e in doc.endpoints if e.parameters),
        }
    )
```

## Error Recovery

### Cache for Recovery

```python
import json
from pathlib import Path

CACHE_DIR = Path(".cache")

def cache_html(section_id: str, html: str):
    """Cache fetched HTML for debugging."""
    CACHE_DIR.mkdir(exist_ok=True)
    (CACHE_DIR / f"{section_id}.html").write_text(html)

def load_cached(section_id: str) -> str | None:
    """Load cached HTML if available."""
    cache_file = CACHE_DIR / f"{section_id}.html"
    if cache_file.exists():
        return cache_file.read_text()
    return None
```

### Checkpoint Progress

```python
def scrape_all_with_checkpoints(sections: list[str], output_dir: Path):
    """Scrape all sections, saving progress."""
    progress_file = output_dir / ".progress.json"

    # Load existing progress
    if progress_file.exists():
        completed = set(json.loads(progress_file.read_text()))
    else:
        completed = set()

    for section in sections:
        if section in completed:
            logger.info(f"Skipping {section} (already done)")
            continue

        try:
            process_section(section, output_dir)
            completed.add(section)
            progress_file.write_text(json.dumps(list(completed)))
        except Exception as e:
            logger.error(f"Failed {section}: {e}")
            # Don't add to completed, will retry next run
```

## Exception Hierarchy

```python
class ScraperError(Exception):
    """Base exception for scraper errors."""
    pass

class FetchError(ScraperError):
    """Error fetching content."""
    def __init__(self, url: str, cause: Exception):
        self.url = url
        self.cause = cause
        super().__init__(f"Failed to fetch {url}: {cause}")

class ParseError(ScraperError):
    """Error parsing content."""
    def __init__(self, section: str, cause: Exception):
        self.section = section
        self.cause = cause
        super().__init__(f"Failed to parse {section}: {cause}")

class ValidationError(ScraperError):
    """Content validation failed."""
    def __init__(self, issues: list[str]):
        self.issues = issues
        super().__init__(f"Validation failed: {', '.join(issues)}")
```
