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
| `cloudflare` | Migrated | Public MCP-backed infrastructure plugin; credentials stay in environment variables; published `npx` MCP startup lists 28 tools. |
| `namecheap` | Migrated | Public MCP-backed registrar/DNS plugin; credentials and whitelisted IPs stay outside the repo; published `npx` MCP startup lists 8 tools. |
| `context7` | Migrated | Public MCP-backed docs plugin; ships Context7 MCP config and current tool schema; published `npx` MCP startup lists `resolve-library-id` and `query-docs`. |
| `codex-session-history` | Migrated | Codex-specific split from `jq-for-clawd`; uses `~/.codex/sessions` and `~/.codex/archived_sessions` JSONL shapes instead of Claude Code's project session layout. |
| `staff-software-engineer` | Migrated | Claude agent behavior preserved; Codex exposure is a `staff-plan-review` skill rather than a Claude subagent definition. |

The parked prototype files from the exploratory pass live under
`.scratch/codex-adapter-prototype/2026-05-14/`. They are intentionally ignored
and should be treated as reference material only.

## Repository Residency

Codex migration is downstream of cleanup. Cleanup can mean keeping a plugin in
this repository, splitting a public core from private overlays, or removing a
plugin from the repository entirely after preserving it somewhere appropriate.

Use these statuses while reviewing every asset:

| Status | Meaning | Typical destination |
| --- | --- | --- |
| `public-marketplace` | Generic, reusable, and appropriate for this public marketplace. | Keep in repo; list in `.claude-plugin/marketplace.json`; add Codex metadata only after review. |
| `needs-generalization` | Useful, but not yet safe or general enough for a public marketplace. | Rewrite with env/userConfig/local overlays, then reclassify. |
| `split-public-private` | Public core is useful, but user-specific data or defaults must move out. | Public core in repo; private values in `.local.md`, user skills, local plugin config, or private repo. |
| `personal-local` | Useful personally, but not a marketplace asset. | `~/.claude/skills/`, local Claude plugin install, `~/.codex/skills/`, or a private repo. |
| `parked` | Not ready to publish or adapt because value, overlap, auth, or architecture is unresolved. | Keep documented here until deliberately resumed or removed. |

When a plugin becomes `personal-local`, remove it from the tracked marketplace
and, if the content is still useful, preserve a recoverable copy outside this
repo before deleting the tracked tree.

## Candidate Review

### Direct Or Near-Direct Candidates

This bucket is currently empty. The near-direct Workato candidates have been
migrated; remaining plugin groups need rewrite, connector, MCP, or personal
scope decisions rather than mechanical manifest work.

### Already Exposed Or Covered Locally

| Plugin | Status | Notes |
| --- | --- | --- |
| `playwright-cli` | Covered | A user-level Codex `playwright` skill already exists; migrate only if this repo plugin has distinct value. |
| `cloudflare` | Migrated | This repo's MCP-backed Cloudflare plugin is now exposed directly instead of substituting the native Codex Cloudflare deployment surface. |

### Requires Rewrite Or Connector Review

These should not be mechanically exposed by adding manifests only.

