# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean Salesforce, HubSpot, or any other CRM with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, chat, email, etc.) rather than specific products. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. Use `gws gmail`, `gws calendar`, `gws drive`, or `gws docs` for Google
Workspace after checking `gws auth status`. Use MCP when no usable CLI exists,
the CLI cannot express the operation safely, or the workflow depends on
MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Default integrations | Other options |
|----------|-------------|-----------------|---------------|
| Calendar | `~~calendar` | Google Calendar via `gws` CLI, Microsoft 365 | — |
| Chat | `~~chat` | Slack MCP | Microsoft Teams |
| Competitive intelligence | `~~competitive intelligence` | Similarweb MCP | Crayon, Klue |
| CRM | `~~CRM` | HubSpot MCP, Close MCP | Salesforce, Pipedrive, Copper |
| Data enrichment | `~~data enrichment` | Clay MCP, ZoomInfo MCP, Apollo MCP | Clearbit, Lusha |
| Email | `~~email` | Gmail via `gws` CLI, Microsoft 365 | — |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files | Confluence, Guru |
| Meeting transcription | `~~conversation intelligence` | Fireflies MCP | Gong, Chorus, Otter.ai |
| Project tracker | `~~project tracker` | Atlassian MCP (Jira/Confluence) | Linear, Asana |
| Sales engagement | `~~sales engagement` | Outreach MCP | Salesloft, Apollo |
