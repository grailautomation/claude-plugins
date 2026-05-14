# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The `.mcp.json` pre-configures fallback MCP servers, but any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. Use `gws gmail`, `gws calendar`, `gws drive`, or `gws docs` for Google
Workspace after checking `gws auth status`. Use MCP when no usable CLI exists,
the CLI cannot express the operation safely, or the workflow depends on
MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Calendar | `~~calendar` | Google Calendar via `gws` CLI, Microsoft 365 | — |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Competitive intelligence | `~~competitive intelligence` | Similarweb | Crayon, Klue |
| CRM | `~~CRM` | HubSpot, Close | Salesforce, Pipedrive, Copper |
| Data enrichment | `~~data enrichment` | Clay, ZoomInfo, Apollo | Clearbit, Lusha |
| Email | `~~email` | Gmail via `gws` CLI, Microsoft 365 | — |
| Knowledge base | `~~knowledge base` | Notion | Confluence, Guru |
| Meeting transcription | `~~conversation intelligence` | Fireflies | Gong, Chorus, Otter.ai |
| Project tracker | `~~project tracker` | Atlassian (Jira/Confluence) | Linear, Asana |
| Sales engagement | `~~sales engagement` | Outreach | Salesloft, Apollo |
