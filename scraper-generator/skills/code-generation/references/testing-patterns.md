# Testing Patterns for Scrapers

Approaches for testing generated scrapers.

## Testing Philosophy

Scrapers are challenging to test because:
1. HTML source can change without notice
2. Network requests are slow and unreliable
3. Edge cases are discovered in production

Focus on:
- Unit tests for parsing logic
- Integration tests with cached HTML
- Validation of output formats

## Unit Testing

### Parse Function Tests

```python
import pytest
from selectolax.parser import HTMLParser
from my_scraper.parser import extract_parameters

def test_extract_parameters_basic():
    """Test parameter extraction from simple table."""
    html = """
    <table>
        <tr><th>Name</th><th>Type</th><th>Description</th></tr>
        <tr><td>id</td><td>integer</td><td>User ID</td></tr>
    </table>
    """
    tree = HTMLParser(html)
    table = tree.css_first("table")

    params = extract_parameters(table)

    assert len(params) == 1
    assert params[0].name == "id"
    assert params[0].type == "integer"

def test_extract_parameters_with_required():
    """Test required parameter detection."""
    html = """
    <table>
        <tr><th>Name</th><th>Type</th><th>Required</th></tr>
        <tr><td>name</td><td>string</td><td>yes</td></tr>
        <tr><td>email</td><td>string</td><td>no</td></tr>
    </table>
    """
    tree = HTMLParser(html)
    table = tree.css_first("table")

    params = extract_parameters(table)

    assert params[0].required is True
    assert params[1].required is False

def test_extract_parameters_empty_table():
    """Test handling of empty table."""
    html = "<table></table>"
    tree = HTMLParser(html)
    table = tree.css_first("table")

    params = extract_parameters(table)

    assert params == []
```

### Edge Case Tests

```python
def test_extract_method_with_badge():
    """Test method extraction from styled badge."""
    html = '<td><span class="badge">POST</span></td>'
    tree = HTMLParser(html)
    cell = tree.css_first("td")

    method = extract_method(cell)

    assert method == "POST"

def test_extract_path_with_anchor():
    """Test path and anchor ID extraction."""
    html = '<td><a href="#create-user">/api/users</a></td>'
    tree = HTMLParser(html)
    cell = tree.css_first("td")

    path, anchor_id = extract_path(cell)

    assert path == "/api/users"
    assert anchor_id == "create-user"

def test_extract_path_with_full_url():
    """Test anchor extraction from full URL."""
    html = '<td><a href="/api/users.html#create-user">/api/users</a></td>'
    tree = HTMLParser(html)
    cell = tree.css_first("td")

    path, anchor_id = extract_path(cell)

    assert anchor_id == "create-user"
```

### Regex Pattern Tests

```python
@pytest.mark.parametrize("path,expected", [
    ("/api/users", False),
    ("/api/users/123", True),
    ("/api/users/:id", False),
    ("/api/users/123/posts", True),
    ("/api/users/:id/posts/:post_id", False),
])
def test_is_example_path(path, expected):
    """Test example path detection."""
    assert is_example_path(path) == expected

@pytest.mark.parametrize("text,expected_method,expected_path", [
    ("GET /api/users", "GET", "/api/users"),
    ("POST /api/users/:id", "POST", "/api/users/:id"),
    ("DELETE /api/items/{id}", "DELETE", "/api/items/{id}"),
])
def test_endpoint_pattern(text, expected_method, expected_path):
    """Test endpoint pattern matching."""
    match = ENDPOINT_PATTERN.match(text)
    assert match is not None
    assert match.group(1) == expected_method
    assert match.group(2) == expected_path
```

## Integration Testing

### Using Cached HTML

```python
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_parse_users_section():
    """Test parsing of cached users section."""
    html = (FIXTURES_DIR / "users.html").read_text()

    doc = parse_documentation(html, "users")

    assert doc.metadata.section_id == "users"
    assert len(doc.endpoints) >= 5  # Expected number
    assert any(e.path == "/api/users" for e in doc.endpoints)

def test_all_endpoints_have_method():
    """Verify all endpoints have valid methods."""
    html = (FIXTURES_DIR / "users.html").read_text()
    doc = parse_documentation(html, "users")

    for ep in doc.endpoints:
        assert ep.method in {"GET", "POST", "PUT", "PATCH", "DELETE"}
```

