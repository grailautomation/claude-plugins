# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Linear, Asana, Jira, or any other tracker with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (project tracker, design, product analytics, etc.) rather than specific products. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

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
| Competitive intelligence | `~~competitive intelligence` | Similarweb MCP | Crayon, Klue |
| Design | `~~design` | Figma MCP | Sketch, Adobe XD |
| Email | `~~email` | Gmail via `gws` CLI | Microsoft 365 |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files | Confluence, Guru, Coda |
| Meeting transcription | `~~meeting transcription` | Fireflies MCP | Gong, Dovetail, Otter.ai |
| Product analytics | `~~product analytics` | Amplitude MCP, Pendo MCP | Mixpanel, Heap, FullStory |
| Project tracker | `~~project tracker` | Linear MCP, Asana MCP, monday.com MCP, ClickUp MCP, Atlassian MCP (Jira/Confluence) | Shortcut, Basecamp |
| User feedback | `~~user feedback` | Intercom MCP | Productboard, Canny, UserVoice |
