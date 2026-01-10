# Documentation Framework Signatures

How to identify common documentation frameworks from HTML structure.

## VuePress

**Signature elements:**
```html
<div id="app">
  <div class="theme-container">
    <div class="sidebar">...</div>
    <main class="page">
      <div class="theme-default-content content__default">
```

**Indicators:**
- `#app` root container
- Classes with `theme-` prefix
- `content__default` class on main content
- Vue.js hydration markers in HTML comments
- Sidebar with `sidebar-links` class

**Content patterns:**
- Clean semantic HTML in content area
- Markdown-rendered tables and code blocks
- Auto-generated heading IDs from text

## Docusaurus

**Signature elements:**
```html
<div id="__docusaurus">
  <nav class="navbar">...</nav>
  <div class="main-wrapper">
    <aside class="theme-doc-sidebar-container">
    <main class="docMainContainer">
      <article>
        <div class="markdown">
```

**Indicators:**
- `#__docusaurus` root
- `theme-doc-` class prefix
- `markdown` class on content
- Meta tags with `docusaurus` generator

**Content patterns:**
- MDX support (React components in markdown)
- Admonitions with `admonition` class
- Code blocks with title bars

## ReadMe.io

**Signature elements:**
```html
<div class="rm-Article">
  <div class="rm-Markdown">
```

**Indicators:**
- Classes with `rm-` prefix
- Hosted on `readme.io` or custom domain with ReadMe patterns
- Interactive API explorer sections
- `readme-variable` elements for templating

**Content patterns:**
- Two-column layout (docs + code samples)
- Collapsible sections
- Try-it-now API widgets

## GitBook

**Signature elements:**
```html
<div class="gitbook-root">
  <div class="css-*"> <!-- CSS-in-JS class names -->
```

**Indicators:**
- CSS-in-JS generated class names (random strings)
- Heavy JavaScript hydration
- `gitbook` in meta tags or scripts

**Content patterns:**
- Block-based content structure
- Embedded code playgrounds
- Version selector in header

## Swagger UI / ReDoc

**Signature elements (Swagger UI):**
```html
<div id="swagger-ui">
  <div class="swagger-ui">
    <div class="opblock opblock-get">
```

**Signature elements (ReDoc):**
```html
<div id="redoc">
  <div class="menu-content">
  <div class="api-content">
```

**Indicators:**
- OpenAPI-driven structure
- Operation blocks with method classes
- Schema definitions inline
- Try-it-out functionality

## MkDocs / Material for MkDocs

**Signature elements:**
```html
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav class="wy-nav-side">
    <section class="wy-nav-content-wrap">
```

**Material for MkDocs:**
```html
<body class="md-content" data-md-color-scheme="default">
  <header class="md-header">
  <main class="md-main">
    <div class="md-content">
```

**Indicators:**
- `wy-` class prefix (Read the Docs theme)
- `md-` class prefix (Material theme)
- MkDocs-specific meta tags

## Sphinx

**Signature elements:**
```html
<div class="document">
  <div class="documentwrapper">
    <div class="bodywrapper">
      <div class="body">
```

**Indicators:**
- `documentwrapper`/`bodywrapper` structure
- `sphinxsidebar` class
- `.rst` extension in source links
- Sphinx generator meta tag

## Custom/Unknown

When framework is not identifiable:

1. Look for consistent patterns in:
   - Class naming conventions
   - Content wrapper structure
   - Navigation layout

2. Check meta tags:
   ```html
   <meta name="generator" content="...">
   ```

3. Check for framework-specific scripts:
   ```html
   <script src="...vuepress..."></script>
   <script src="...docusaurus..."></script>
   ```

4. Proceed with generic analysis:
   - Focus on semantic HTML elements
   - Look for main content containers
   - Identify heading and table patterns

## Framework Impact on Parsing

| Framework | Heading IDs | Tables | Code Blocks | Special Considerations |
|-----------|-------------|--------|-------------|----------------------|
| VuePress | Auto from text | Standard HTML | Fenced with lang | Clean, predictable |
| Docusaurus | Auto from text | Standard HTML | With title bars | MDX may add components |
| ReadMe.io | Generated | Custom styles | Interactive | Two-column layout |
| GitBook | Random CSS classes | Custom | Custom | Heavy JS, may need wait |
| Swagger/ReDoc | Operation IDs | Schema tables | JSON/YAML | Structured from OpenAPI |
| MkDocs | Auto from text | Standard HTML | Standard | Admonitions |
| Sphinx | Auto from text | RST-style | RST-style | Different structure |
