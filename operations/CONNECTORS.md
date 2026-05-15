# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~ITSM` might mean ServiceNow, Zendesk, or any other service management tool with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (ITSM, project tracker, knowledge base, etc.) rather than specific products. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. Use `gws gmail`, `gws calendar`, `gws drive`, or `gws docs` for Google
Workspace after checking `gws auth status`. Use MCP when no usable CLI exists,
the CLI cannot express the operation safely, or the workflow depends on
MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Default integrations | Other options |
|----------|-------------|-----------------|---------------|
| Calendar | `~~calendar` | Google Calendar via `gws` CLI | Microsoft 365 |
| Chat | `~~chat` | Slack MCP | Microsoft Teams |
| Email | `~~email` | Gmail via `gws` CLI, Microsoft 365 MCP | — |
| ITSM | `~~ITSM` | ServiceNow MCP; pilot official ServiceNow `snc` client for generic record workflows | Zendesk, Freshservice, Jira Service Management |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files, Atlassian MCP (Confluence) | Guru, Coda |
| Project tracker | `~~project tracker` | Asana MCP, Atlassian MCP (Jira) | Linear, monday.com, ClickUp |
| Procurement | `~~procurement` | — | Coupa, SAP Ariba, Zip |
| Office suite | `~~office suite` | Microsoft 365 | Google Workspace via `gws` CLI |
