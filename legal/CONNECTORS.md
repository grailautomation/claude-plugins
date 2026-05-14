# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~e-signature` might mean DocuSign, Adobe Sign, or any other e-signature system with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (contract storage, CRM, e-signature, etc.) rather than a specific organization's stack. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Calendar | `~~calendar` | Google Calendar | Microsoft 365 |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Cloud storage | `~~cloud storage` | Google Drive | Microsoft 365, Box, Dropbox, Egnyte |
| CRM | `~~CRM` | HubSpot | Salesforce, Pipedrive |
| Email | `~~email` | Gmail | Microsoft 365 |
| E-signature | `~~e-signature` | DocuSign | Adobe Sign, PandaDoc |
| Knowledge base | `~~knowledge base` | Notion | Confluence, Guru, Coda |

Contract playbooks, fallback positions, approved templates, jurisdiction preferences, and escalation rules are organization-specific. Keep those in gitignored local notes, user/project memory, or a private plugin rather than publishing them in this marketplace repo.