| Plugin group | Required action before listing | Why it is blocked |
| --- | --- | --- |
| `agents` | Resolve [issue #29](https://github.com/grailautomation/claude-plugins/issues/29): rewrite only useful agent prompts as Codex skills with `SKILL.md`; keep Claude-only agent files out of Codex manifests. | This plugin is an agent-definition bundle, and Claude subagent metadata is not a Codex plugin interface. |
| `issue-blaster`, `scraper-generator` | Resolve [issue #23](https://github.com/grailautomation/claude-plugins/issues/23): replace Claude subagent orchestration with Codex-native skill workflows, then smoke-test one end-to-end issue/scraper flow. | Both plugins mix skills with Claude agents and assume delegation surfaces that Codex will not load as plugin skills. |
| `data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` | Resolve [issue #25](https://github.com/grailautomation/claude-plugins/issues/25): map every `.mcp.json` server to either a supported Codex MCP dependency, a Codex app/connector, or an intentional omission; then set explicit auth policy. | They are mostly connector catalogs. Listing them without auth/install mapping would expose broken or misleading integrations. |
| `google-workspace` | Resolve [issue #27](https://github.com/grailautomation/claude-plugins/issues/27): split the large recipe surface into safe read-only, write/send, watch/automation, admin/security, and multi-product recipe groups before listing. | The plugin has many action-oriented recipes with different auth and side-effect profiles, so one manifest policy is too coarse. |
| `dev-browser` | Resolve [issue #20](https://github.com/grailautomation/claude-plugins/issues/20): decide keep, retire, or narrow Codex adaptation; if kept for Codex, run its server/extension validation first. | It is a full browser-extension/runtime project, not a simple skill bundle, and it overlaps existing Codex browser capabilities. |

### Initial Residency Calls

These are working classifications, not final deletion decisions:

| Plugin or group | Current residency call | Cleanup implication |
| --- | --- | --- |
| Migrated Codex plugins in the current marketplace | `public-marketplace` or accepted public/personal hybrid | Keep listed; continue validating mechanically. |
| `terminal-tidbits` | `split-public-private` | Public skill stays here; personal notes stay outside the plugin directory. |
| `salesforce-soql` | `split-public-private` | Public SOQL and CLI workflows stay here; org schemas remain ignored/local unless sanitized examples are deliberate. |
| `cloudflare`, `namecheap` | `public-marketplace` | Keep in the public Claude marketplace. Credentials, account IDs, whitelisted IPs, and domain lists stay outside the repo in environment variables, account settings, Claude/Codex config, or gitignored local notes. |
| Domain MCP packs | `needs-generalization` | Preserve Claude MCP parity first; track Codex connector/auth/side-effect mapping in [issue #25](https://github.com/grailautomation/claude-plugins/issues/25). |
| `google-workspace` | `needs-generalization` | Track the read/write/send/watch/admin split in [issue #27](https://github.com/grailautomation/claude-plugins/issues/27); preserve Claude behavior until each Codex group is reviewed. |
| `jq-for-clawd` / `codex-session-history` | `public-marketplace` split | Keep `jq-for-clawd` as the Claude Code session-history skill; expose `codex-session-history` separately for Codex's distinct session JSONL structure. |
| `espanso`, `karabiner-elements` | `public-marketplace` Claude-only | Keep in the public Claude marketplace as generic macOS config workflows; do not expose to Codex until a side-effect policy and local-config validation path are deliberately designed. |
| `dev-browser` | `parked` | Do not list for Codex until [issue #20](https://github.com/grailautomation/claude-plugins/issues/20) resolves the keep/retire/validate path. |
| `playwright-cli` | `public-marketplace` Claude-only | Keep listed for Claude; do not list for Codex unless a concrete gap appears versus the installed Codex `playwright` skill. |
| `agents` | `parked` | Track extraction decisions in [issue #29](https://github.com/grailautomation/claude-plugins/issues/29); generic explore/plan/bash agents overlap Codex's built-in delegation surfaces. |

## Migration Rules

- Add a plugin to `.agents/plugins/marketplace.json` only after its
  `.codex-plugin/plugin.json`, skill metadata, and runtime assumptions have been
  reviewed.
- Preserve the existing Claude asset architecture by default. Do not replace an
  MCP-backed Claude workflow with a native Codex app/connector unless there is a
  documented reason; open a GitHub issue for those exceptions.
- Prefer `skills/<skill>/agents/openai.yaml` for Codex-only invocation policy
  instead of overloading Claude-specific frontmatter.
- Do not copy personal author emails into Codex manifests.
- Keep Codex migration PRs separate from Claude cleanup PRs.
- Validate both surfaces when a plugin remains dual-use: `claude plugin
  validate <plugin>` for Claude and JSON/YAML/frontmatter checks for Codex.
- Run `ruby scripts/validate_repo.rb` before proposing or merging repository
  metadata changes.
