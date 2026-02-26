---
name: context7
version: 0.1.0
user-invocable: true
description: >-
  This skill should be used when the user asks to "fetch current library docs",
  "use Context7", "get up-to-date documentation", "look up the latest API",
  or when generating code for modern frameworks (Next.js 15, React 19,
  Tailwind v4, Svelte 5, etc.), when a user requests version-specific library
  docs, or when troubleshooting potentially outdated API patterns. Skip for
  vanilla JS/HTML/CSS, stable well-known APIs, or general programming concepts.
---

# Context7 MCP Usage Guide

Context7 provides current library documentation to prevent hallucinated APIs. It exposes two tools that must be used in sequence.

## Core Workflow

**Step 1: Resolve the library ID**
```
resolve-library-id(libraryName: "next.js")
→ Returns: /vercel/next.js (plus metadata, trust scores, versions)
```

**Step 2: Fetch documentation**
```
query-docs(
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "middleware",  // optional — focuses results
  tokens: 5000          // optional — default 5000, min 1000
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

## Using the Topic Parameter

Focus documentation retrieval with specific topics:

```
query-docs(
  context7CompatibleLibraryID: "/supabase/supabase-js",
  topic: "authentication"  // Much better than fetching all docs
)
```

Good topic values: `routing`, `hooks`, `authentication`, `middleware`, `configuration`, `testing`, `deployment`, `database`, `api`, `components`

## Error Handling

See [references/error-handling.md](references/error-handling.md) for common errors and solutions.

**Quick reference:**
- "Documentation not found" — Library may not be indexed; check context7.com or try base ID without version
- Empty results — Try broader topic or remove topic parameter
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
