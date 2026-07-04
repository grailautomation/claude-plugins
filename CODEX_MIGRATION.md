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

## Installability Status

The Codex installability pass is complete for the reviewed plugin set. The
tracked repo-local Codex marketplace at `.agents/plugins/marketplace.json`
contains 33 plugins, and each listed plugin has a matching
`.codex-plugin/plugin.json`.

This means the plugins are visible and available for install in Codex. Live
SaaS authentication, MCP-vs-CLI replacement, and vendor-specific smoke tests
are quality/runtime follow-ups, not blockers for Codex marketplace visibility.
Handle those only when a plugin is actively being installed, used, or promoted
from MCP to a CLI-backed default.

## Wrap-Down Status (2026-05-15 UTC / 2026-05-14 PDT)

The original practical requirement is satisfied: plugins that were approved for
Codex exposure are visible and available for install through the repo-local
Codex marketplace. Authentication and live SaaS validation are intentionally
deferred until a plugin is installed or used.

Completed cleanup and migration work includes:

- Modernized the Claude plugin content structure and validation rules.
- Added repository validation and CLI availability/smoke tooling.
- Added Codex adapter manifests and marketplace entries for reviewed plugins.
- Split Codex-specific session history from the Claude `jq-for-clawd` skill.
- Removed the obsolete `agents` plugin from the tracked Claude marketplace and
  repository.
- Kept `playwright-cli` Claude-only because Codex already has a better
  user-level `playwright` skill; if that skill needs source control, treat
  a separate `codex-skills` repository as the likely home for a Codex-native
  copy.
- Kept CLI-first policy for both Claude and Codex: use maintained CLIs over MCP
  when workflow coverage, auth, structured output, and write safeguards are
  good enough.

Deferred follow-up: revisit every pull request created in this repository
between 2026-05-10 and 2026-05-15 to check whether Copilot added post-merge
review comments. As of this wrap-down, the GitHub query below returns 45 merged
PRs, from #4 through #62 with gaps where issue numbers were used:

```bash
gh pr list --state all \
  --search "created:2026-05-10..2026-05-15 repo:grailautomation/claude-plugins" \
  --json number,title,state,createdAt,mergedAt,url \
  --limit 100
```

Two Claude marketplace plugins are intentionally not listed for Codex:

| Plugin | Why it is not listed |
| --- | --- |
| `jq-for-clawd` | Claude Code session-history skill; Codex uses different session paths and JSONL shapes, so the Codex-compatible split is `codex-session-history`. |
| `playwright-cli` | Already covered by the user-level Codex `playwright` skill, which has Codex-specific wrapper scripts and policy. Listing this repo copy would mostly create duplicate choices. |

The previous `agents` plugin was removed from the Claude marketplace and repo
after deciding that its Claude subagent bundle duplicated Codex's built-in
agent/delegation patterns and did not need a Codex replacement.

## Current Codex Marketplace

The tracked Codex marketplace exposes these 33 entries. The ten domain packs
are grouped into one row below because they share the same migration pattern:

| Plugin | Status | Rationale |
| --- | --- | --- |
| `spec-kit` | Migrated | High-value workflow plugin; already structured as skills plus bundled scripts; no MCP or connector dependency. |
| `uv-package-manager` | Migrated | Skill-only Python tooling workflow; no plugin-local state or connector dependency. |
| `python-patterns` | Migrated | Skill-only Python reference and review workflow. |
| `openapi-spec-generation` | Migrated | Skill-only OpenAPI workflow with local references. |
| `python-quickbooks` | Migrated | Skill-only library reference; examples use placeholders rather than live credentials. |
| `espanso` | Migrated | Local text-expander config skill. Codex exposure is user-invoked only and keeps preview, backup, confirmation, and verification rules for live machine-state edits. |
| `karabiner-elements` | Migrated | Local keyboard-remapping config skill. Codex exposure is user-invoked only and keeps inspect, preview, backup, confirmation, lint, apply, verify, and rollback rules for live machine-state edits. |
| `salesforce-soql` | Migrated | Salesforce CLI/reference workflow; no bundled MCP and org schemas remain local/ignored. |
| `google-workspace` | Migrated | Broad Gmail, Calendar, Drive, Docs, Sheets, Slides, Tasks, Pub/Sub, and Cloud workflow plugin; Codex and Claude route through the `gws` CLI rather than Google MCP endpoints. |
| Domain packs: `data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` | Migrated with filtered MCP configs | Listed for Codex with `.mcp.codex.json` files that keep remaining reachable hosted HTTP MCP endpoints. High-confidence CLI replacements are omitted from both Claude and Codex MCP configs; pilot and wrapper candidates are tracked in [MCP_CLI_REVIEW.md](MCP_CLI_REVIEW.md). |
| `workato-api` | Migrated | REST reference and curl/httpx execution patterns; credentials come from environment variables or gitignored local notes. |
| `workato-recipe` | Migrated | Script-backed recipe analysis now uses the stable root CLI and avoids Claude-only path/subagent assumptions for Codex. |
| `workato-connector-sdk` | Migrated | Documentation-heavy connector SDK plugin; stale CLI claims and copied token/project examples were corrected before exposure. |
| `workato-platform-cli` | Migrated | Repo copy matches the installed user-level Codex skill; listed with explicit invocation policy because it can manage real Workato assets. |
| `cloudflare` | Migrated | Public CLI-first infrastructure plugin. Prefer `cf` for zones/DNS/Registrar/account APIs and `wrangler` for Workers/Pages/KV/R2/D1. The previous MCP config is preserved as `.mcp.legacy.json` for explicit opt-in only. |
| `namecheap` | Migrated | Public MCP-backed registrar/DNS plugin; credentials and whitelisted IPs stay outside the repo; published `npx` MCP startup lists 8 tools. |
| `context7` | Migrated | Public CLI-backed docs plugin. Use `ctx7 library` and `ctx7 docs` by default; the previous MCP config is preserved as `.mcp.legacy.json` for explicit opt-in compatibility only. |
| `codex-session-history` | Migrated | Codex-specific split from `jq-for-clawd`; uses `~/.codex/sessions` and `~/.codex/archived_sessions` JSONL shapes instead of Claude Code's project session layout. |
| `staff-software-engineer` | Migrated | Claude agent behavior preserved; Codex exposure is a `staff-plan-review` skill rather than a Claude subagent definition. |
| `issue-blaster` | Migrated | Claude slash-command and subagent behavior preserved; Codex exposure uses direct `gh`/`rg` workflows, sequential multi-issue handling by default, and explicit user-authorized subagents only for parallel work. |
| `scraper-generator` | Migrated | Claude slash-command and subagent behavior preserved; Codex exposure runs the analysis, architecture, code-generation, and validation phases inline with local fetch/file/shell tools unless the user explicitly authorizes Codex subagents. |
| `dev-browser` | Migrated | Browser automation server/extension workflow. Listed for Codex after user acceptance of persistent browser-state side effects; standalone mode remains the default and extension mode is intentional opt-in. |

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
| `cloudflare` | Migrated | This repo's Cloudflare plugin is exposed as a CLI-first adapter. It uses `cf`/`wrangler` by default; `flarectl`, `cli4`, and the legacy MCP server are fallback or compatibility paths only. |
| `google-workspace` | Migrated | The broad plugin is now listed for Codex as a CLI-backed integration. It has no `.mcp.json`; use `gws` v0.22.5 or newer on `$PATH`, preserve the existing auth model, and keep side-effect confirmation rules in the plugin README and shared skill. |
| Domain MCP packs | Migrated with filtered MCP configs | `data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, and `sales` are listed for Codex with `.mcp.codex.json` files that preserve remaining hosted HTTP MCP endpoints. BigQuery and Guru now route through maintained CLIs instead of MCP; Linear and Notion have authenticated pilot smoke coverage but still keep MCP pending workflow mapping. Pilot/wrapper candidates are tracked in [MCP_CLI_REVIEW.md](MCP_CLI_REVIEW.md). See [DOMAIN_PACKS_CODEX.md](DOMAIN_PACKS_CODEX.md). |

### Removed Non-Candidates

| Plugin | Decision | Notes |
| --- | --- | --- |
| `agents` | Removed | The bundle was Claude subagent definitions, not a Codex plugin surface. `explore`, `plan`, `general-purpose`, and `bash` duplicated Codex's built-in local/delegated work patterns, and `statusline-setup` edited Claude Code settings. |

### Requires Rewrite Or Connector Review

This bucket is currently empty. New connector-heavy candidates should not be
mechanically exposed by adding manifests only; first map MCP dependencies,
auth/setup expectations, and side-effect classes.

### Initial Residency Calls

These are working classifications, not final deletion decisions:

| Plugin or group | Current residency call | Cleanup implication |
| --- | --- | --- |
| Migrated Codex plugins in the current marketplace | `public-marketplace` or accepted public/personal hybrid | Keep listed; continue validating mechanically. |
| `salesforce-soql` | `split-public-private` | Public SOQL and CLI workflows stay here; org schemas remain ignored/local unless sanitized examples are deliberate. |
| `cloudflare`, `namecheap` | `public-marketplace` | Keep in the public Claude marketplace. Cloudflare is CLI-first by default and keeps MCP as legacy opt-in only; Namecheap remains MCP-backed until a safer CLI/API wrapper is chosen. Credentials, account IDs, whitelisted IPs, and domain lists stay outside the repo in environment variables, account settings, Claude/Codex config, or gitignored local notes. |
| `issue-blaster` | `public-marketplace` | Keep listed for Claude and Codex. Claude keeps slash-command/subagent orchestration; Codex uses direct single-issue `gh`/`rg` analysis and explicit user-authorized subagents only for parallelism. |
| `scraper-generator` | `public-marketplace` | Keep listed for Claude and Codex. Claude keeps slash-command/subagent orchestration; Codex runs phases inline by default and validates generated scrapers with the bundled script. |
| Domain MCP packs | `public-marketplace` with filtered Codex MCP configs | Keep listed for Claude and Codex. Prefer maintained CLIs over MCP whenever a CLI can safely perform the workflow; Gmail, Google Calendar, Google Drive, BigQuery, and Guru route through CLI-backed paths. Codex uses `.mcp.codex.json` per pack for remaining reachable hosted HTTP MCP dependencies and omits endpoints that failed MCP probes instead of substituting native connectors. Linear and Notion are smoke-tested pilots, not replace-now integrations. Pilot and wrapper candidates are tracked in [MCP_CLI_REVIEW.md](MCP_CLI_REVIEW.md). |
| `google-workspace` | `public-marketplace` | Keep as one broad plugin for Claude and Codex. The integration is CLI-backed rather than MCP-backed; require current `gws` auth and side-effect confirmation instead of splitting by product or action class. |
| `jq-for-clawd` / `codex-session-history` | `public-marketplace` split | Keep `jq-for-clawd` as the Claude Code session-history skill; expose `codex-session-history` separately for Codex's distinct session JSONL structure. |
| `espanso` | `public-marketplace` | Keep listed for Claude and Codex. Treat text-expander config as live user machine state: inspect, preview, back up, confirm, apply, and verify. |
| `karabiner-elements` | `public-marketplace` | Keep listed for Claude and Codex. Treat keyboard-remapping config as live user machine state: inspect, preview, back up, confirm, lint when possible, apply, verify, and document rollback. |
| `dev-browser` | `public-marketplace` | Keep listed for Claude and Codex. Standalone browser mode is the default; extension mode intentionally uses logged-in Chrome state when requested. |
| `playwright-cli` | `public-marketplace` Claude-only | Keep listed for Claude. Codex should keep using the user-level `playwright` skill unless a concrete gap appears; that skill has Codex-specific wrapper scripts and headless defaults. |

## Migration Rules

- Add a plugin to `.agents/plugins/marketplace.json` only after its
  `.codex-plugin/plugin.json`, skill metadata, and runtime assumptions have been
  reviewed.
- Preserve the existing asset architecture by default, but prefer maintained
  CLI-backed workflows over MCP when a CLI can safely perform the operation. Do
  not replace an MCP-backed workflow with a native Codex app/connector unless
  there is a documented reason; open a GitHub issue for those exceptions.
- Prefer `skills/<skill>/agents/openai.yaml` for Codex-only invocation policy
  instead of overloading Claude-specific frontmatter.
- Do not copy personal author emails into Codex manifests.
- Keep Codex migration PRs separate from Claude cleanup PRs.
- Validate both surfaces when a plugin remains dual-use: `claude plugin
  validate <plugin>` for Claude and JSON/YAML/frontmatter checks for Codex.
- Browser-control plugins require an explicit side-effect policy before Codex
  listing, especially when they can operate on a persistent browser profile,
  logged-in sessions, cookies, bookmarks, or installed extensions.
- Run `ruby scripts/validate_repo.rb` before proposing or merging repository
  metadata changes.
- Run `ruby scripts/check_cli_integrations.rb` to report local availability for
  CLI-backed replacements. Use `--strict` only for machines expected to have all
  required CLIs; the script does not install anything.

## Skills-Only Plugins → Personal Skills (2026-07-04)

The 13 skills-only plugins (espanso, google-workspace, jq-for-clawd,
karabiner-elements, openapi-spec-generation, playwright-cli, python-patterns,
python-quickbooks, salesforce-soql, uv-package-manager, workato-api,
workato-connector-sdk, workato-platform-cli) were removed from this repo.

- **Claude:** migrated to personal skills at `~/dev/claude-skills`, symlinked into
  `~/.claude/skills/`, default `off` with per-repo `skillOverrides` — granularity that
  plugin-bundled skills cannot provide (plugin skills are all-or-nothing).
- **Codex:** mirrored into the local `claude-code-skills` plugin
  (`~/dev/codex-skills/plugins/claude-code-skills`, marketplace `local-codex-skills`),
  so Codex retains access independent of this repo.
- Removed from both `.claude-plugin/marketplace.json` (Claude) and
  `.agents/plugins/marketplace.json` (Codex `grail-dev` source); the latter also
  dropped the pre-existing dead `terminal-tidbits`/`oasb-scaffold` entries.