### Snapshot Testing

```python
import json

def test_json_output_matches_snapshot(snapshot):
    """Compare JSON output to saved snapshot."""
    html = (FIXTURES_DIR / "users.html").read_text()
    doc = parse_documentation(html, "users")
    output = doc.model_dump_json(indent=2)

    snapshot.assert_match(output, "users_api.json")
```

## Output Validation

### OpenAPI Validation

```python
import subprocess

def test_openapi_validates():
    """Verify generated OpenAPI spec is valid."""
    html = (FIXTURES_DIR / "users.html").read_text()
    doc = parse_documentation(html, "users")
    spec = format_as_openapi(doc)

    # Write temp file
    spec_file = Path("temp_spec.yaml")
    spec_file.write_text(spec)

    try:
        result = subprocess.run(
            ["npx", "@openapitools/openapi-generator-cli", "validate",
             "-i", str(spec_file)],
            capture_output=True,
            text=True
        )
        assert "No validation issues" in result.stdout
    finally:
        spec_file.unlink()
```

### JSON Schema Validation

```python
from pydantic import ValidationError

def test_output_matches_schema():
    """Verify output matches expected schema."""
    html = (FIXTURES_DIR / "users.html").read_text()
    doc = parse_documentation(html, "users")

    # Re-validate through Pydantic
    try:
        APIDocumentation.model_validate(doc.model_dump())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e}")
```

## Test Fixtures

### Creating Fixtures

```python
def save_fixture(section_id: str):
    """Fetch and save HTML fixture for testing."""
    html = fetch_html(get_section_url(section_id))

    fixture_path = FIXTURES_DIR / f"{section_id}.html"
    fixture_path.write_text(html)
    print(f"Saved fixture to {fixture_path}")
```

### Fixture Structure

```
tests/
├── fixtures/
│   ├── users.html
│   ├── recipes.html
│   └── connections.html
├── test_parser.py
├── test_formatters.py
└── test_integration.py
```

## Continuous Testing

### pytest Configuration

```toml
# pyproject.toml

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### Test Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=my_scraper --cov-report=term-missing

# Run specific test file
pytest tests/test_parser.py

# Run tests matching pattern
pytest -k "test_extract"
```

## Validation Script

```bash
#!/usr/bin/env bash
# scripts/validate-scraper.sh

set -euo pipefail

SCRAPER_NAME="${1:?Usage: validate-scraper.sh <scraper_name>}"
OUTPUT_DIR="output"

echo "=== Validating $SCRAPER_NAME scraper ==="

# 1. Check package structure
echo "Checking package structure..."
required_files=(
    "${SCRAPER_NAME}_scraper/__init__.py"
    "${SCRAPER_NAME}_scraper/models.py"
    "${SCRAPER_NAME}_scraper/parser.py"
    "${SCRAPER_NAME}_scraper/scraper.py"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "ERROR: Missing $file"
        exit 1
    fi
done
echo "✓ Package structure OK"

# 2. Run scraper on sample section
echo "Running scraper..."
python main.py --section users --output-dir "$OUTPUT_DIR" --verbose

# 3. Validate JSON output
echo "Validating JSON output..."
python -c "import json; json.load(open('$OUTPUT_DIR/users_api.json'))"
echo "✓ JSON valid"

# 4. Validate OpenAPI output
echo "Validating OpenAPI spec..."
npx @openapitools/openapi-generator-cli validate -i "$OUTPUT_DIR/users_openapi.yaml"
echo "✓ OpenAPI valid"

# 5. Check endpoint count
endpoint_count=$(python -c "
import json
doc = json.load(open('$OUTPUT_DIR/users_api.json'))
print(len(doc['endpoints']))
")
echo "Found $endpoint_count endpoints"

if [[ "$endpoint_count" -lt 1 ]]; then
    echo "ERROR: No endpoints extracted"
    exit 1
fi

echo "=== Validation complete ==="
```
