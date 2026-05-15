# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~e-signature` might mean DocuSign, Adobe Sign, or any other e-signature system with a CLI or MCP source.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (contract storage, CRM, e-signature, etc.) rather than a specific organization's stack. The plugin may ship remaining fallback MCP servers, while maintained CLI-backed defaults live outside `.mcp.json`; any maintained CLI or MCP source in that category works when it follows the CLI-first policy below.

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
| Cloud storage | `~~cloud storage` | Google Drive via `gws` CLI | Microsoft 365, Box, Dropbox, Egnyte |
| CRM | `~~CRM` | HubSpot MCP | Salesforce, Pipedrive |
| Email | `~~email` | Gmail via `gws` CLI | Microsoft 365 |
| E-signature | `~~e-signature` | DocuSign MCP | Adobe Sign, PandaDoc |
| Knowledge base | `~~knowledge base` | Notion MCP with `ntn` CLI pilot for pages/data sources/files | Confluence, Guru, Coda |

Contract playbooks, fallback positions, approved templates, jurisdiction preferences, and escalation rules are organization-specific. Keep those in gitignored local notes, user/project memory, or a private plugin rather than publishing them in this marketplace repo.
