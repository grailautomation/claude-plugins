# Doc Site Analysis Skill

When analyzing an API documentation page to understand its structure and extraction patterns, follow this systematic approach.

## Core Objective

Your goal is to discover how a documentation site organizes its API reference content so you can later write code to extract that content deterministically. You're not extracting data now—you're discovering the patterns that will inform scraper code generation.

## Phase 1: Initial Reconnaissance

Fetch the target URL and observe the raw HTML structure. Look for:

1. **Page framework signatures** - Most doc sites use static site generators with distinctive patterns
2. **Content organization** - How is the page divided into sections?
3. **Navigation structure** - Sidebar, breadcrumbs, table of contents
4. **Endpoint listing patterns** - Tables, lists, or inline definitions

Document your observations before proceeding. The goal is to understand the "shape" of the documentation.

## Phase 2: Identify the Index Pattern

API documentation typically provides an index of available endpoints. Common patterns:

### Quick Reference Tables
Look for tables with columns like Method/Resource/Description or similar. These are gold—they give you a complete list of endpoints in structured form.

```html
<table>
  <tr><th>Type</th><th>Resource</th><th>Description</th></tr>
  <tr>
    <td>GET</td>
    <td><a href="#get-connection">connections/:connection_id</a></td>
    <td>Get connection details</td>
  </tr>
</table>
```

Key signals:
- Table has HTTP method column (GET, POST, PUT, DELETE, PATCH)
- Links contain anchor fragments (`#heading-id`) pointing to detail sections
- Resource column contains URL paths with parameters

### Sidebar Navigation
Some sites list endpoints in the sidebar. Look for:
- Nested lists under section headings
- Links to anchors or separate pages
- HTTP method badges or prefixes

### Section Headings as Index
When no explicit index exists, the headings themselves form the index:
- H2/H3 elements containing method + path patterns
- Pattern: "GET /api/users" or "List Users (GET)"

## Phase 3: Map Section Boundaries

Once you know where endpoints are listed, understand how detail sections are organized:

1. **Heading-based sections** - Each endpoint gets an H2/H3, content until next heading belongs to it
2. **Container-based sections** - Each endpoint wrapped in a div with class or ID
3. **Flat structure** - All content flows sequentially, headings are the only markers

For heading-based sections (most common), note:
- The heading level used (H2, H3)
- Whether headings have IDs (essential for anchor linking)
- The pattern in heading text (method first? path first? description?)

## Phase 4: Locate Content Elements

Within each endpoint section, identify where to find:

### Parameters
Usually in tables with columns: Name, Type, Required, Description
```html
<table>
  <tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr>
  <tr><td>id</td><td>integer</td><td>yes</td><td>User ID</td></tr>
</table>
```

Look for section subheadings like "Request Parameters", "Query Parameters", "Body Parameters"

### Request/Response Examples
Code blocks with language hints:
```html
<pre><code class="language-json">{"name": "example"}</code></pre>
<pre><code class="language-curl">curl -X GET ...</code></pre>
```

Or syntax-highlighted divs:
```html
<div class="highlight-json"><pre>...</pre></div>
```

### Descriptions
Prose paragraphs between the heading and first table/code block. May contain important context about authentication, rate limits, or special behavior.

## Phase 5: Detect Edge Cases

Real documentation has inconsistencies. Look for:

1. **Broken anchor links** - Index links that don't match heading IDs
2. **Multiple table formats** - Different pages may use different table structures
3. **Nested content** - Examples inside collapsible sections or tabs
4. **Generated IDs** - Headings without explicit IDs, where browser generates them from text

Document any patterns that differ from the main structure.

## Output: Site Analysis Document

After analysis, produce a structured document containing:

```yaml
site:
  name: "Workato API Documentation"
  base_url: "https://docs.workato.com"
  framework: "VuePress"  # or Docusaurus, ReadMe, custom, unknown

index_pattern:
  type: "quick_reference_table"  # or sidebar, headings, list
  location: "top of page"
  columns: ["Type", "Resource", "Description"]
  link_column: "Resource"
  anchor_format: "#heading-id"

section_pattern:
  type: "heading_based"
  heading_level: "h2"
  id_source: "explicit"  # or generated
  text_format: "{description}"  # e.g., "Get connection details"

content_elements:
  parameters:
    type: "table"
    columns: ["Name", "Type", "Required", "Description"]

  request_examples:
    type: "code_block"
    languages: ["curl", "json"]
    container: "pre > code"

  response_examples:
    type: "code_block"
    languages: ["json"]
    container: "div.highlight-json pre"

edge_cases:
  - "First endpoint in some pages has broken anchor link"
  - "Some tables use 'Required?' instead of 'Required'"
```

This structured output becomes the input for scraper code generation.

## Reference Materials

For detailed information on specific topics:

- `references/html-patterns.md` - Common HTML structures for tables, code blocks, navigation
- `references/framework-signatures.md` - How to identify VuePress, Docusaurus, ReadMe, etc.
- `references/extraction-strategies.md` - Parsing approaches for different patterns

For a worked example:

- `examples/workato-analysis.md` - Complete analysis of Workato API documentation
