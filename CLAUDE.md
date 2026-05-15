# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Monorepo of Claude Code plugins. Each plugin is a self-contained directory with its own `.claude-plugin/plugin.json`. The root `.claude-plugin/marketplace.json` lists every publishable plugin with metadata (name, source path, category, `strict` flag).

Some plugins may also include Codex adapter metadata such as `.codex-plugin/plugin.json`, but Claude and Codex plugin architectures are not interchangeable. Treat Codex exposure as a separate adapter layer.

See `CODEX_MIGRATION.md` for the current Codex marketplace contents, candidate
review, and migration rules.

This is a **content-first repository** — almost entirely Markdown. There is no build system, test runner, CI pipeline, or linting config. The legacy/local MCP server implementations (`cloudflare`, `namecheap`) are the only plugins with JavaScript code. Cloudflare is CLI-first by default; its MCP config is legacy opt-in.

## Plugin Anatomy

Each plugin lives in a top-level directory with this structure:

```
<plugin>/
├── .claude-plugin/plugin.json   # Claude manifest: name required; description strongly recommended
├── .codex-plugin/plugin.json    # Optional Codex adapter manifest when supported
├── skills/<skill-name>/
│   ├── SKILL.md                 # Frontmatter + focused core knowledge
│   └── references/*.md          # Deep-dive docs, lazily loaded via Read tool
├── agents/*.md                  # Subagent definitions with tool restrictions
├── commands/*.md                # Legacy flat skill files only; do not add new command recipes
├── hooks/                       # PreToolUse/PostToolUse/Stop hooks (unused currently)
├── mcp-server/                  # Local MCP server code (cloudflare legacy opt-in, namecheap default)
└── scripts/                     # Shell scripts invoked by skills (only spec-kit)
```

Not every plugin uses all component types.

## Key Conventions

### Skills (SKILL.md)

