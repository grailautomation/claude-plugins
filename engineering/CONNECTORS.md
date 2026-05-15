# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~source control` might mean GitHub, GitLab, or any other VCS with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (source control, CI/CD, monitoring, etc.) rather than specific products. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. If an engineering workflow needs Google-backed email, calendar, or
files, use the `google-workspace` plugin and `gws` CLI after checking
`gws auth status`. Use MCP when no usable CLI exists, the CLI cannot express the
operation safely, or the workflow depends on MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Default integrations | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack MCP | Microsoft Teams |
| Source control | `~~source control` | GitHub via `gh` CLI | GitLab, Bitbucket |
| Project tracker | `~~project tracker` | Linear MCP, Asana MCP, Atlassian MCP (Jira/Confluence) | Shortcut, ClickUp |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files | Confluence, Guru, Coda |
| Monitoring | `~~monitoring` | Datadog MCP | New Relic, Grafana, Splunk |
| Incident management | `~~incident management` | PagerDuty MCP | Opsgenie, Incident.io, FireHydrant |
| CI/CD | `~~CI/CD` | — | CircleCI, GitHub Actions, Jenkins, BuildKite |
