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

| Plugin group | Reason |
| --- | --- |
| `agents`, `staff-software-engineer` | Claude subagent definitions are not equivalent to Codex plugin skills. |
| `issue-blaster`, `scraper-generator` | Include Claude subagents and workflow assumptions that need Codex-native rewrite. |
| `data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` | Many include placeholder connector or MCP expectations; review `.mcp.json` and decide Codex app/MCP mapping first. |
| `google-workspace` | Large recipe surface; likely valuable, but needs connector/auth strategy before listing. |
| `cloudflare`, `namecheap` | MCP server packaging and credential setup need Codex manifest and install-path review. |
| `jq-for-clawd` | Claude session-history assumptions need a Codex session-log rewrite. |
| `dev-browser` | Overlaps existing browser tooling and needs runtime/tooling validation. |
| `espanso`, `karabiner-elements` | Likely personal machine-automation skills rather than public marketplace plugins. |

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
