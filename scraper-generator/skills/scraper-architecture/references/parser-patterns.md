# Parser Patterns Reference

CSS selector strategies and parsing patterns for HTML extraction.

## Parser Library: selectolax

Selectolax is the recommended parser for performance and ease of use.

```python
from selectolax.parser import HTMLParser, Node

tree = HTMLParser(html_content)
```

### Key Methods

```python
# Select single element (returns first match or None)
element = tree.css_first("selector")

# Select all matching elements
elements = tree.css("selector")

# Get text content
text = element.text(strip=True)
text = element.text(separator=" ", strip=True)  # With whitespace normalization

# Get attribute
href = element.attributes.get("href", "")

# Get raw HTML
html = element.html

# Navigate DOM
parent = element.parent
sibling = element.next
children = element.iter()
```

## Common Selectors

### Tables

```python
# Find all tables
tree.css("table")

# Find table with specific class
tree.css_first("table.parameters")

# Get header cells
table.css("th")

# Get body rows (skip header)
table.css("tr")[1:]  # or table.css("tbody tr")

# Get cells in a row
row.css("td")
```

### Headings

```python
# All level-2 headings
tree.css("h2")

# Headings with ID
tree.css("h2[id]")

# Specific heading by ID
tree.css_first('[id="get-users"]')

# Headings containing text (manual filter)
[h for h in tree.css("h2") if "GET" in h.text()]
```

### Code Blocks

```python
# Fenced code blocks
tree.css("pre code")

# Language-specific blocks
tree.css('code[class*="language-json"]')
tree.css('code.language-curl')

# Highlighted containers
tree.css("div.highlight pre")
```

### Links

```python
# All links
tree.css("a")

# Links with anchors
tree.css('a[href^="#"]')

# Links in specific container
tree.css(".sidebar a")
```

## Extraction Patterns

### Table to Dictionary

```python
def table_to_dicts(table: Node) -> list[dict]:
    """Convert HTML table to list of dictionaries."""
    headers = [th.text(strip=True).lower() for th in table.css("th")]
    rows = []

    for tr in table.css("tr")[1:]:  # Skip header row
        cells = tr.css("td")
        if len(cells) == len(headers):
            row = {headers[i]: cells[i].text(strip=True) for i in range(len(headers))}
            rows.append(row)

    return rows
```

### Section Content Collection

```python
def get_section_content(heading: Node) -> list[Node]:
    """Collect nodes until next same-level heading."""
    content = []
    sibling = heading.next
    tag = heading.tag  # e.g., "h2"

    while sibling:
        if sibling.tag == tag:
            break
        content.append(sibling)
        sibling = sibling.next

    return content
```

### Find by Text Pattern

```python
import re

def find_heading_by_pattern(tree: HTMLParser, pattern: str) -> Node | None:
    """Find heading matching regex pattern."""
    regex = re.compile(pattern, re.IGNORECASE)
    for heading in tree.css("h2, h3"):
        if regex.search(heading.text(strip=True)):
            return heading
    return None

# Example: Find "GET /api/users" headings
heading = find_heading_by_pattern(tree, r"GET\s+/api/users")
```

### Extract Preceding Text

```python
def get_text_before(element: Node) -> str:
    """Get text content between previous heading and this element."""
    texts = []
    sibling = element.previous

    while sibling:
        if sibling.tag in ["h1", "h2", "h3", "h4"]:
            break
        if sibling.tag == "p":
            texts.insert(0, sibling.text(strip=True))
        sibling = sibling.previous

    return " ".join(texts)
```

## Error Handling

### Safe Attribute Access

```python
# Bad: may throw if attribute doesn't exist
href = element.attributes["href"]

# Good: returns None or default
href = element.attributes.get("href", "")

# Extra safe: handle None values
href = element.attributes.get("href") or ""
```

### Safe Text Extraction

```python
def safe_text(node: Node | None) -> str:
    """Get text from node, or empty string if None."""
    return node.text(strip=True) if node else ""
```

### Safe Selection

```python
def safe_first(tree: HTMLParser, selector: str) -> Node | None:
    """Select first element or None."""
    try:
        return tree.css_first(selector)
    except Exception:
        return None
```

## Performance Tips

### Narrow Selections

```python
# Slower: searches whole document
tree.css("td a")

# Faster: search within specific section
section = tree.css_first(".api-reference")
if section:
    section.css("td a")
```

### Avoid Repeated Parsing

```python
# Bad: parses table multiple times
headers = table.css("th")
rows = table.css("tr")
cells = table.css("td")

# Good: single iteration
for row in table.css("tr"):
    if row.css("th"):  # Header row
        headers = [th.text(strip=True) for th in row.css("th")]
    else:
        cells = row.css("td")
```

### Use css_first for Single Results

```python
# Wasteful: returns list, takes first
elements = tree.css("#unique-id")
element = elements[0] if elements else None

# Better: returns single element or None
element = tree.css_first("#unique-id")
```

## Debugging

### Print Element Structure

```python
def debug_element(element: Node):
    print(f"Tag: {element.tag}")
    print(f"ID: {element.attributes.get('id')}")
    print(f"Classes: {element.attributes.get('class')}")
    print(f"Text: {element.text(strip=True)[:100]}")
    print(f"HTML: {element.html[:200]}")
```

### Dump All Tables

```python
def list_tables(tree: HTMLParser):
    for i, table in enumerate(tree.css("table")):
        headers = [th.text(strip=True) for th in table.css("th")]
        row_count = len(table.css("tr")) - 1
        print(f"Table {i}: {headers}, {row_count} rows")
```
