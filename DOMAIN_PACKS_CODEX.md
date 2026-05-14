# Domain Packs Codex Mapping

This document records the Codex mapping for the connector-heavy domain packs:
`data`, `design`, `engineering`, `enterprise-search`, `finance`, `legal`,
`operations`, `product-management`, `productivity`, and `sales`.

The Claude marketplace behavior is preserved. Each pack keeps its original
`.mcp.json`. Codex uses `.mcp.codex.json`, which includes only hosted HTTP MCP
endpoints that responded to a non-auth MCP `initialize` probe with either a
valid initialize response or an auth/RBAC challenge.

## Mapping Rules

- Do not replace a hosted MCP dependency with a native Codex app or connector in
  these packs unless a specific issue documents the exception.
- Auth is install/runtime user setup. Most included endpoints returned an OAuth,
  bearer-token, API-key, or RBAC challenge during unauthenticated probing.
- Endpoints that returned `404`, failed DNS resolution, or otherwise did not
  behave like reachable MCP servers are omitted from `.mcp.codex.json`.
- Omitted endpoints stay in the Claude `.mcp.json` until a separate issue decides
  whether to fix, replace, or remove them.
- Side-effect boundaries stay workflow-level, not plugin boundaries. Commands
  that write, send, share, invite, watch, subscribe, renew, administer, or change
  external state require user confirmation before execution.

## Pack Decisions

| Pack | Codex MCP config | Included for Codex | Omitted from Codex |
| --- | --- | --- | --- |
| `data` | `.mcp.codex.json` | `bigquery`, `hex`, `amplitude`, `atlassian` | None |
| `design` | `.mcp.codex.json` | `slack`, `figma`, `linear`, `asana`, `atlassian`, `notion`, `intercom` | `google-calendar`, `gmail` |
| `engineering` | `.mcp.codex.json` | `slack`, `linear`, `asana`, `atlassian`, `notion`, `github`, `pagerduty`, `datadog` | `google-calendar`, `gmail` |
| `enterprise-search` | `.mcp.codex.json` | `slack`, `notion`, `guru`, `atlassian`, `asana`, `ms365` | `google-calendar`, `gmail` |
| `finance` | `.mcp.codex.json` | `bigquery`, `slack`, `ms365` | `google-calendar`, `gmail` |
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

The Codex mapping was based on unauthenticated MCP `initialize` probes. Included
endpoints returned `200` initialize success or `401`/`403` auth challenges that
indicate a reachable MCP surface. Some Codex endpoints intentionally differ from
the preserved Claude `.mcp.json` because the Claude value failed probing and a
current public vendor endpoint was available:

- `datadog`: Codex uses `https://mcp.datadoghq.com/api/unstable/mcp-server/mcp`.
- `github`: Codex uses `https://api.githubcopilot.com/mcp/`.
- `outreach`: Codex uses `https://api.outreach.io/mcp/`.

Remaining omitted endpoints have these final dispositions:

- `apollo`: the configured URL returned `404`; Apollo's public MCP guidance points
  users to hosted connector directories rather than a stable server URL to commit.
- `gmail`: `404` from the Claude-hosted endpoint
- `google-calendar`: `404` from the Claude-hosted endpoint
- `google-drive`: DNS resolution failure for the configured Claude-hosted
  endpoint
- `pendo`: no universal default; the documented Pendo MCP URL is regional and
  must match the user's sign-in hostname
- `servicenow`: the configured shared host did not resolve; ServiceNow documents
  instance-generated server URLs of the form
  `https://<instance>.service-now.com/sncapps/mcp-server/mcp/<server-name>`
