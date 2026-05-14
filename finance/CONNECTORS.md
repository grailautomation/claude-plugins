# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~data warehouse` might mean Snowflake, BigQuery, or any other warehouse with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (data warehouse, chat, project tracker, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Data warehouse | `~~data warehouse` | BigQuery | Snowflake, Databricks, Redshift, PostgreSQL |
| Email | `~~email` | Microsoft 365 | — |
| Office suite | `~~office suite` | Microsoft 365 | — |
| Chat | `~~chat` | Slack | Microsoft Teams |
| ERP / Accounting | `~~erp` | — (no supported MCP servers yet) | NetSuite, SAP, QuickBooks, Xero |
| Analytics / BI | `~~analytics` | — (no supported MCP servers yet) | Tableau, Looker, Power BI |

Snowflake and Databricks endpoints vary by account/workspace. Configure them in user, project, or local MCP settings with environment-variable-backed URLs instead of publishing empty marketplace defaults.
