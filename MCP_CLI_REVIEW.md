# MCP CLI Replacement Review

This ledger records the broad CLI-based review of remaining MCP dependencies.
It uses a wider definition than "stable official vendor CLI": vendor technical
previews, official API CLIs, mature community CLIs, Terraform/IaC providers,
generic API clients, and feasible repo-owned wrappers all count as candidates.

Do not remove MCP from a plugin just because a CLI candidate exists. Remove MCP
only after the CLI path is validated for auth, JSON/NDJSON output, read-only
inspection, write safeguards, and the concrete workflows used by the plugin.

## Verdicts

| Vendor | Verdict | CLI-based path | Action |
| --- | --- | --- | --- |
| `cloudflare` | Replace now | `cf`, `wrangler`; `flarectl`/`cli4` fallback | Plugin is CLI-first. Legacy MCP is `.mcp.legacy.json` only. |
| `bigquery` | Replace now | `bq` CLI | Remove from domain MCP configs; use dry runs, byte caps, and explicit write confirmation. |
| `context7` | Replace now | `ctx7` CLI | Plugin is CLI-first. Legacy MCP is `.mcp.legacy.json` only. |
| `guru` | Replace now | `@getguru/cli` | Remove Guru MCP from enterprise-search; validate CLI auth/source before broad installs. |
| `amplitude` | Pilot | `@amplitude/wizard`, `@amplitude/ampli`, APIs | Pilot for setup/instrumentation; keep MCP for analytics querying until proven otherwise. |
| `atlassian` | Pilot | TWG CLI beta, `acli`, `jira-cli` | Pilot TWG for Jira/Confluence cross-product workflows before removing MCP. |
| `clickup` | Pilot | `@krodak/clickup-cli` / `cup` | Pilot read/write workflows with source review and JSON checks. |
| `linear` | Pilot | `@schpet/linear-cli`, `@kyaukyuai/linear-cli` | Pilot issue/project/comment/doc workflows; compare dry-run and receipt support. |
| `datadog` | Pilot | Dogshell, `agent-datadog`, `@leoflores/datadog-cli`, Terraform, `datadog-ci` | Pilot incident/observability reads; keep MCP for advanced toolsets until mapped. |
| `pagerduty` | Pilot | `pd`, Terraform, Pulumi | Pilot incidents/services/schedules/config; keep MCP for incident insights/status/workflow tools. |
| `ms365` | Pilot | `m365`, `msgraph`, Graph PowerShell | Pilot with explicit read-only scopes and write boundary mapping. |
| `clay` | Pilot | `clay-gtm-cli` | Pilot webhook-table workflows; keep MCP for Clay Functions/admin credit controls until mapped. |
| `close` | Pilot | `close-crm-cli`, Close REST/OpenAPI | Pilot CRM reads/writes in isolated mode; require confirmation for writes. |
| `fireflies` | Pilot | `ffcli`, GraphQL API | Pilot read-only transcript workflows; keep MCP for management/soundbite/channel workflows. |
| `hubspot` | Pilot | community `hubspot-cli`, `g-gremlin`; official `hs` only for dev/CMS | Pilot CRM operations; do not treat official `hs` as CRM replacement. |
| `intercom` | Pilot | official `@intercom/cli`, OpenAPI | Strong pilot candidate; likely replace after auth/read/write smoke tests. |
| `hex` | Pilot | official `hex` CLI | Keep MCP for Hex Agent thread workflows until CLI coverage is confirmed. |
| `notion` | Pilot | official `ntn` CLI | Keep MCP until Notion AI search/tool coverage is mapped; pilot page/data-source/file workflows. |
| `servicenow` | Pilot | official `snc` CLI | Pilot generic ITSM table CRUD; keep MCP for Now Assist or instance-specific workflows. |
| `asana` | Wrapper candidate | Asana REST/API client wrapper; community CLIs are partial | Build/pilot wrapper only if broad Work Graph workflows are needed without MCP. |
| `monday` | Wrapper candidate | GraphQL API wrapper; official `mapps` is app-dev only | Build wrapper for board/item/docs workflows before removing MCP. |
| `slack` | Wrapper candidate | Slack Web API wrapper; official Slack CLI is app-dev only | Do not use browser-token CLIs. Keep MCP until scoped Web API wrapper exists. |
| `pendo` | Wrapper candidate | Engage/Aggregation/Data Sync API wrapper | API supports useful reads, but service-account notes favor MCP today. |
| `similarweb` | Wrapper candidate | Similarweb V5 REST/Batch API wrapper | Build read-only wrapper for common market-intelligence reads before removing MCP. |
| `apollo` | Wrapper candidate | Apollo REST wrapper; `g-gremlin` for enrichment | API covers pieces; no strong Apollo-specific CLI found. |
| `outreach` | Wrapper candidate | Outreach REST/S2S wrapper; `g-gremlin` for pushes | Keep MCP for revenue-context/Kaia/Q&A until wrapper is designed. |
| `zoominfo` | Wrapper candidate | ZoomInfo API wrapper; `g-gremlin` for enrichment | API access is gated; validate authenticated docs before replacement. |
| `docusign` | Wrapper candidate | DocuSign SDK/OpenAPI wrapper | Build safe draft/send/status/download wrapper before removing MCP. |
| `namecheap` | Wrapper candidate | Namecheap API wrapper; Terraform for managed DNS | Existing MCP is thin API wrapper; CLI should preserve read-modify-write DNS safeguards. |
| `figma` | Keep MCP | Code Connect CLI and export tools are adjuncts only | MCP remains the maintained design-context/canvas workflow. |

## Pilot Gates

Before moving any `Pilot` vendor to "replace now":

1. Check install lanes with `type -a`, `which -a`, and package-manager metadata.
2. Prefer `pnpm dlx`, Homebrew, or project-local commands over new global installs.
3. Inspect source/package ownership and recent maintenance.
4. Run read-only auth/status and list/search smoke tests.
5. Verify JSON or NDJSON output that an agent can parse safely.
6. Verify dry-run, preview, or confirmation boundaries for writes.
7. Update both Claude and Codex configs in the same direction unless a documented runtime limitation prevents parity.

## Wrapper Gates

Before replacing MCP with a repo-owned wrapper:

1. Define the smallest useful workflow set.
2. Prefer read-only commands first.
3. Make destructive commands require explicit confirmation and target IDs.
4. Keep credentials in environment variables or local CLI auth stores.
5. Emit JSON by default or with a documented `--json`/`--ndjson` flag.
6. Document scopes, rate limits, credit consumption, and paid-plan limitations.
