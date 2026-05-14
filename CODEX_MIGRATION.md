# Codex Migration Ledger

This repository remains Claude-first, with Codex exposure added only when a
plugin has been deliberately reviewed against Codex plugin structure.

Current Codex docs baseline:
- A Codex plugin needs `.codex-plugin/plugin.json`.
- Plugin components such as `skills/`, `.mcp.json`, `.app.json`, `hooks/`, and
  `assets/` stay at the plugin root; only `plugin.json` belongs under
  `.codex-plugin/`.
- Repo-scoped marketplaces live at `.agents/plugins/marketplace.json`.
- Marketplace `source.path` is relative to the repository root and must begin
  with `./`.
- Codex skills require `name` and `description` frontmatter and can use
  `skills/<skill>/agents/openai.yaml` for Codex-specific invocation policy and
  presentation metadata.

## Current Codex Marketplace

The tracked Codex marketplace exposes:

| Plugin | Status | Rationale |
| --- | --- | --- |
| `spec-kit` | Migrated | High-value workflow plugin; already structured as skills plus bundled scripts; no MCP or connector dependency. |
| `uv-package-manager` | Migrated | Skill-only Python tooling workflow; no plugin-local state or connector dependency. |
| `python-patterns` | Migrated | Skill-only Python reference and review workflow. |
| `openapi-spec-generation` | Migrated | Skill-only OpenAPI workflow with local references. |
| `python-quickbooks` | Migrated | Skill-only library reference; examples use placeholders rather than live credentials. |
| `terminal-tidbits` | Migrated | User-data path moved outside the plugin directory; defaults remain plugin-bundled. |
| `salesforce-soql` | Migrated | Salesforce CLI/reference workflow; no bundled MCP and org schemas remain local/ignored. |
| `oasb-scaffold` | Migrated | Repo-specific OASBuilder convention skill; exposed for personal/repo-local usefulness. |
| `workato-api` | Migrated | REST reference and curl/httpx execution patterns; credentials come from environment variables or gitignored local notes. |
| `workato-recipe` | Migrated | Script-backed recipe analysis now uses the stable root CLI and avoids Claude-only path/subagent assumptions for Codex. |
| `workato-connector-sdk` | Migrated | Documentation-heavy connector SDK plugin; stale CLI claims and copied token/project examples were corrected before exposure. |
| `workato-platform-cli` | Migrated | Repo copy matches the installed user-level Codex skill; listed with explicit invocation policy because it can manage real Workato assets. |

The parked prototype files from the exploratory pass live under
`.scratch/codex-adapter-prototype/2026-05-14/`. They are intentionally ignored
and should be treated as reference material only.

## Candidate Review

### Direct Or Near-Direct Candidates

This bucket is currently empty. The near-direct Workato candidates have been
migrated; remaining plugin groups need rewrite, connector, MCP, or personal
scope decisions rather than mechanical manifest work.

### Already Exposed Or Covered Locally

| Plugin | Status | Notes |
| --- | --- | --- |
| `playwright-cli` | Covered | A user-level Codex `playwright` skill already exists; migrate only if this repo plugin has distinct value. |
| `cloudflare` | Partially covered | Codex has Cloudflare deployment/plugin support; this repo's MCP packaging needs a separate credential review. |

### Requires Rewrite Or Connector Review

These should not be mechanically exposed by adding manifests only.

| Plugin group | Required action before listing | Why it is blocked |
| --- | --- | --- |
| `agents`, `staff-software-engineer` | Rewrite useful agent prompts as Codex skills with `SKILL.md`; keep Claude-only agent files out of Codex manifests. | These plugins are agent-definition bundles, and Claude subagent metadata is not a Codex plugin interface. |
| `issue-blaster`, `scraper-generator` | Replace Claude subagent orchestration with Codex-native skill workflows, then smoke-test one end-to-end issue/scraper flow. | Both plugins mix skills with Claude agents and assume delegation surfaces that Codex will not load as plugin skills. |
| `data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` | For each domain pack, map every `.mcp.json` server to either a supported Codex MCP dependency, a Codex app/connector, or an intentional omission; then set explicit auth policy. | They are mostly connector catalogs. Listing them without auth/install mapping would expose broken or misleading integrations. |
| `google-workspace` | Split the large recipe surface into safe read-only, write/send, and watch/automation groups; map each group to Codex Google connectors or MCP dependencies before listing. | The plugin has many action-oriented recipes with different auth and side-effect profiles, so one manifest policy is too coarse. |
| `cloudflare`, `namecheap` | Verify local MCP server packaging, npm package names, lockfile choice, env vars, and Codex MCP startup behavior; then add manifests with explicit env requirements. | These ship MCP servers and credentials, not only skills. The install path must work before marketplace exposure. |
| `context7` | Add or declare a Codex-compatible Context7 MCP dependency, or rewrite the skill to route through an available docs tool. | The skill instructs the agent to call Context7 tools, but this repo plugin does not currently provide the MCP server config. |
| `jq-for-clawd` | Fork into a Claude session-history skill and a Codex session-history skill; rewrite the Codex variant for `~/.codex/sessions` and Codex rollout JSONL structure. | Current instructions hard-code Claude Code session paths and message schema. |
| `dev-browser` | Decide whether it supersedes, complements, or should be retired in favor of the existing Chrome/browser tooling; if kept, run its build/test suite and validate extension startup. | It is a full browser-extension/runtime project, not a simple skill bundle, and it overlaps existing Codex browser capabilities. |
| `espanso`, `karabiner-elements` | Decide whether these belong in the public marketplace or should remain personal user-local skills; if listed, mark explicit-invocation-only and validate macOS config backup/restore behavior. | They modify local machine automation state and include user-environment assumptions. |
| `playwright-cli` | Keep covered unless a concrete gap versus the installed Codex `playwright` skill appears; if a gap exists, migrate only that distinct workflow. | The current Codex environment already has a Playwright skill, so listing another browser automation plugin risks duplicate triggers. |

## Migration Rules

- Add a plugin to `.agents/plugins/marketplace.json` only after its
  `.codex-plugin/plugin.json`, skill metadata, and runtime assumptions have been
  reviewed.
- Prefer `skills/<skill>/agents/openai.yaml` for Codex-only invocation policy
  instead of overloading Claude-specific frontmatter.
- Do not copy personal author emails into Codex manifests.
- Keep Codex migration PRs separate from Claude cleanup PRs.
- Validate both surfaces when a plugin remains dual-use: `claude plugin
  validate <plugin>` for Claude and JSON/YAML/frontmatter checks for Codex.