- YAML frontmatter with optional `name`, recommended `description`, and behavior fields like `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, and `context`
- The `description` field doubles as a **trigger phrase list** — Claude matches user requests to skills based on it
- **Progressive discovery**: SKILL.md provides the summary; `references/*.md` provides depth. Link references with relative markdown links — Claude won't discover them otherwise
- Keep SKILL.md focused; move detailed reference material to `references/`
- `disable-model-invocation: true` keeps workflow skills user-invoked only; `user-invocable: false` marks background knowledge that users should not invoke directly
- For Codex-only invocation policy or presentation metadata, use
  `skills/<skill>/agents/openai.yaml`; do not assume Claude-specific
  frontmatter is honored by Codex.

### Agents (agents/*.md)

- YAML frontmatter with `name`, `description`, `tools:` or `disallowedTools:`, `model:`
- Enforce least-privilege via tool whitelists/blacklists (e.g., read-only agents block `Edit`, `Write`, `Task`)
- Plugin-shipped agents cannot use `hooks`, `mcpServers`, or `permissionMode`; keep those in user/project config instead
- `$ARGUMENTS` in the body receives input from the caller (interpolated into system prompt)

### Commands (commands/*.md)

- Custom slash command authoring is now part of Claude skills. Existing `commands/*.md` files still work, but modernized assets should live at `skills/<name>/SKILL.md`; do not add new command recipe files.
- YAML frontmatter with `description`, optional `argument-hint`, `allowed-tools`, and usually `disable-model-invocation: true` for user-triggered workflows
- `$ARGUMENTS` receives user input after the slash command
- `${CLAUDE_PLUGIN_ROOT}` resolves paths to plugin-relative resources at runtime

### MCP Servers

- Plain Node.js using `@modelcontextprotocol/sdk` with stdio transport
- Claude plugins can expose MCP either with root `.mcp.json` or inline
  `mcpServers` in `.claude-plugin/plugin.json`. Do not use either for
  CLI-first plugins.
- Credentials read from environment variables, declared in `.mcp.json` at the
  plugin root when MCP is the default path; legacy opt-in MCP configs use
  `.mcp.legacy.json`.
- Published local MCP packages use `@grailautomation/<name>-mcp`
- Prefer CLI-backed integrations over MCP whenever a maintained CLI can safely
  perform the workflow. This applies to Claude and Codex. Use MCP only when no
  usable CLI exists, the CLI cannot express the operation safely, or the MCP
  server itself is the plugin's core value.
- For Google Workspace, route Gmail, Calendar, Drive, Docs, Sheets, Slides, and
  related workflows through the `google-workspace` plugin and `gws` CLI, not
  Gmail/GCal/GDrive MCP endpoints.
- Route BigQuery, Guru, Context7, and Cloudflare through their maintained CLIs
  rather than default MCP. Pilot Hex, Notion, and ServiceNow CLI workflows, but
  keep their MCP configs until auth, JSON output, write safeguards, and workflow
  coverage are validated.
- Use `ruby scripts/check_cli_integrations.rb` to report local CLI availability
  for CLI-backed replacements. The script does not install anything; use
  `--strict` only when validating an environment expected to have the required
  CLIs.
- For plugin-required per-install values, prefer `userConfig` in `plugin.json` and `${user_config.KEY}` substitutions. For optional account/workspace-specific connectors, prefer user/project/local MCP config with environment-variable-backed URLs so broad marketplace plugins do not fail on unset placeholders.

### Versioning

- During active development, omit `version` from plugin manifests and marketplace entries. Claude Code then uses the plugin source git commit SHA as the cache/update key, so content changes are not silently skipped.
- Do not set `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; Claude resolves the manifest value first and the marketplace entry second.
- If a plugin needs stable public release behavior, use semantic versioning and a `CHANGELOG.md`, preferably controlled from the marketplace entry so release state stays centralized.
- If repository-wide SHA churn becomes a problem, add a release script that tracks a per-plugin content digest and bumps only the changed plugins' marketplace-entry patch versions. Do not use raw repo SHAs or arbitrary content hashes as visible release versions.

## Content Governance

**Never commit real org IDs, email addresses, company names, or credentials to this repo.** User-specific data goes in `.local.md` files (gitignored) or `~/.claude/skills/`. Evaluate real-looking examples case-by-case before scrubbing them; preserve utility, but prefer `example.com` / fictional data for public plugin content.

### Repository Residency

Repo membership is an explicit decision, not a fixed constraint. During cleanup,
classify each asset before publishing, adapting, or deleting it:

| Status | Meaning | Action |
| --- | --- | --- |
| `public-marketplace` | Generic enough to publish from this repo. | Keep tracked, list in the Claude marketplace, and add Codex metadata only after review. |
| `needs-generalization` | Useful, but currently has personal or local assumptions. | Rewrite with public defaults plus env/userConfig/local overlays before listing broadly. |
| `split-public-private` | Has a reusable public core and private user-specific values. | Keep the reusable core here; move private values to `.local.md`, user skills, local plugin config, or a private repo. |
| `personal-local` | Valuable to Dave, but not a public marketplace asset. | Remove from the tracked marketplace/repo after preserving it in a local Claude/Codex install location or private repo. |
| `parked` | Potentially useful, but blocked by architecture, auth, overlap, or unclear value. | Keep documented in the migration ledger, but do not list or adapt until the blocker is resolved. |

Removing an asset from this repo is allowed when classification calls for it,
but do it deliberately: remove marketplace entries, preserve a recoverable copy
outside the repo when it is still personally useful, and record the destination
or reason in the relevant migration ledger.

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

Before committing, run the repository validator and verify no PII in tracked
files:

```bash
ruby scripts/validate_repo.rb
ruby scripts/check_cli_integrations.rb

# Check tracked files for email addresses (excluding example.com and plugin infra files)
git grep -n -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -- '*.md' | rg -v '@example|CLAUDE.md'
git grep -n -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' -- '*.md' '*.json' | rg -v '@example|CLAUDE.md|marketplace.json'

# Check for Salesforce org IDs
git grep -n -E '00D[A-Za-z0-9]{15}' -- '*.md' | rg -v '00D000000000000|data:image'

# Check for hardcoded user paths
git grep -n -E '/Users/[a-z]+' -- '*.md'
```

### Git History Note

PII from the salesforce-soql org schemas existed in git history prior to commit `fe12666`. This is a documented risk acceptance — the repo was not public at the time, and history rewriting is destructive. If the repo is ever made public, run `git filter-repo` on the affected commits first.
