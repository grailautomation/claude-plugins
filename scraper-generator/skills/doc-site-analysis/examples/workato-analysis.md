# Workato API Documentation Analysis

This document captures the patterns discovered while building the Workato API documentation scraper.

## Site Overview

```yaml
site:
  name: "Workato API Documentation"
  base_url: "https://docs.workato.com"
  framework: "VuePress"
  section_count: 28
  total_endpoints: 206
```

## Framework Identification

**VuePress signatures found:**
- `<div id="app">` root container
- `class="theme-default-content content__default"` on main content
- Clean semantic HTML with auto-generated heading IDs
- Sidebar navigation in `.sidebar-links`

## Index Pattern: Quick Reference Tables

Workato uses summary tables at the top of each API section page.

### Table Structure

```html
<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Resource</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GET</td>
      <td><a href="#get-connection-details">connections/:id</a></td>
      <td>Get connection details by ID</td>
    </tr>
  </tbody>
</table>
```

### Key Observations

1. **Columns are consistent:** Type, Resource, Description
2. **Links contain anchor fragments:** `href="#heading-id"` pointing to detail sections
3. **Paths use colon notation:** `:id` for path parameters (not `{id}`)
4. **Some links include full URL:** `/workato-api/team.html#invite-collaborator`

### Extraction Logic

```python
# Column identification by header text
headers = [th.text(strip=True).lower() for th in table.css("th")]
has_type = any(h in ["type", "method"] for h in headers)
has_resource = any(h in ["resource", "path", "endpoint"] for h in headers)

# Anchor ID extraction
anchor = cell.css_first("a")
href = anchor.attributes.get("href") or ""
if href.startswith("#"):
    anchor_id = href[1:]
elif "#" in href:
    anchor_id = href.split("#")[1]
```

## Section Pattern: Heading-Based

Each endpoint has an H2 heading with a unique ID. Content flows until the next H2.

### Heading Structure

```html
<h2 id="get-connection-details">Get connection details</h2>
<p>Returns details about a specific connection...</p>
<h3>Request</h3>
<table><!-- parameters --></table>
<h3>Response</h3>
<pre><code class="language-json">...</code></pre>
```

### Section Finding Strategies

The scraper uses multiple strategies in priority order:

1. **Anchor ID lookup** (most reliable)
   ```python
   heading = tree.css_first(f'[id="{anchor_id}"]')
   ```

2. **Method + Path match** (fallback)
   ```python
   for heading in tree.css("h2, h3"):
       text = heading.text(strip=True)
       if method in text.upper() and path in text:
           return heading
   ```

3. **Description match** (last resort)
   - Extract first verb from description
   - Match to heading text
   - e.g., "Returns connection details" matches heading "Get connection details"

### Known Edge Cases

1. **Broken anchor links:** Some table links don't have anchor fragments
   - Example: `POST /api/sdk/generate_schema/csv` has href without `#`
   - Mitigation: Fall back to text matching strategies

2. **Description verb mismatch:** Table says "Returns..." but heading says "Get..."
   - The anchor ID strategy solves this completely

## Parameter Tables

### Structure

```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>connection_id</td>
      <td>integer</td>
      <td>The connection ID to retrieve</td>
    </tr>
  </tbody>
</table>
```

### Variations Observed

1. **Required column:** Sometimes present, sometimes not
   - When absent, check description for "required" keyword

2. **Type formats:**
   - `string`
   - `integer`
   - `array of strings`
   - `object` (with nested description)

3. **Path vs Query vs Body parameters:**
   - Path params: Identified by matching `:param` in endpoint path
   - Query params: Usually for GET endpoints
   - Body params: Usually for POST/PUT endpoints

### Detection Logic

```python
path_param_names = {match.group(1) for match in re.finditer(r":(\w+)", path)}

for param in extracted_params:
    if param.name in path_param_names:
        param.location = "path"
    elif method == "GET":
        param.location = "query"
    else:
        param.location = "body"
```

## Code Examples

### Languages Found

1. **curl** - Request examples
2. **json** - Request/response bodies
3. **ruby** (occasional) - SDK examples

### Block Structure

```html
<pre><code class="language-json">
{
  "id": 123,
  "name": "Production DB"
}
</code></pre>
```

### Request vs Response Classification

1. Check preceding heading/text for "Request"/"Response" keywords
2. For POST/PUT: First JSON block is usually request body
3. For GET: JSON blocks are usually response examples
4. curl blocks are always request examples

## Rate Limits

Found in dedicated tables or inline text:

```html
<table>
  <tr><th>Endpoint</th><th>Rate limit</th></tr>
  <tr><td>Default</td><td>10,000 per minute</td></tr>
</table>
```

Or as text pattern:
```
"Rate limit: 10000 requests per minute"
```

## Discovered Challenges

### 1. Example Paths in Tables

Some pages include example URLs with numeric IDs that should be excluded:

```python
def _is_example_path(path: str) -> bool:
    """Filter out example-specific URLs."""
    # Skip paths that are clearly examples with numeric IDs
    if re.search(r'/\d+(?:/|$)', path):
        # But allow generic :id patterns
        if ':' not in path and '{' not in path:
            return True
    return False
```

### 2. HTTP Status Codes vs Parameters

Response status tables look similar to parameter tables:

```html
<table>
  <tr><th>Status</th><th>Description</th></tr>
  <tr><td>200</td><td>Success</td></tr>
  <tr><td>404</td><td>Not found</td></tr>
</table>
```

Detection:
```python
def _is_http_status_code(text: str) -> bool:
    if text.isdigit() and 100 <= int(text) <= 599:
        return True
    # Also check common status names
    return text.lower() in {"not found", "unauthorized", "forbidden"}
```

### 3. Multiple Tables Per Section

Some endpoints have:
1. Path parameters table
2. Query parameters table
3. Request body fields table
4. Response fields table

Solution: Check surrounding context (H3 headings, preceding text) to classify tables.

## Summary: Workato Pattern Profile

| Aspect | Pattern |
|--------|---------|
| Framework | VuePress |
| Index | Quick reference table with Type/Resource/Description |
| Links | Anchor fragments to H2 headings |
| Path params | Colon notation (`:id`) |
| Sections | H2-bounded, sequential content |
| Parameters | Tables with Name/Type/Description columns |
| Examples | Fenced code blocks with language hints |
| Rate limits | Dedicated tables or text patterns |

## Files in Reference Implementation

See `examples/workato_scraper/` for the complete implementation:

- `parser.py` - Main parsing logic with all strategies
- `models.py` - Pydantic data models
- `scraper.py` - HTTP fetching with retry logic
- `sections.py` - Registry of 28 API sections
- `formatters/` - JSON, Markdown, OpenAPI output
