---
name: dev-browser
description: Browser automation and scraping with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.
---

# Dev Browser

Browser automation that maintains page state across script executions. Write small, focused scripts to accomplish tasks incrementally.

## Setup

Two modes available. Ask the user if unclear which to use.

### Standalone Mode (Default)

Launches a new Chromium browser. Start the server and verify readiness:

```bash
cd skills/dev-browser && ./server.sh &

# Verify server is ready (poll HTTP endpoint — do NOT watch stdout)
for i in $(seq 1 30); do
  curl -s http://localhost:9222 > /dev/null 2>&1 && echo "Server ready" && break
  sleep 1
done
```

Add `--headless` to `./server.sh --headless &` for headless mode.

If the server is already running from a previous session, the curl check succeeds immediately — no restart needed.

### Extension Mode

Connects to the user's existing Chrome browser (preserving logged-in sessions):

```bash
cd skills/dev-browser && npm i && npm run start-extension &
```

Wait for `Extension connected` in the output. If the extension hasn't connected, tell the user to install it from: https://github.com/SawyerHood/dev-browser/releases

For detailed server lifecycle management, see [Server Management](references/server-management.md).

## Choosing Your Approach

- **Local/source-available sites**: Read the source code first to write selectors directly
- **Unknown page layouts**: Use `getAISnapshot()` to discover elements — see [ARIA Snapshots](references/aria-snapshots.md)
- **Visual feedback**: Take screenshots to see what the user sees

## Writing Scripts

> **Run all scripts from `skills/dev-browser/` directory.** The `@/` import alias requires this.

Execute scripts inline using heredocs:

```bash
cd skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("example", { viewport: { width: 1920, height: 1080 } });

await page.goto("https://example.com");
await waitForPageLoad(page);

console.log({ title: await page.title(), url: page.url() });
await client.disconnect();
EOF
```

Write to `tmp/` files only when the script needs reuse or is complex.

### Key Principles

1. **Small scripts**: Each script does ONE thing (navigate, click, fill, check)
2. **Evaluate state**: Log/return state at the end to decide next steps
3. **Descriptive page names**: Use `"checkout"`, `"login"`, not `"main"`
4. **Always disconnect**: `await client.disconnect()` — pages persist on server
5. **Plain JS in evaluate**: `page.evaluate()` runs in the browser — no TypeScript syntax

```typescript
// Correct: plain JavaScript in browser context
const text = await page.evaluate(() => {
  return document.body.innerText;
});

// Wrong: TypeScript syntax breaks at runtime
const text = await page.evaluate(() => {
  const el: HTMLElement = document.body; // Type annotation fails in browser!
  return el.innerText;
});
```

## Workflow Loop

Follow this pattern for complex tasks:

1. **Write a script** to perform one action
2. **Run it** and observe the output
3. **Evaluate** — did it work? What's the current state?
4. **Decide** — is the task complete or do we need another script?
5. **Repeat** until done

## Inspecting Page State

### Screenshots

```typescript
await page.screenshot({ path: "tmp/screenshot.png" });
await page.screenshot({ path: "tmp/full.png", fullPage: true });
```

### ARIA Snapshots

Use `getAISnapshot()` to discover page elements without knowing selectors. Returns a YAML accessibility tree with `[ref=eN]` markers for interactive elements:

```typescript
const snapshot = await client.getAISnapshot("mypage");
console.log(snapshot);

// Interact with a discovered element
const element = await client.selectSnapshotRef("mypage", "e5");
await element.click();
```

For the full guide on interpreting snapshots, refs, and the discover-then-interact pattern, see [ARIA Snapshots](references/aria-snapshots.md).

## Waiting

```typescript
import { waitForPageLoad } from "@/client.js";

await waitForPageLoad(page);                   // After navigation
await page.waitForSelector(".results");        // For specific elements
await page.waitForURL("**/success");           // For specific URL
```

## Error Recovery

Page state persists after failures. Debug with:

```bash
cd skills/dev-browser && npx tsx <<'EOF'
import { connect } from "@/client.js";

const client = await connect();
const page = await client.page("mypage");

await page.screenshot({ path: "tmp/debug.png" });
console.log({
  url: page.url(),
  title: await page.title(),
  bodyText: await page.textContent("body").then((t) => t?.slice(0, 200)),
});

await client.disconnect();
EOF
```

## Client API Quick Reference

```typescript
const client = await connect();

const page = await client.page("name");                    // Get or create page
const page = await client.page("name", { viewport: {} }); // With viewport
const pages = await client.list();                         // List all pages
await client.close("name");                                // Close a page
await client.disconnect();                                 // Disconnect (pages persist)

const snapshot = await client.getAISnapshot("name");       // Accessibility tree
const el = await client.selectSnapshotRef("name", "e5");   // Element by ref
const info = await client.getServerInfo();                 // Server mode info
```

The `page` object is a standard Playwright `Page`. For the full API reference with all parameters, return types, and options, see [Client API](references/client-api.md).

## Scraping

For large datasets (followers, posts, search results), intercept and replay network requests rather than scrolling the DOM. See [Scraping Guide](references/scraping.md).

## Reference Documentation

- **[Server Management](references/server-management.md)** — Starting, stopping, verifying readiness, troubleshooting
- **[Client API](references/client-api.md)** — Full API reference with all methods, parameters, and types
- **[ARIA Snapshots](references/aria-snapshots.md)** — Element discovery, ref system, interaction patterns
- **[Scraping Guide](references/scraping.md)** — Network interception, API replay, pagination
