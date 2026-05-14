# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~data warehouse` might mean Snowflake, BigQuery, or any other warehouse with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (data warehouse, notebook, product analytics, etc.) rather than specific products. The `.mcp.json` pre-configures fallback MCP servers, but any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

## CLI-first integration policy

Prefer a maintained CLI over MCP whenever the CLI can safely perform the
workflow. Use MCP when no usable CLI exists, the CLI cannot express the
operation safely, or the workflow depends on MCP-only capabilities.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Data warehouse | `~~data warehouse` | BigQuery | Snowflake, Databricks, Redshift, PostgreSQL, MySQL |
| Notebook | `~~notebook` | Hex | Jupyter, Deepnote, Observable |
| Product analytics | `~~product analytics` | Amplitude | Mixpanel, Heap |
| Project tracker | `~~project tracker` | Atlassian (Jira/Confluence) | Linear, Asana |

Snowflake and Databricks endpoints vary by account/workspace. Configure them in user, project, or local MCP settings with environment-variable-backed URLs instead of publishing empty marketplace defaults.
