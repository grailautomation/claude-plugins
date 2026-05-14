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

# Context7 MCP Usage Guide

Context7 provides current library, framework, SDK, API, CLI, and cloud-service documentation to prevent stale API usage. It exposes two tools that must be used in sequence.

## Core Workflow

**Step 1: Resolve the library ID**
```
resolve-library-id(
  libraryName: "Next.js",
  query: "Find current Next.js middleware documentation"
)
→ Returns: /vercel/next.js (plus metadata, trust scores, versions)
```

**Step 2: Fetch documentation**
```
query-docs(
  libraryId: "/vercel/next.js",
  query: "How does middleware work in the current version?"
)
```

Skip Step 1 only when the exact library ID is already known from a previous call or user input.

## Library ID Format

| Format | Example | Use Case |
|--------|---------|----------|
| `/org/project` | `/vercel/next.js` | Latest docs |
| `/org/project/vX.Y.Z` | `/vercel/next.js/v15.1.0` | Version-specific |

Note the `v` prefix on version numbers.

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

```
query-docs(
  libraryId: "/supabase/supabase-js",
  query: "How do I configure email/password authentication in supabase-js?"
)
```

Good query topics include routing, hooks, authentication, middleware, configuration, testing, deployment, database access, API clients, and UI components.

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
