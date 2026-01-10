# HTML Patterns in API Documentation

Common HTML structures found in API documentation and how to identify them.

## Tables

### Parameter Tables
Most common structure for API parameters:

```html
<!-- Standard 4-column layout -->
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>integer</td>
      <td>yes</td>
      <td>The unique identifier</td>
    </tr>
  </tbody>
</table>
```

Variations:
- Required column may be "Required?" or omitted (assume optional)
- Type column may include format hints: "integer (int64)"
- Some use `<code>` tags around parameter names
- Description may contain nested elements (links, code spans)

### Quick Reference Tables
Index tables listing all endpoints:

```html
<table>
  <tr>
    <th>Type</th>
    <th>Resource</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td><a href="#list-users">/api/users</a></td>
    <td>List all users</td>
  </tr>
</table>
```

Key extraction points:
- HTTP method from first column (normalize: GET, POST, PUT, DELETE, PATCH)
- Path from link text or second column
- Anchor ID from href attribute (strip leading #)
- Description from last column

## Code Blocks

### Language-Annotated Blocks
Modern documentation uses fenced code blocks with language hints:

```html
<pre><code class="language-json">
{
  "id": 123,
  "name": "Example"
}
</code></pre>
```

Common class patterns:
- `language-{lang}` - Standard markdown rendering
- `highlight-{lang}` - Some SSGs
- `lang-{lang}` - Alternative
- `{lang}` - Simple class name

### Syntax Highlighted Blocks
Many sites pre-render syntax highlighting:

```html
<div class="highlight highlight-json">
  <pre>
    <span class="p">{</span>
    <span class="s2">"id"</span>
    <span class="p">:</span>
    <span class="mi">123</span>
    <span class="p">}</span>
  </pre>
</div>
```

To extract content, get `.text_content()` to strip span tags.

### Curl Examples
Curl blocks contain valuable request structure:

```html
<pre><code class="language-bash">
curl -X POST 'https://api.example.com/users' \
  -H 'Authorization: Bearer token' \
  -H 'Content-Type: application/json' \
  -d '{"name": "New User"}'
</code></pre>
```

Parse for:
- HTTP method after `-X`
- URL (may include path parameters)
- Headers after `-H`
- Request body after `-d` or `--data`

## Headings

### ID Patterns
Headings with explicit IDs:

```html
<h2 id="get-user-details">Get user details</h2>
```

Auto-generated IDs (from heading text):
- Lowercase
- Spaces to hyphens
- Special characters removed
- "Get User Details" → "get-user-details"

### Method in Heading
Some docs include HTTP method in heading:

```html
<h2 id="get-users">GET /api/users</h2>
<h3>GET List Users</h3>
<h2>List Users <span class="method">GET</span></h2>
```

## Navigation Elements

### Sidebar Structure
```html
<nav class="sidebar">
  <ul>
    <li class="section">
      <span>Users</span>
      <ul>
        <li><a href="#list-users">List users</a></li>
        <li><a href="#get-user">Get user</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

### Breadcrumbs
```html
<nav class="breadcrumb">
  <a href="/docs">Docs</a> >
  <a href="/docs/api">API Reference</a> >
  <span>Users</span>
</nav>
```

### Table of Contents
```html
<div class="toc">
  <h4>On this page</h4>
  <ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#endpoints">Endpoints</a></li>
  </ul>
</div>
```

## Content Wrappers

### Main Content Area
Identify the main content to avoid nav/footer noise:

```html
<main class="content">...</main>
<div class="markdown-body">...</div>
<article class="documentation">...</article>
<div id="content">...</div>
```

### Section Containers
Some sites wrap each endpoint in a container:

```html
<section class="endpoint" id="get-users">
  <h2>Get Users</h2>
  <p>Description...</p>
  <h3>Parameters</h3>
  <table>...</table>
</section>
```

## Special Elements

### Method Badges
```html
<span class="method method-get">GET</span>
<span class="badge badge-post">POST</span>
<code class="http-method">DELETE</code>
```

### Required Indicators
```html
<span class="required">*</span>
<span class="required-badge">Required</span>
<td>yes</td>
<td class="required">true</td>
```

### Collapsible Sections
```html
<details>
  <summary>Show example response</summary>
  <pre><code>...</code></pre>
</details>
```

### Tabs
```html
<div class="tabs">
  <button class="tab active" data-tab="curl">cURL</button>
  <button class="tab" data-tab="python">Python</button>
</div>
<div class="tab-content" id="curl">...</div>
<div class="tab-content hidden" id="python">...</div>
```
