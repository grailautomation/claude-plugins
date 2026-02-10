# Client API Reference

The dev-browser client connects to the server's HTTP API and provides Playwright `Page` objects for automation.

## Connecting

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();                          // Default: http://localhost:9222
const client = await connect("http://localhost:9222");   // Explicit URL
```

Returns a `DevBrowserClient` with the methods below. The client automatically reconnects if the CDP connection drops.

## DevBrowserClient Methods

### `client.page(name, options?)`

Get an existing page by name or create a new one. Returns a standard Playwright `Page` object.

```typescript
const page = await client.page("checkout");

// With custom viewport (only applies to new pages)
const page = await client.page("wide", { viewport: { width: 1920, height: 1080 } });
```

**Parameters:**
- `name` (string, required) — Descriptive page name. Use meaningful names like `"login"`, `"search-results"`, `"checkout"`.
- `options.viewport` (object, optional) — `{ width: number, height: number }`. Only applied when creating a new page.

**Returns:** Playwright `Page` — full Playwright API available (goto, click, fill, evaluate, screenshot, etc.)

**Behavior:**
- If a page with this name exists, returns the existing page
- If not, creates a new page in the persistent browser context
- Pages persist after `disconnect()` — the next script can reconnect to the same page

### `client.list()`

List all named pages currently open on the server.

```typescript
const pages = await client.list();
console.log(pages); // ["login", "checkout", "search-results"]
```

**Returns:** `string[]` — array of page names

### `client.close(name)`

Close a specific page and remove it from the registry.

```typescript
await client.close("checkout");
```

**Parameters:**
- `name` (string, required) — Name of the page to close

### `client.disconnect()`

Disconnect the CDP connection. Pages remain alive on the server for future scripts.

```typescript
await client.disconnect();
```

**Always call this at the end of every script** to release the CDP connection cleanly.

### `client.getAISnapshot(name)`

Get an ARIA accessibility tree snapshot of a page. See [ARIA Snapshots](aria-snapshots.md) for full documentation.

```typescript
const snapshot = await client.getAISnapshot("mypage");
console.log(snapshot); // YAML-formatted accessibility tree with [ref=eN] markers
```

**Parameters:**
- `name` (string, required) — Name of the page to snapshot

**Returns:** `string` — YAML-formatted accessibility tree

### `client.selectSnapshotRef(name, ref)`

Get a Playwright `ElementHandle` for a ref from the last snapshot. See [ARIA Snapshots](aria-snapshots.md) for usage patterns.

```typescript
const element = await client.selectSnapshotRef("mypage", "e5");
await element.click();
```

**Parameters:**
- `name` (string, required) — Name of the page
- `ref` (string, required) — Ref identifier from snapshot (e.g., `"e5"`)

**Returns:** `ElementHandle | null`

**Throws** if no snapshot has been taken yet or if the ref doesn't exist.

### `client.getServerInfo()`

Get server mode and connection status.

```typescript
const info = await client.getServerInfo();
console.log(info);
// { wsEndpoint: "ws://...", mode: "launch", extensionConnected: undefined }
// { wsEndpoint: "ws://...", mode: "extension", extensionConnected: true }
```

**Returns:**
- `wsEndpoint` (string) — CDP WebSocket URL
- `mode` (`"launch"` | `"extension"`) — Which mode the server is running in
- `extensionConnected` (boolean, optional) — Whether the Chrome extension is connected (extension mode only)

## waitForPageLoad

Wait for a page to finish loading. Checks `document.readyState` and monitors pending network requests.

```typescript
import { waitForPageLoad } from "@/client.js";

await waitForPageLoad(page);                           // Default options
await waitForPageLoad(page, { timeout: 15000 });       // Custom timeout
await waitForPageLoad(page, { waitForNetworkIdle: false }); // Don't wait for network
```

**Parameters:**
- `page` (Page, required) — Playwright Page object
- `options` (object, optional):
  - `timeout` (number, default: 10000) — Maximum wait time in ms
  - `pollInterval` (number, default: 50) — How often to check page state in ms
  - `minimumWait` (number, default: 100) — Minimum time to wait even if page appears ready
  - `waitForNetworkIdle` (boolean, default: true) — Wait for no pending network requests

**Returns:** `WaitForPageLoadResult`
- `success` (boolean) — Whether the page loaded successfully
- `readyState` (string) — Document ready state when finished
- `pendingRequests` (number) — Remaining pending requests
- `waitTimeMs` (number) — Time spent waiting
- `timedOut` (boolean) — Whether timeout was reached

**Smart filtering:** Automatically ignores ads, tracking pixels, and non-critical resources (images loading > 3s) when determining network idle state.

## Other Waiting Patterns

Use Playwright's built-in waiting methods on the `Page` object:

```typescript
await page.waitForSelector(".results");        // Wait for a specific element
await page.waitForURL("**/success");           // Wait for a URL pattern
await page.waitForLoadState("networkidle");    // Playwright's network idle
await page.waitForTimeout(1000);               // Fixed delay (use sparingly)
```

## Types

```typescript
interface ViewportSize {
  width: number;
  height: number;
}

interface PageOptions {
  viewport?: ViewportSize;
}

interface ServerInfo {
  wsEndpoint: string;
  mode: "launch" | "extension";
  extensionConnected?: boolean;
}

interface WaitForPageLoadResult {
  success: boolean;
  readyState: string;
  pendingRequests: number;
  waitTimeMs: number;
  timedOut: boolean;
}
```
