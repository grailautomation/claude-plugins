# MCP Inventory

This inventory reflects tracked default `.mcp.json` files, explicitly preserved
legacy MCP configs, and deliberate MCP-to-CLI replacements in this repository.
It is not a Codex migration approval list. This repo is CLI-first: when a
maintained CLI can safely perform a workflow, prefer that CLI over MCP for both
Claude and Codex. See [MCP_CLI_REVIEW.md](MCP_CLI_REVIEW.md) for the broader
CLI replacement ledger.

MCP remains appropriate when no usable CLI exists, the CLI cannot express the
operation safely, or the MCP server is itself the plugin's core value. Google
Workspace is the concrete enforced case here: Gmail, Google Calendar, and
Google Drive route through the `google-workspace` plugin and `gws` CLI rather
than Gmail/GCal/GDrive MCP endpoints.

Connector-heavy domain pack review is resolved in
[issue #25](https://github.com/grailautomation/claude-plugins/issues/25). See
[DOMAIN_PACKS_CODEX.md](DOMAIN_PACKS_CODEX.md) for pack-level Codex mappings,
omissions, and side-effect expectations.

## Current Servers and CLI Replacements

| Server | Kind | Current config | Used by | Env vars | Current disposition |
| --- | --- | --- | --- | --- | --- |
| `amplitude` | HTTP MCP | `https://mcp.amplitude.com/mcp` | `data`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `apollo` | HTTP MCP | `https://api.apollo.io/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `asana` | HTTP MCP | `https://mcp.asana.com/v2/mcp` | `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `atlassian` | HTTP MCP | `https://mcp.atlassian.com/v1/mcp` | `data`, `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `bigquery` | removed HTTP MCP | Previously `https://bigquery.googleapis.com/mcp` | `data`, `finance` |  | Default path is the Google Cloud SDK `bq` CLI. Removed from Claude and Codex domain MCP configs; use `bq --format=json`, `--dry_run`, and byte caps for safe workflows. |
| `clay` | HTTP MCP | `https://api.clay.com/v3/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `clickup` | HTTP MCP | `https://mcp.clickup.com/mcp` | `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `close` | HTTP MCP | `https://mcp.close.com/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `cloudflare` | legacy local npm MCP | `npx -y @grailautomation/cloudflare-mcp` via `cloudflare/.mcp.legacy.json` | `cloudflare` | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` | Default plugin path is CLI-first: use `cf` for zones/DNS/Registrar/account APIs and `wrangler` for Workers/Pages/KV/R2/D1. Legacy MCP startup previously passed with 28 tools and is preserved for explicit opt-in only. |
| `context7` | legacy local npm MCP | `npx -y @upstash/context7-mcp` via `context7/.mcp.legacy.json` | `context7` |  | Default path is the `ctx7` CLI. The legacy MCP config is preserved for explicit opt-in compatibility only. |
| `datadog` | HTTP MCP | `https://mcp.datadoghq.com/mcp` | `engineering` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `docusign` | HTTP MCP | `https://mcp.docusign.com/mcp` | `legal` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `figma` | HTTP MCP | `https://mcp.figma.com/mcp` | `design`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `fireflies` | HTTP MCP | `https://api.fireflies.ai/mcp` | `product-management`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `guru` | removed HTTP MCP | Previously `https://mcp.api.getguru.com/mcp` | `enterprise-search` |  | Default path is the Guru CLI (`guru` / `@getguru/cli`). Removed from Claude and Codex enterprise-search MCP configs. |
| `hex` | HTTP MCP | `https://app.hex.tech/mcp` | `data` |  | Pilot the official `hex` CLI for projects/apps/cells/runs; keep MCP until Hex Agent thread workflows are mapped. |
| `hubspot` | HTTP MCP | `https://mcp.hubspot.com/anthropic` | `legal`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `intercom` | HTTP MCP | `https://mcp.intercom.com/mcp` | `design`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `linear` | HTTP MCP | `https://mcp.linear.app/mcp` | `design`, `engineering`, `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `monday` | HTTP MCP | `https://mcp.monday.com/mcp` | `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `ms365` | HTTP MCP | `https://microsoft365.mcp.claude.com/mcp` | `enterprise-search`, `finance`, `operations`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `namecheap` | local npm MCP | `npx -y @grailautomation/namecheap-mcp` | `namecheap` | `NAMECHEAP_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_USERNAME` | Public Claude and Codex plugin; npm package exists at `0.1.0`; published `npx` tools/list smoke passed with 8 tools |
| `notion` | HTTP MCP | `https://mcp.notion.com/mcp` | `design`, `engineering`, `enterprise-search`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Pilot the official `ntn` CLI for page/data-source/file workflows; keep MCP until Notion AI search and plan-gated tool coverage are mapped. |
| `outreach` | HTTP MCP | `https://mcp.outreach.io/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `pagerduty` | HTTP MCP | `https://mcp.pagerduty.com/mcp` | `engineering` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `pendo` | HTTP MCP | `https://app.pendo.io/mcp/v0/shttp` | `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `servicenow` | HTTP MCP for Claude, omitted for Codex | `https://mcp.servicenow.com/mcp` | `operations` |  | Pilot the official `snc` CLI for generic ITSM table/record workflows. Claude keeps MCP pending pilot; Codex omits the unresolved shared endpoint. |
| `similarweb` | HTTP MCP | `https://mcp.similarweb.com/mcp` | `product-management`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `slack` | HTTP MCP | `https://mcp.slack.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `zoominfo` | HTTP MCP | `https://mcp.zoominfo.com/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |

## Hosted HTTP MCP Dispositions

The connector-heavy domain packs use MCP for non-Google hosted providers and
the `google-workspace` / `gws` CLI path for Gmail, Google Calendar, and Google
Drive. Codex uses pack-local `.mcp.codex.json` files that include only
endpoints that responded to a non-auth MCP `initialize` probe with either
initialize success or an auth/RBAC challenge. Endpoints that returned `404` or
failed DNS resolution are intentionally omitted from Codex configs until a
specific issue chooses a fix or replacement. High-confidence CLI replacements
are removed from both Claude and Codex MCP configs even if the hosted MCP probe
previously succeeded.

| Server | Codex disposition | Auth/setup expectation |
| --- | --- | --- |
| `amplitude` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `apollo` | Omitted from Codex filtered configs | The configured URL returned `404`; Apollo's public MCP guidance points users to hosted connector directories rather than a stable server URL to commit. |
| `asana` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `atlassian` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `bigquery` | Removed from domain MCP configs | Use the Google Cloud SDK `bq` CLI for BigQuery workflows. Do not re-add BigQuery MCP unless a future issue documents why `bq` is insufficient. |
| `clay` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user login/OAuth setup required. |
| `clickup` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `close` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `datadog` | Included in filtered Codex MCP configs with corrected Codex URL | Original Claude URL returned `404`; Codex uses `https://mcp.datadoghq.com/api/unstable/mcp-server/mcp`, which reached an auth challenge. User OAuth/token setup required. |
| `docusign` | Included in filtered Codex MCP configs | Endpoint reached RBAC access denial; user auth and account/RBAC setup required. |
| `figma` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `fireflies` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `github` | Removed from engineering MCP configs | Use the `gh` CLI for GitHub work in Claude and Codex. Do not add GitHub MCP unless a future issue documents why CLI is insufficient. |
| `gmail` | Removed from domain-pack MCP configs | Use the separate `google-workspace` CLI plugin and `gws gmail` for Google Workspace work. Do not add Gmail MCP unless a future issue documents why CLI is insufficient. |
| `google-calendar` | Removed from domain-pack MCP configs | Use the separate `google-workspace` CLI plugin and `gws calendar` for Google Workspace work. Do not add Google Calendar MCP unless a future issue documents why CLI is insufficient. |
| `google-drive` | Removed from domain-pack MCP configs | Use the separate `google-workspace` CLI plugin and `gws drive` for Google Workspace work. Do not add Google Drive MCP unless a future issue documents why CLI is insufficient. |
| `guru` | Removed from domain MCP configs | Use the Guru CLI for Guru search and card workflows. Do not re-add Guru MCP unless a future issue documents why the CLI is insufficient. |
| `hex` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; pilot the official Hex CLI before removing MCP because Hex Agent thread workflows may still require MCP. |
| `hubspot` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `intercom` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `linear` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `monday` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `ms365` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; Microsoft auth setup required. |
| `notion` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; pilot the official Notion `ntn` CLI before removing MCP because Notion AI search and plan-gated tool coverage still need mapping. |
| `outreach` | Included in filtered Codex MCP configs with corrected Codex URL | Original Claude host did not resolve; Codex uses `https://api.outreach.io/mcp/`, which reached an auth challenge. Outreach Amplify/org enablement and user auth required. |
| `pagerduty` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `pendo` | Omitted from Codex filtered configs | The existing URL did not resolve from this network, and Pendo documents regional MCP URLs that must match the user's sign-in hostname; no universal public default is committed. |
| `servicenow` | Included in Claude MCP config; omitted from Codex filtered configs | The configured shared host did not resolve for Codex, while Claude retains the existing config pending the `snc` CLI pilot. ServiceNow also documents instance-generated server URLs of the form `https://<instance>.service-now.com/sncapps/mcp-server/mcp/<server-name>`. |
| `similarweb` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; API key or bearer-token setup required. |
| `slack` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token/OAuth setup required. |
| `zoominfo` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |

Side-effect expectations for the domain packs are documented in
[DOMAIN_PACKS_CODEX.md](DOMAIN_PACKS_CODEX.md). Authenticated live workflow
smoke tests remain install/runtime validation because they require user-specific
SaaS OAuth, scopes, workspaces, and target records.

## Review Rules

- Do not list connector-heavy plugins for Codex by adding manifests only.
- Treat CLI-backed integrations as the default source of truth when a maintained
  CLI exists and can safely perform the workflow.
- Run `ruby scripts/check_cli_integrations.rb` to report whether CLI-backed
  replacements are available on the current machine. Use `--strict` only when
  validating an environment that is expected to have all required CLIs.
- For HTTP MCP servers, verify runtime support, auth setup, and side effects
  before listing the owning plugin.
- For local npm MCP servers, verify package name, package manager/lockfile,
  environment variables, and startup behavior before deciding whether the plugin
  is public or personal/local.
- For Cloudflare, prefer the CLI stack over MCP: `cf` for zones, DNS,
  Registrar, Accounts, and generated API-backed commands; `wrangler` for
  Workers, Pages, KV, R2, D1, Queues, and local development; `flarectl` or
  `cli4` only as fallback surfaces.
- For Microsoft endpoints, call out any proposed native Codex connector
  substitution in a GitHub issue before changing the migration plan.
- For Gmail, Google Calendar, and Google Drive in Claude or Codex, use the
  `google-workspace` plugin and `gws` CLI over MCP. Open an issue only if a
  workflow cannot be represented safely through the CLI.
