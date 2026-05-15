---
name: context7
version: 0.1.0
user-invocable: true
description: >-
  This skill should be used when the user asks to "fetch current library docs",
  "use Context7", "get up-to-date documentation", "look up the latest API",
  or when generating code for modern libraries, frameworks, SDKs, APIs, CLIs,
  or cloud services where current syntax matters. Use when a user requests
  version-specific docs or when troubleshooting potentially outdated API
  patterns. Skip for vanilla JS/HTML/CSS, code review, business-logic
  debugging, refactoring, or general programming concepts.
---

# Context7 CLI Usage Guide

Context7 provides current library, framework, SDK, API, CLI, and cloud-service
documentation to prevent stale API usage. Use the `ctx7` CLI instead of MCP.
The CLI works without authentication for normal `library` and `docs` lookups;
login or `CONTEXT7_API_KEY` only improves rate limits and unlocks skill
generation.

Prefer one-off execution when the CLI is not already installed:

```bash
npx -y ctx7 --help
pnpm dlx ctx7 --help
```

Before recommending a persistent global install, check existing install lanes:

```bash
type -a ctx7 node npm pnpm npx
which -a ctx7 node npm pnpm npx
```

## Core Workflow

**Step 1: Resolve the library ID**
```bash
ctx7 library nextjs "Find current Next.js middleware documentation"
ctx7 library react "How to clean up useEffect with async operations" --json
```
This returns matching Context7 library IDs plus coverage and trust metadata.
Choose the closest match with the strongest coverage and reputation.

**Step 2: Fetch documentation**
```bash
ctx7 docs /vercel/next.js "How does middleware work in the current version?"
ctx7 docs /facebook/react "How to use hooks for state management" --json
```

Skip Step 1 only when the exact library ID is already known from a previous
lookup or user input. Library IDs always start with `/`; plain package names are
for `ctx7 library`, not `ctx7 docs`.

## Library ID Format

| Format | Example | Use Case |
|--------|---------|----------|
| `/org/project` | `/vercel/next.js` | Latest docs |
| `/org/project/vX.Y.Z` | `/vercel/next.js/v15.1.0` | Version-specific |

Note the `v` prefix on version numbers.

Example:

```bash
ctx7 docs /vercel/next.js/v14.3.0-canary.87 "How to set up app router"
```

## When to Use Context7

**Activate for:**
- Libraries released or updated after training cutoff (Next.js 15, React 19, Svelte 5)
- Fast-evolving frameworks (TanStack Query, Tailwind CSS, Zod, Prisma)
- Setup and configuration tasks requiring current syntax
- Version-specific API questions
- Niche libraries with limited training data

**Skip for:**
- Vanilla JavaScript, HTML, CSS
- General algorithms and data structures
- Stable, well-documented APIs (lodash basics, moment.js)
- Non-code tasks

## Writing Good Queries

Use specific task-oriented queries for both tool calls. Do not send API keys, credentials, personal data, proprietary source code, or other sensitive details in Context7 queries.

```bash
ctx7 library supabase "How do I configure email/password authentication in supabase-js?"
ctx7 docs /supabase/supabase-js "How do I configure email/password authentication in supabase-js?"
```

Good query topics include routing, hooks, authentication, middleware, configuration, testing, deployment, database access, API clients, and UI components.

Use `--json` when the response will be piped into other tools. Keep queries
task-oriented, not keyword-only.

## Authentication

Most documentation lookups work without authentication:

```bash
ctx7 whoami
ctx7 login --no-browser
export CONTEXT7_API_KEY=your_key
```

Do not include API keys, credentials, proprietary code, or personal data in
Context7 queries.

## Legacy MCP

The previous MCP config is preserved as `.mcp.legacy.json` for explicit opt-in
compatibility testing only. Do not restore `.mcp.json` as the default path unless
a future issue documents why the CLI is insufficient. Do not add inline
`mcpServers` to `.claude-plugin/plugin.json` or `mcpServers` to
`.codex-plugin/plugin.json` for the default plugin path.

## Error Handling

See [references/error-handling.md](references/error-handling.md) for common errors and solutions.

**Quick reference:**
- "Documentation not found" — Library may not be indexed; check context7.com or try base ID without version
- Empty results — Try a broader task-oriented query
- Rate limit errors — Back off and retry; consider API key for heavy usage

## High-Value Libraries

These benefit most from Context7 (fast-changing APIs):

| Category | Libraries |
|----------|-----------|
| React ecosystem | Next.js, React, TanStack Query, Zustand |
| CSS/Styling | Tailwind CSS, Panda CSS, StyleX |
| Validation | Zod, Valibot, ArkType |
| Database/ORM | Prisma, Drizzle, Supabase |
| Full-stack | Nuxt, SvelteKit, Astro, Remix |
