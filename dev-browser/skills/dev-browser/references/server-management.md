# Server Management

The dev-browser server is a long-running process that launches Chromium and exposes an HTTP API on port 9222 for page management. Pages persist across script executions until the server is stopped.

## Starting the Server

### Standalone Mode (Default)

Launches a fresh Chromium instance. Use this for most automation tasks.

```bash
cd skills/dev-browser && ./server.sh &
```

Add `--headless` for headless mode (no visible browser window):

```bash
cd skills/dev-browser && ./server.sh --headless &
```

The `server.sh` script runs `npm install` then starts the server via `npx tsx scripts/start-server.ts`.

### Extension Mode

Connects to the user's existing Chrome browser (preserving logged-in sessions, cookies, extensions). Use when:

- The user is already logged into sites they want to automate
- The user explicitly asks to use the extension

```bash
cd skills/dev-browser && npm i && npm run start-extension &
```

Wait for `Extension connected` in the console before running scripts. If the extension hasn't connected, tell the user to install and activate it from: https://github.com/SawyerHood/dev-browser/releases

## Verifying Readiness

**Do not watch stdout for a "Ready" message.** Background processes don't stream stdout in Claude Code.

Instead, poll the HTTP endpoint:

```bash
for i in $(seq 1 30); do
  curl -s http://localhost:9222 > /dev/null 2>&1 && echo "Server ready" && break
  sleep 1
done
```

This handles both cases:
- **Server just started**: curl retries until the HTTP API is up (up to 30 seconds)
- **Server already running**: curl succeeds immediately on the first attempt

### Quick Check (No Polling)

To test if the server is already running without starting it:

```bash
curl -s http://localhost:9222 | head -c 100
```

A successful response returns JSON with the WebSocket endpoint.

## How It Works Internally

`scripts/start-server.ts` does the following on startup:

1. Creates `tmp/` and `profiles/` directories
2. Checks if Playwright Chromium is installed; installs it if not
3. **Checks if a server is already running on port 9222** — if so, exits immediately with code 0 (this is why background tasks may appear to "complete instantly" with no output)
4. Cleans up stale Chrome processes on CDP port 9223
5. Launches Chromium with `launchPersistentContext` (cookies and localStorage persist across restarts)
6. Starts Express HTTP API on port 9222
7. Prints "Ready" and keeps the process alive

Understanding step 3 is important: if the server is already running from a previous session, `start-server.ts` exits silently. The curl poll pattern handles this gracefully.

## HTTP API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Server info (returns WebSocket endpoint) |
| `/pages` | GET | List all named pages |
| `/pages` | POST | Get or create a page by name |
| `/pages/:name` | DELETE | Close a page |

## Stopping the Server

Kill the server process:

```bash
pkill -f "start-server.ts" 2>/dev/null
pkill -f "start-relay.ts" 2>/dev/null
```

Or use a targeted approach:

```bash
# Find and kill the process on port 9222
lsof -ti:9222 | xargs kill 2>/dev/null
```

## Troubleshooting

### Server exits immediately (exit code 0)

A server is already running on port 9222. Use `curl -s http://localhost:9222` to confirm, then proceed with your scripts — no restart needed.

### Port 9222 or 9223 already in use

Another process is occupying the port. Find and kill it:

```bash
lsof -ti:9222 | xargs kill 2>/dev/null
lsof -ti:9223 | xargs kill 2>/dev/null
```

Then restart the server.

### npm install fails

Run it manually first to see the error:

```bash
cd skills/dev-browser && npm install
```

Common causes: missing Node.js, network issues, or permission problems.

### Chromium fails to launch

Playwright may need its browser binaries installed:

```bash
cd skills/dev-browser && npx playwright install chromium
```

### Server starts but scripts can't connect

Verify the server is responding:

```bash
curl -s http://localhost:9222
```

If it returns JSON with a `wsEndpoint`, the server is running. If scripts still fail, the CDP WebSocket connection on port 9223 may be stale — restart the server.
