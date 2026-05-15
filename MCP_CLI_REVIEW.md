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
| `hex` | Pilot | official `hex` CLI | Pilot workspace/project/cell/run/connection inventory and controlled draft operations. Keep MCP for Agent thread create/continue and natural-language exploration workflows. |
| `notion` | Pilot | official `ntn` CLI | Pilot page, data-source, file, and raw API workflows. Keep MCP for Notion AI search, connected-source search, and database-view workflows. |
| `servicenow` | Pilot | official `snc` CLI | Pilot generic record query/get/create/update/delete only with the ServiceNow `snc` client. Keep MCP for instance-specific MCP servers and Now Assist-style workflows. |
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

`ruby scripts/check_cli_integrations.rb` is a local availability check, not an
installer. For ambiguous command names, it verifies the binary identity before
reporting an installed command so unrelated packages such as npm `hex` or npm
`snc` are not accepted by accident.

For non-mutating authenticated/runtime checks, use
`ruby scripts/smoke_cli_integrations.rb`. This live smoke script is intentionally
separate from the availability checker because it can call SaaS APIs, read local
auth stores, and invoke one-off `pnpm dlx`/`npx` commands. Run a single check
with `--only <key>` when validating one integration.

BigQuery is the current service-account-backed smoke path. Set
`GCP_SERVICE_ACCOUNT_OP_REF=op://<vault>/<item>/<field>` to a 1Password field
containing a Google service-account JSON key. The smoke script writes it to a
mode `0600` temp file, runs `bq` with
`CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`, and removes the file when done.
`GOOGLE_APPLICATION_CREDENTIALS` remains appropriate for ADC/client-library
code, but `bq`/Cloud SDK commands need `CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`
to reliably use the service-account key instead of the active user account.

Notion has a read-only smoke path for the `ntn` pilot. Set
`NOTION_API_TOKEN_OP_REF=op://<vault>/<item>/<field>` to a 1Password field
containing the Notion API token. The smoke script verifies `ntn doctor`, API
endpoint discovery, `v1/users/me`, workspace search, page retrieval when search
returns a page, and file listing. Passing this smoke test does not make Notion
a replace-now integration because Notion MCP still covers Notion AI search,
connected-source search, and database-view workflows.

## Pilot Findings

### Hex

The official Hex CLI is a useful pilot, but it is not a full MCP replacement
yet. Official install paths are `brew install hex-inc/hex-cli/hex` or the Hex
install script; do not use the unrelated npm package named `hex`. Use
`hex --json ...` for agent-readable output and `hex auth status` before live
workflows.

Good CLI pilot workflows are read-heavy workspace inspection and bounded
operations such as `hex --json project list`, `hex --json project get`,
`hex --json project export`, `hex --json cell list`, `hex --json connection
list`, and run status checks. The MCP still carries Hex Agent Thread workflows:
project semantic search, `create_thread`, `get_thread`, and
`continue_thread`, including generated charts/tables and follow-up analysis.

### Notion

The official Notion CLI is a strong pilot for page, data-source, file, and raw
API workflows. Official install paths are `curl -fsSL https://ntn.dev | bash`
or `npm install --global ntn`; Node.js 22+ and npm 10+ are required for the npm
path. Use `ntn doctor` for setup/auth health and prefer JSON-capable commands
such as `ntn api ls --json`, `ntn pages get <page-id> --json`, and
`ntn datasources query <data-source-id> --filter ... --json`.

Authenticated read-only smoke tests passed locally through `pnpm dlx ntn` using
a 1Password-sourced `NOTION_API_TOKEN`: `ntn doctor`, `ntn api ls --json`,
`ntn api v1/users/me`, `ntn api v1/search page_size:=5`, `ntn pages get
<page-id> --json` from a search result, and `ntn files list --json`.

Keep Notion MCP until authenticated parity is proven for Notion AI search,
connected-source search, database-view queries, and higher-level agent tools.
The CLI is better for file upload workflows, but raw `ntn api` write calls are
powerful and still require explicit user confirmation.

### ServiceNow

ServiceNow currently has two different command-line surfaces that are easy to
confuse:

- `snc` is the ServiceNow CLI documented for instance connection profiles,
  JSON output, and record CRUD/query commands such as `snc record query`.
- `@servicenow/cli` exposes `now-cli` and is oriented around UI/component app
  development, not generic ITSM table workflows.

Do not install or run the unrelated npm package named `snc`. Pilot ServiceNow
CLI replacement only when the ServiceNow Store/GitHub `snc` client is available
and `snc configure profile list --output json` plus read-only record queries
pass against the target instance. Keep MCP for instance-generated MCP servers,
Now Assist-style workflows, and any workflow that needs server-side tools not
covered by generic record operations.

## Wrapper Gates

Before replacing MCP with a repo-owned wrapper:

1. Define the smallest useful workflow set.
2. Prefer read-only commands first.
3. Make destructive commands require explicit confirmation and target IDs.
4. Keep credentials in environment variables or local CLI auth stores.
5. Emit JSON by default or with a documented `--json`/`--ndjson` flag.
6. Document scopes, rate limits, credit consumption, and paid-plan limitations.
