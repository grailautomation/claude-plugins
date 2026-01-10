# Extraction Strategies

Different approaches for extracting API documentation content based on discovered patterns.

## Index Extraction Strategies

### Strategy: Quick Reference Table

**When to use:** Page has a summary table listing all endpoints with methods and paths.

**Approach:**
1. Find table by structure (columns contain method-like values)
2. Identify columns by header text or position
3. For each row:
   - Extract HTTP method (normalize to uppercase)
   - Extract path from text or link
   - Extract anchor ID from link href
   - Extract description

**CSS pattern:**
```python
table = tree.css_first("table")
for row in table.css("tr"):
    cells = row.css("td")
    if len(cells) >= 3:
        method = cells[0].text(strip=True).upper()
        path_link = cells[1].css_first("a")
        anchor_id = path_link.attributes.get("href", "").lstrip("#")
        path = path_link.text(strip=True)
        description = cells[2].text(strip=True)
```

**Edge cases:**
- Some tables have thead/tbody, others don't
- Method might be in a badge span, not plain text
- Links may include full URL, not just anchor

### Strategy: Sidebar Navigation

**When to use:** Endpoints listed in sidebar menu, not in content.

**Approach:**
1. Find sidebar container
2. Identify endpoint links (contain method patterns or path patterns)
3. Extract from link text and href

**CSS pattern:**
```python
sidebar = tree.css_first("nav.sidebar, aside.sidebar, .sidebar")
for link in sidebar.css("a"):
    href = link.attributes.get("href", "")
    text = link.text(strip=True)
    # Parse method and path from text
```

### Strategy: Heading Scan

**When to use:** No explicit index; headings themselves list endpoints.

**Approach:**
1. Find all H2/H3 headings
2. Filter to those matching endpoint patterns
3. Extract method and path from heading text

**Pattern matching:**
```python
import re
endpoint_pattern = re.compile(
    r"(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)",
    re.IGNORECASE
)
for heading in tree.css("h2, h3"):
    text = heading.text(strip=True)
    match = endpoint_pattern.search(text)
    if match:
        method, path = match.groups()
```

## Section Extraction Strategies

### Strategy: Anchor ID Lookup

**When to use:** Index provides anchor IDs that match heading IDs.

**Approach:**
1. Use anchor ID from index
2. Find heading with matching ID
3. Collect content until next same-level heading

**Implementation:**
```python
def find_section(tree, anchor_id):
    heading = tree.css_first(f'[id="{anchor_id}"]')
    if not heading:
        return None

    content = []
    sibling = heading.next
    heading_tag = heading.tag

    while sibling:
        if sibling.tag == heading_tag:
            break  # Next section starts
        content.append(sibling)
        sibling = sibling.next

    return content
```

**Edge cases:**
- ID may be on wrapper div, not heading itself
- Generated IDs may differ from expected pattern
- Some pages use h2, others h3

### Strategy: Text Matching

**When to use:** Anchor IDs don't exist or don't match.

**Approach:**
1. Search headings for text containing method + path
2. Or search for description text
3. Apply fuzzy matching if needed

**Implementation:**
```python
def find_by_text(tree, method, path, description):
    # Strategy 1: Method + Path in heading
    for h in tree.css("h2, h3"):
        text = h.text(strip=True).upper()
        if method in text and path in text:
            return h

    # Strategy 2: Description match
    for h in tree.css("h2, h3"):
        text = h.text(strip=True).lower()
        if description.lower() in text:
            return h

    return None
```

### Strategy: Sequential Traversal

**When to use:** Content flows sequentially without clear section markers.

**Approach:**
1. Find first content element (table, code block)
2. Traverse backwards to find section start
3. Traverse forwards to find section end

## Content Extraction Strategies

### Strategy: Parameter Tables

**Approach:**
1. Within section, find tables with parameter-like structure
2. Identify column semantics from headers
3. Extract each parameter as structured data

**Column detection:**
```python
def identify_columns(headers):
    columns = {}
    for i, h in enumerate(headers):
        text = h.lower()
        if "name" in text or "parameter" in text:
            columns["name"] = i
        elif "type" in text:
            columns["type"] = i
        elif "required" in text:
            columns["required"] = i
        elif "description" in text or "desc" in text:
            columns["description"] = i
    return columns
```

### Strategy: Code Block Classification

**Approach:**
1. Find code blocks within section
2. Classify by language hint or content pattern
3. Associate with request/response role

**Classification:**
```python
def classify_code_block(element):
    # Check language class
    classes = element.attributes.get("class", "")
    if "json" in classes:
        return "json"
    if "curl" in classes or "bash" in classes:
        return "curl"

    # Check content pattern
    text = element.text(strip=True)
    if text.startswith("{") or text.startswith("["):
        return "json"
    if text.startswith("curl"):
        return "curl"

    return "unknown"

def determine_role(code_block, section_context):
    """Is this a request body or response example?"""
    # Check preceding text
    prev_text = get_preceding_text(code_block)
    if "request" in prev_text.lower():
        return "request"
    if "response" in prev_text.lower():
        return "response"

    # For POST/PUT, first JSON is usually request
    # For GET, JSON is usually response
    return infer_from_method(section_context)
```

### Strategy: Description Extraction

**Approach:**
1. Find paragraph elements between heading and first table/code
2. Concatenate text content
3. Strip boilerplate phrases

```python
def extract_description(section_heading):
    description_parts = []
    sibling = section_heading.next

    while sibling:
        if sibling.tag in ["table", "pre", "h2", "h3"]:
            break
        if sibling.tag == "p":
            description_parts.append(sibling.text(strip=True))
        sibling = sibling.next

    return " ".join(description_parts)
```

## Error Handling Strategies

### Missing Content

When expected content is missing:
1. Log the gap for documentation
2. Provide sensible defaults
3. Continue extraction (don't fail completely)

### Format Variations

When format differs from expected:
1. Try alternative patterns
2. Fall back to less structured extraction
3. Flag as needing manual review

### Malformed HTML

When HTML is invalid:
1. Use lenient parser (selectolax handles this well)
2. Try CSS selector alternatives
3. Fall back to text pattern matching
