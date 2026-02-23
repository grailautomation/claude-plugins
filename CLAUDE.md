# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Monorepo of 13 Claude Code plugins. Each plugin is a self-contained directory with its own `.claude-plugin/plugin.json`. The root `.claude-plugin/marketplace.json` registers all plugins with metadata (name, source path, category, `strict` flag).

This is a **content-first repository** — almost entirely Markdown. There is no build system, test runner, CI pipeline, or linting config. The two MCP server plugins (`cloudflare`, `namecheap`) are the only ones with JavaScript code.

## Plugin Anatomy

Each plugin lives in a top-level directory with this structure:

```
<plugin>/
├── .claude-plugin/plugin.json   # Required: name, description, author
├── skills/<skill-name>/
│   ├── SKILL.md                 # Frontmatter + core knowledge (~200 lines max)
│   └── references/*.md          # Deep-dive docs, lazily loaded via Read tool
├── agents/*.md                  # Subagent definitions with tool restrictions
├── commands/*.md                # User-invocable slash commands
├── hooks/                       # PreToolUse/PostToolUse/Stop hooks (unused currently)
├── mcp-server/                  # MCP servers (only cloudflare, namecheap)
└── scripts/                     # Shell scripts invoked by commands (only spec-kit)
```

Not every plugin uses all component types.

## Key Conventions

### Skills (SKILL.md)

- YAML frontmatter with `name`, `description`, optional `user-invocable`, `version`
- The `description` field doubles as a **trigger phrase list** — Claude matches user requests to skills based on it
- **Progressive discovery**: SKILL.md provides the summary; `references/*.md` provides depth. Link references with relative markdown links — Claude won't discover them otherwise
- Keep SKILL.md under ~200 lines; move detail to `references/`
- `user-invocable: false` marks skills only activated by other skills/commands, not by users directly

### Agents (agents/*.md)

- YAML frontmatter with `name`, `description`, `tools:` or `disallowedTools:`, `model:`
- Enforce least-privilege via tool whitelists/blacklists (e.g., read-only agents block `Edit`, `Write`, `Task`)
- `$ARGUMENTS` in the body receives input from the caller (interpolated into system prompt)

### Commands (commands/*.md)

- YAML frontmatter with `description`, optional `argument-hint`, `allowed-tools`
- `$ARGUMENTS` receives user input after the slash command
- `${CLAUDE_PLUGIN_ROOT}` resolves paths to plugin-relative resources at runtime

### MCP Servers

- Plain Node.js using `@modelcontextprotocol/sdk` with stdio transport
- Credentials read from environment variables, declared in `.mcp.json` at the plugin root
- Published to npm as `@grailautomation/<name>-mcp`

## Content Governance

**Never commit real org IDs, email addresses, company names, or credentials to this repo.** User-specific data goes in `.local.md` files (gitignored) or `~/.claude/skills/`.

### Decision Tree

```
Does it contain PII, org IDs, credentials, or company-specific data?
├── YES → Is it contextually tied to a specific plugin?
│   ├── YES → .local.md file inside the plugin (gitignored)
│   └── NO  → User-level skill (~/.claude/skills/)
└── NO  → Is it useful to other Claude Code users?
    ├── YES → Plugin repo (public)
    └── NO  → User-level skill or doesn't need to exist
```

### The Four Tiers

| Tier | Location | What goes here | Example |
|------|----------|---------------|---------|
| 1. Public | Plugin repo | Generic, reusable content that works for any user | SOQL syntax guides, Workato SDK docs, generic agents |
| 2. User skills | `~/.claude/skills/` | Personal knowledge spanning multiple projects | Machine config, company/org context, credential refs |
| 3. Local plugin | `*.local.md` (gitignored) | User-specific data tied to a specific plugin | Org schemas, personal domain lists, custom paths |
| 4. Private | Don't publish | Plugins inherently org-specific with no generic value | Internal API connectors with no reusable patterns |

### Pre-Commit Checks

Before committing, verify no PII in tracked files:

```bash
# Check for email addresses (excluding example.com and plugin infra files)
grep -rn '@[a-z]' --include='*.md' . | grep -v '@example' | grep -v 'CLAUDE.md'
grep -rn '@[a-z]' --include='*.md' --include='*.json' . | grep -v '@example' | grep -v 'CLAUDE.md' | grep -v 'plugin.json' | grep -v 'marketplace.json'

# Check for Salesforce org IDs
grep -rn '00D[A-Za-z0-9]\{15\}' --include='*.md' . | grep -v '00D000000000000'

# Check for hardcoded user paths
grep -rn '/Users/[a-z]' --include='*.md' .
```

### Git History Note

PII from the salesforce-soql org schemas existed in git history prior to commit `fe12666`. This is a documented risk acceptance — the repo was not public at the time, and history rewriting is destructive. If the repo is ever made public, run `git filter-repo` on the affected commits first.
