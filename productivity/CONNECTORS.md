# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. Use `gws gmail`, `gws calendar`, `gws drive`, or `gws docs` for Google
Workspace after checking `gws auth status`. Use MCP when no usable CLI exists,
the CLI cannot express the operation safely, or the workflow depends on
MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Default integrations | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack MCP | Microsoft Teams, Discord |
| Email | `~~email` | Microsoft 365 MCP | — |
| Calendar | `~~calendar` | Microsoft 365 MCP | — |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files | Confluence, Guru, Coda |
| Project tracker | `~~project tracker` | Asana MCP, Linear MCP, Atlassian MCP (Jira/Confluence), monday.com MCP, ClickUp MCP | Shortcut, Basecamp, Wrike |
| Office suite | `~~office suite` | Microsoft 365 MCP | — |
