# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository Overview

Monorepo of Claude Code plugins, with optional Codex adapter metadata where needed. Claude plugins use `.claude-plugin/plugin.json`, and the root `.claude-plugin/marketplace.json` lists every publishable Claude plugin with metadata (name, source path, category, `strict` flag).

Codex plugin architecture is not interchangeable with Claude plugin architecture. Codex exposure is additive: use `.agents/plugins/marketplace.json` plus per-plugin `.codex-plugin/plugin.json` only for plugins that have been deliberately adapted for Codex.

This is a **content-first repository** — almost entirely Markdown. There is no build system, test runner, CI pipeline, or linting config. The two MCP server plugins (`cloudflare`, `namecheap`) are the only ones with JavaScript code.

## Plugin Anatomy

Each plugin lives in a top-level directory with this structure:

```
<plugin>/
├── .claude-plugin/plugin.json  # Claude manifest: name required; description strongly recommended
├── .codex-plugin/plugin.json   # Optional Codex adapter manifest when supported
├── skills/<skill-name>/
│   ├── SKILL.md                 # Frontmatter + focused core knowledge
│   └── references/*.md          # Deep-dive docs, lazily loaded via Read tool
├── agents/*.md                  # Subagent definitions with tool restrictions
├── commands/*.md                # Legacy flat skill files only; do not add new command recipes
├── hooks/                       # PreToolUse/PostToolUse/Stop hooks (unused currently)
├── mcp-server/                  # MCP servers (only cloudflare, namecheap)
└── scripts/                     # Shell scripts invoked by skills (only spec-kit)
```

Not every plugin uses all component types.

## Key Conventions

### Skills (SKILL.md)

- YAML frontmatter with optional `name`, recommended `description`, and behavior fields like `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, and `context`
- The `description` field doubles as a **trigger phrase list** — Claude matches user requests to skills based on it
- **Progressive discovery**: SKILL.md provides the summary; `references/*.md` provides depth. Link references with relative markdown links — Codex won't discover them otherwise
- Keep SKILL.md focused; move detailed reference material to `references/`
- `disable-model-invocation: true` keeps workflow skills user-invoked only; `user-invocable: false` marks background knowledge that users should not invoke directly

### Agents (agents/*.md)

- YAML frontmatter with `name`, `description`, `tools:` or `disallowedTools:`, `model:`
- Enforce least-privilege via tool whitelists/blacklists (e.g., read-only agents block `Edit`, `Write`, `Task`)
- Plugin-shipped Claude agents cannot use `hooks`, `mcpServers`, or `permissionMode`; keep those in user/project config instead
- `$ARGUMENTS` in the body receives input from the caller (interpolated into system prompt)

### Commands (commands/*.md)

- Custom slash command authoring is now part of Claude skills. Existing `commands/*.md` files still work, but modernized assets should live at `skills/<name>/SKILL.md`; do not add new command recipe files.
- YAML frontmatter with `description`, optional `argument-hint`, `allowed-tools`, and usually `disable-model-invocation: true` for user-triggered workflows
- `$ARGUMENTS` receives user input after the slash command
- `${CLAUDE_PLUGIN_ROOT}` resolves paths to plugin-relative resources at runtime

### MCP Servers

- Plain Node.js using `@modelcontextprotocol/sdk` with stdio transport
- Credentials read from environment variables, declared in `.mcp.json` at the plugin root
- Published to npm as `@grailautomation/<name>-mcp`
- For plugin-required per-install values, prefer `userConfig` in `plugin.json` and `${user_config.KEY}` substitutions. For optional account/workspace-specific connectors, prefer user/project/local MCP config with environment-variable-backed URLs so broad marketplace plugins do not fail on unset placeholders.

### Versioning

- During active development, omit `version` from plugin manifests and marketplace entries. Claude Code then uses the plugin source git commit SHA as the cache/update key, so content changes are not silently skipped.
- Do not set `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; Claude resolves the manifest value first and the marketplace entry second.
- If a plugin needs stable public release behavior, use semantic versioning and a `CHANGELOG.md`, preferably controlled from the marketplace entry so release state stays centralized.
- If repository-wide SHA churn becomes a problem, add a release script that tracks a per-plugin content digest and bumps only the changed plugins' marketplace-entry patch versions. Do not use raw repo SHAs or arbitrary content hashes as visible release versions.

## Content Governance

**Never commit real org IDs, email addresses, company names, or credentials to this repo.** User-specific data goes in `.local.md` files (gitignored) or user-level skills (`~/.claude/skills/` or `~/.codex/skills/`). Evaluate real-looking examples case-by-case before scrubbing them; preserve utility, but prefer `example.com` / fictional data for public plugin content.

### Decision Tree

```
Does it contain PII, org IDs, credentials, or company-specific data?
├── YES → Is it contextually tied to a specific plugin?
│   ├── YES → .local.md file inside the plugin (gitignored)
│   └── NO  → User-level skill (~/.claude/skills/ or ~/.codex/skills/)
└── NO  → Is it useful to other Claude Code users?
    ├── YES → Plugin repo (public)
    └── NO  → User-level skill or doesn't need to exist
```

### The Four Tiers

| Tier | Location | What goes here | Example |
|------|----------|---------------|---------|
| 1. Public | Plugin repo | Generic, reusable content that works for any user | SOQL syntax guides, Workato SDK docs, generic agents |
| 2. User skills | `~/.claude/skills/` or `~/.codex/skills/` | Personal knowledge spanning multiple projects | Machine config, company/org context, credential refs |
| 3. Local plugin | `*.local.md` (gitignored) | User-specific data tied to a specific plugin | Org schemas, personal domain lists, custom paths |
| 4. Private | Don't publish | Plugins inherently org-specific with no generic value | Internal API connectors with no reusable patterns |

### Pre-Commit Checks

Before committing, verify no PII in tracked files:

```bash
# Check tracked files for email addresses (excluding example.com and plugin infra files)
git grep -n -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -- '*.md' | rg -v '@example|AGENTS.md'
git grep -n -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -- '*.md' '*.json' | rg -v '@example|AGENTS.md|plugin.json|marketplace.json'

# Check for Salesforce org IDs
git grep -n -E '00D[A-Za-z0-9]{15}' -- '*.md' | rg -v '00D000000000000|data:image'

# Check for hardcoded user paths
git grep -n -E '/Users/[a-z]+' -- '*.md'
```

### Git History Note

PII from the salesforce-soql org schemas existed in git history prior to commit `fe12666`. This is a documented risk acceptance — the repo was not public at the time, and history rewriting is destructive. If the repo is ever made public, run `git filter-repo` on the affected commits first.
