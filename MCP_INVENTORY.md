# MCP Inventory

This inventory reflects the tracked `.mcp.json` files in this repository. It is
not a Codex migration approval list. Preserve Claude MCP parity by default; if a
native Codex app/connector looks materially better for a specific dependency,
open a GitHub issue instead of silently substituting it.

## Current Servers

| Server | Kind | Current config | Used by | Env vars | Current disposition |
| --- | --- | --- | --- | --- | --- |
| `amplitude` | HTTP MCP | `https://mcp.amplitude.com/mcp` | `data`, `product-management` |  | Claude MCP parity review required |
| `apollo` | HTTP MCP | `https://api.apollo.io/mcp` | `sales` |  | Claude MCP parity review required |
| `asana` | HTTP MCP | `https://mcp.asana.com/v2/mcp` | `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity` |  | Claude MCP parity review required |
| `atlassian` | HTTP MCP | `https://mcp.atlassian.com/v1/mcp` | `data`, `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity`, `sales` |  | Claude MCP parity review required |
| `bigquery` | HTTP MCP | `https://bigquery.googleapis.com/mcp` | `data`, `finance` |  | Claude MCP parity review required |
| `clay` | HTTP MCP | `https://api.clay.com/v3/mcp` | `sales` |  | Claude MCP parity review required |
| `clickup` | HTTP MCP | `https://mcp.clickup.com/mcp` | `product-management`, `productivity` |  | Claude MCP parity review required |
| `close` | HTTP MCP | `https://mcp.close.com/mcp` | `sales` |  | Claude MCP parity review required |
| `cloudflare` | local npm MCP | `npx -y @grailautomation/cloudflare-mcp` | `cloudflare` | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` | Public Claude and Codex plugin; npm package exists at `0.1.0`; published `npx` tools/list smoke passed with 28 tools |
| `datadog` | HTTP MCP | `https://mcp.datadoghq.com/mcp` | `engineering` |  | Claude MCP parity review required |
| `docusign` | HTTP MCP | `https://mcp.docusign.com/mcp` | `legal` |  | Claude MCP parity review required |
| `figma` | HTTP MCP | `https://mcp.figma.com/mcp` | `design`, `product-management` |  | Claude MCP parity review required |
| `fireflies` | HTTP MCP | `https://api.fireflies.ai/mcp` | `product-management`, `sales` |  | Claude MCP parity review required |
| `github` | HTTP MCP | `https://api.github.com/mcp` | `engineering` |  | Claude MCP parity review required |
| `gmail` | HTTP MCP | `https://gmail.mcp.claude.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Claude MCP parity review required |
| `google-calendar` | HTTP MCP | `https://gcal.mcp.claude.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Claude MCP parity review required |
| `google-drive` | HTTP MCP | `https://google-drive-mcp.claude.com/mcp` | `legal` |  | Claude MCP parity review required |
| `guru` | HTTP MCP | `https://mcp.api.getguru.com/mcp` | `enterprise-search` |  | Claude MCP parity review required |
| `hex` | HTTP MCP | `https://app.hex.tech/mcp` | `data` |  | Claude MCP parity review required |
| `hubspot` | HTTP MCP | `https://mcp.hubspot.com/anthropic` | `legal`, `sales` |  | Claude MCP parity review required |
| `intercom` | HTTP MCP | `https://mcp.intercom.com/mcp` | `design`, `product-management` |  | Claude MCP parity review required |
| `linear` | HTTP MCP | `https://mcp.linear.app/mcp` | `design`, `engineering`, `product-management`, `productivity` |  | Claude MCP parity review required |
| `monday` | HTTP MCP | `https://mcp.monday.com/mcp` | `product-management`, `productivity` |  | Claude MCP parity review required |
| `ms365` | HTTP MCP | `https://microsoft365.mcp.claude.com/mcp` | `enterprise-search`, `finance`, `operations`, `productivity`, `sales` |  | Claude MCP parity review required |
| `namecheap` | local npm MCP | `npx -y @grailautomation/namecheap-mcp` | `namecheap` | `NAMECHEAP_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_USERNAME` | Public Claude and Codex plugin; npm package exists at `0.1.0`; published `npx` tools/list smoke passed with 8 tools |
| `notion` | HTTP MCP | `https://mcp.notion.com/mcp` | `design`, `engineering`, `enterprise-search`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Claude MCP parity review required |
| `outreach` | HTTP MCP | `https://mcp.outreach.io/mcp` | `sales` |  | Claude MCP parity review required |
| `pagerduty` | HTTP MCP | `https://mcp.pagerduty.com/mcp` | `engineering` |  | Claude MCP parity review required |
| `pendo` | HTTP MCP | `https://app.pendo.io/mcp/v0/shttp` | `product-management` |  | Claude MCP parity review required |
| `servicenow` | HTTP MCP | `https://mcp.servicenow.com/mcp` | `operations` |  | Claude MCP parity review required |
| `similarweb` | HTTP MCP | `https://mcp.similarweb.com/mcp` | `product-management`, `sales` |  | Claude MCP parity review required |
| `slack` | HTTP MCP | `https://mcp.slack.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Claude MCP parity review required |
| `zoominfo` | HTTP MCP | `https://mcp.zoominfo.com/mcp` | `sales` |  | Claude MCP parity review required |

## Review Rules

- Do not list connector-heavy plugins for Codex by adding manifests only.
- Keep the current Claude MCP architecture as the default source of truth.
- For HTTP MCP servers, verify Codex runtime support, auth setup, and side
  effects before listing the owning plugin.
- For local npm MCP servers, verify package name, package manager/lockfile,
  environment variables, and startup behavior before deciding whether the plugin
  is public or personal/local.
- For Google and Microsoft endpoints, call out any proposed native Codex
  connector substitution in a GitHub issue before changing the migration plan.
