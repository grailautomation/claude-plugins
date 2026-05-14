# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~chat` might mean Slack, Microsoft Teams, or any other chat tool with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, email, cloud storage, etc.) rather than specific products. The `.mcp.json` pre-configures fallback MCP servers, but any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. When `~~email`, `~~calendar`, or `~~cloud storage` means Google
Workspace, use the `google-workspace` plugin and `gws` CLI after checking
`gws auth status`. Use MCP when no usable CLI exists, the CLI cannot express the
operation safely, or the workflow depends on MCP-only capabilities.

This plugin uses `~~category` references extensively as source labels in search output (e.g. `~~chat:`, `~~email:`). These are intentional — they represent dynamic category markers that resolve to whatever tool is connected.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams, Discord |
| Email | `~~email` | Microsoft 365 | — |
| Cloud storage | `~~cloud storage` | Microsoft 365 | Dropbox |
| Knowledge base | `~~knowledge base` | Notion, Guru | Confluence, Slite |
| Project tracker | `~~project tracker` | Atlassian (Jira/Confluence), Asana | Linear, monday.com |
| CRM | `~~CRM` | *(not pre-configured)* | Salesforce, HubSpot |
| Office suite | `~~office suite` | Microsoft 365 | Google Workspace via `gws` CLI |
