# ARIA Snapshots

ARIA snapshots provide an accessibility-tree view of a page, returning a YAML-formatted structure with interactive element references. Use them to discover page elements without knowing CSS selectors in advance.

## When to Use Snapshots

| Approach | When to Use |
|----------|-------------|
| **ARIA Snapshot** | Unknown page layout, need to discover elements |
| **CSS Selectors** | Local/source-available sites where you can read the HTML |
| **Screenshots** | Visual verification, seeing what the user sees |

Use snapshots as the default discovery mechanism for unfamiliar pages. Once you've identified elements via their refs, you can interact with them directly.

## Getting a Snapshot

```typescript
const snapshot = await client.getAISnapshot("page-name");
console.log(snapshot);
```

This returns a YAML-formatted accessibility tree of the page body:

```yaml
- banner:
  - link "Hacker News" [ref=e1]
  - navigation:
    - link "new" [ref=e2]
    - link "past" [ref=e3]
    - link "comments" [ref=e4]
- main:
  - list:
    - listitem:
      - link "Show HN: My Project" [ref=e8]
      - text: "(example.com)"
      - link "328 comments" [ref=e9]
- contentinfo:
  - textbox [ref=e10]:
    - /placeholder: "Search"
```

## Understanding Refs

Refs are assigned to **visible, interactive elements** only. Each ref is a stable identifier for that element until the next snapshot call.

### Ref Format

- `[ref=eN]` — Element reference ID (e.g., `e1`, `e15`, `e203`)

### State Attributes

- `[checked]` — Checkbox/radio is checked
- `[checked=mixed]` — Indeterminate state
- `[disabled]` — Element is disabled
- `[expanded]` — Expandable element is open
- `[active]` — Element has focus
- `[level=N]` — Heading level (1-6)
- `[pressed]` — Toggle button is pressed
- `[selected]` — Option/tab is selected
- `[cursor=pointer]` — Element has pointer cursor (clickable)

### Properties

- `/url:` — Link href value
- `/placeholder:` — Input placeholder text

## Interacting with Refs

After getting a snapshot, use `selectSnapshotRef()` to get a Playwright `ElementHandle`:

```typescript
const snapshot = await client.getAISnapshot("mypage");
console.log(snapshot); // Find the ref you need

// Click a link
const link = await client.selectSnapshotRef("mypage", "e8");
await link.click();

// Type into a textbox
const searchBox = await client.selectSnapshotRef("mypage", "e10");
await searchBox.fill("search query");

// Read text from an element
const element = await client.selectSnapshotRef("mypage", "e5");
const text = await element.textContent();
```

## The Discover-Then-Interact Pattern

For unfamiliar pages, follow this workflow:

### Step 1: Navigate and snapshot

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("explore");
await page.goto("https://example.com");
await waitForPageLoad(page);

const snapshot = await client.getAISnapshot("explore");
console.log(snapshot);
await client.disconnect();
```

### Step 2: Identify the target element from the snapshot output

Read the YAML tree to find the element you need. Look for recognizable names, roles, and structure.

### Step 3: Interact with the ref

```typescript
import { connect } from "@/client.js";

const client = await connect();
const element = await client.selectSnapshotRef("explore", "e15");
await element.click();

// Take a screenshot to verify
const page = await client.page("explore");
await page.screenshot({ path: "tmp/after-click.png" });
await client.disconnect();
```

### Step 4: Re-snapshot if the page changed

After interactions that change the page (clicks, navigation, form submissions), take a new snapshot to discover the updated element tree.

## Ref Persistence

Refs are stored on `window.__devBrowserRefs` in the browser context. They persist across Playwright CDP reconnections (when your script disconnects and a new script connects to the same page). However, refs are invalidated when you call `getAISnapshot()` again — the new snapshot assigns fresh refs.

## Roles Reference

Common roles you'll see in snapshots:

| Role | HTML Elements |
|------|--------------|
| `link` | `<a href>` |
| `button` | `<button>`, `<input type="submit">` |
| `textbox` | `<input type="text">`, `<textarea>` |
| `checkbox` | `<input type="checkbox">` |
| `radio` | `<input type="radio">` |
| `combobox` | `<select>`, `<input>` with datalist |
| `heading` | `<h1>`–`<h6>` |
| `list` | `<ul>`, `<ol>` |
| `listitem` | `<li>` |
| `navigation` | `<nav>` |
| `banner` | `<header>` (top-level) |
| `contentinfo` | `<footer>` (top-level) |
| `main` | `<main>` |
| `table` | `<table>` |
| `row` | `<tr>` |
| `cell` | `<td>` |
| `img` | `<img>` with alt text |
| `generic` | `<div>`, `<span>` (with accessible attributes) |
