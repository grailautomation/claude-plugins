# Domain Packs Codex Mapping

This document records the Codex mapping for the connector-heavy domain packs:
`data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`,
`operations`, `product-management`, `productivity`, and `sales`.

This repo is CLI-first for Claude and Codex. When a maintained CLI can safely
perform a workflow, prefer that CLI over MCP. Google Workspace is handled
through the `google-workspace` plugin and `gws` CLI. Domain-pack `.mcp.json`
files keep remaining MCP dependencies only. Codex additionally uses
`.mcp.codex.json`, which includes only remaining hosted HTTP MCP endpoints that
responded to a non-auth MCP `initialize` probe with either a valid initialize
response or an auth/RBAC challenge. High-confidence CLI replacements are omitted
from both Claude and Codex MCP configs.

## Mapping Rules

- Prefer a maintained CLI over hosted MCP whenever the CLI can safely perform
  the workflow. Do not replace a hosted MCP dependency with a native app or
  connector in these packs unless a specific issue documents the exception.
- Gmail, Google Calendar, and Google Drive are handled through the
  `google-workspace` plugin and `gws` CLI in Claude and Codex, not through MCP.
  Domain-pack skills may still use `~~email`, `~~calendar`, and
  `~~cloud storage` as source labels, but Google-backed execution should route
  to `gws gmail`, `gws calendar`, or `gws drive` after checking auth with
  `gws auth status`.
- Auth is install/runtime user setup. Most included endpoints returned an OAuth,
  bearer-token, API-key, or RBAC challenge during unauthenticated probing.
- Endpoints that returned `404`, failed DNS resolution, or otherwise did not
  behave like reachable MCP servers are omitted from `.mcp.codex.json`.
- Omitted non-Google endpoints either stay in the Claude `.mcp.json` until a
  separate issue decides their fate, or are removed when a CLI-backed path has
  been chosen and documented.
- Side-effect boundaries stay workflow-level, not plugin boundaries. Commands
  that write, send, share, invite, watch, subscribe, renew, administer, or change
  external state require user confirmation before execution.

## Pack Decisions

| Pack | Codex MCP config | Included for Codex | Omitted from Codex |
| --- | --- | --- | --- |
| `data` | `.mcp.codex.json` | `hex`, `amplitude`, `atlassian` | `bigquery` |
| `design` | `.mcp.codex.json` | `slack`, `figma`, `linear`, `asana`, `atlassian`, `notion`, `intercom` | `google-calendar`, `gmail` |
| `engineering` | `.mcp.codex.json` | `slack`, `linear`, `asana`, `atlassian`, `notion`, `pagerduty`, `datadog` | `github`, `google-calendar`, `gmail` |
| `enterprise-search` | `.mcp.codex.json` | `slack`, `notion`, `atlassian`, `asana`, `ms365` | `guru`, `google-calendar`, `gmail` |
| `finance` | `.mcp.codex.json` | `slack`, `ms365` | `bigquery`, `google-calendar`, `gmail` |
| `legal` | `.mcp.codex.json` | `slack`, `docusign`, `hubspot`, `notion` | `google-calendar`, `gmail`, `google-drive` |
| `operations` | `.mcp.codex.json` | `slack`, `notion`, `atlassian`, `asana`, `ms365` | `google-calendar`, `gmail`, `servicenow` |
| `product-management` | `.mcp.codex.json` | `slack`, `linear`, `asana`, `monday`, `clickup`, `atlassian`, `notion`, `figma`, `amplitude`, `intercom`, `fireflies`, `similarweb` | `pendo`, `google-calendar`, `gmail` |
| `productivity` | `.mcp.codex.json` | `slack`, `notion`, `asana`, `linear`, `atlassian`, `ms365`, `monday`, `clickup` | `google-calendar`, `gmail` |
| `sales` | `.mcp.codex.json` | `slack`, `hubspot`, `close`, `clay`, `zoominfo`, `notion`, `atlassian`, `fireflies`, `ms365`, `outreach`, `similarweb` | `apollo`, `google-calendar`, `gmail` |

## Side-Effect Expectations

| Class | Examples | Runtime expectation |
| --- | --- | --- |
| Read-only | Search, analysis, dashboard review, design critique, CRM lookup, knowledge synthesis | May run after auth is available; cite sources and avoid exporting sensitive data unnecessarily. |
| Write/send/share/invite | Slack or Chat posts, Gmail or Microsoft 365 sends, Drive or DocuSign sharing, project-tracker updates, CRM updates | Confirm the exact target, content, and audience before execution. Prefer drafts or dry-runs where available. |
| Watch/automation | Event watches, digest jobs, workflow syncs, recurring updates, project-tracker automations | Confirm persistence, cleanup behavior, ownership, and notification scope before execution. |
| Admin/security | BigQuery admin actions, DocuSign RBAC-sensitive actions, ServiceNow-style changes, security/compliance operations | Require explicit user authorization and least-privilege auth. Stop if the connector cannot show scope or target clearly. |

## Probe Summary

The Codex mapping was initially based on unauthenticated MCP `initialize`
probes. Included endpoints returned `200` initialize success or `401`/`403`
auth challenges that indicate a reachable MCP surface. Some Codex endpoints
intentionally differ from the corresponding Claude `.mcp.json` value when the
Claude value failed probing and a current public vendor endpoint was available:

- `datadog`: Codex uses `https://mcp.datadoghq.com/api/unstable/mcp-server/mcp`.
- `outreach`: Codex uses `https://api.outreach.io/mcp/`.

Remaining omitted endpoints have these final dispositions:

- `apollo`: the configured URL returned `404`; Apollo's public MCP guidance points
  users to hosted connector directories rather than a stable server URL to commit.
- `bigquery`: handled through the Google Cloud SDK `bq` CLI in Claude and Codex
- `guru`: handled through the Guru CLI in Claude and Codex
- `github`: handled through the `gh` CLI for GitHub work in Claude and Codex
- `gmail`: handled by the `google-workspace` plugin and `gws gmail` in Claude
  and Codex
- `google-calendar`: handled by the `google-workspace` plugin and
  `gws calendar` in Claude and Codex
- `google-drive`: handled by the `google-workspace` plugin and `gws drive` in
  Claude and Codex
- `pendo`: no universal default; the documented Pendo MCP URL is regional and
  must match the user's sign-in hostname
- `servicenow`: omitted from Codex because the configured shared MCP host did
  not resolve and ServiceNow documents instance-generated server URLs of the
  form
  `https://<instance>.service-now.com/sncapps/mcp-server/mcp/<server-name>`.
  Claude retains the existing config pending the `snc` CLI pilot.

Pilot CLI candidates are tracked in [MCP_CLI_REVIEW.md](MCP_CLI_REVIEW.md).
Do not remove `hex`, `notion`, or `servicenow` MCP configs solely because a CLI
exists; their CLI paths still need smoke tests and workflow coverage mapping.
