# MCP Inventory

This inventory reflects the tracked `.mcp.json` files in this repository. It is
not a Codex migration approval list. Preserve existing MCP behavior by default; if a
native Codex app/connector looks materially better for a specific dependency,
open a GitHub issue instead of silently substituting it.

Connector-heavy domain pack review is resolved in
[issue #25](https://github.com/grailautomation/claude-plugins/issues/25). See
[DOMAIN_PACKS_CODEX.md](DOMAIN_PACKS_CODEX.md) for pack-level Codex mappings,
omissions, and side-effect expectations.

## Current Servers

| Server | Kind | Current config | Used by | Env vars | Current disposition |
| --- | --- | --- | --- | --- | --- |
| `amplitude` | HTTP MCP | `https://mcp.amplitude.com/mcp` | `data`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `apollo` | HTTP MCP | `https://api.apollo.io/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `asana` | HTTP MCP | `https://mcp.asana.com/v2/mcp` | `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `atlassian` | HTTP MCP | `https://mcp.atlassian.com/v1/mcp` | `data`, `design`, `engineering`, `enterprise-search`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `bigquery` | HTTP MCP | `https://bigquery.googleapis.com/mcp` | `data`, `finance` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `clay` | HTTP MCP | `https://api.clay.com/v3/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `clickup` | HTTP MCP | `https://mcp.clickup.com/mcp` | `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `close` | HTTP MCP | `https://mcp.close.com/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `cloudflare` | local npm MCP | `npx -y @grailautomation/cloudflare-mcp` | `cloudflare` | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` | Public Claude and Codex plugin; npm package exists at `0.1.0`; published `npx` tools/list smoke passed with 28 tools |
| `context7` | local npm MCP | `npx -y @upstash/context7-mcp` | `context7` |  | Public Claude and Codex plugin; npm package latest observed at `2.2.5`; published `npx` tools/list smoke passed with 2 tools |
| `datadog` | HTTP MCP | `https://mcp.datadoghq.com/mcp` | `engineering` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `docusign` | HTTP MCP | `https://mcp.docusign.com/mcp` | `legal` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `figma` | HTTP MCP | `https://mcp.figma.com/mcp` | `design`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `fireflies` | HTTP MCP | `https://api.fireflies.ai/mcp` | `product-management`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `github` | HTTP MCP | `https://api.github.com/mcp` | `engineering` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `gmail` | HTTP MCP | `https://gmail.mcp.claude.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `google-calendar` | HTTP MCP | `https://gcal.mcp.claude.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `google-drive` | HTTP MCP | `https://google-drive-mcp.claude.com/mcp` | `legal` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `guru` | HTTP MCP | `https://mcp.api.getguru.com/mcp` | `enterprise-search` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `hex` | HTTP MCP | `https://app.hex.tech/mcp` | `data` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `hubspot` | HTTP MCP | `https://mcp.hubspot.com/anthropic` | `legal`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `intercom` | HTTP MCP | `https://mcp.intercom.com/mcp` | `design`, `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `linear` | HTTP MCP | `https://mcp.linear.app/mcp` | `design`, `engineering`, `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `monday` | HTTP MCP | `https://mcp.monday.com/mcp` | `product-management`, `productivity` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `ms365` | HTTP MCP | `https://microsoft365.mcp.claude.com/mcp` | `enterprise-search`, `finance`, `operations`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `namecheap` | local npm MCP | `npx -y @grailautomation/namecheap-mcp` | `namecheap` | `NAMECHEAP_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_USERNAME` | Public Claude and Codex plugin; npm package exists at `0.1.0`; published `npx` tools/list smoke passed with 8 tools |
| `notion` | HTTP MCP | `https://mcp.notion.com/mcp` | `design`, `engineering`, `enterprise-search`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `outreach` | HTTP MCP | `https://mcp.outreach.io/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `pagerduty` | HTTP MCP | `https://mcp.pagerduty.com/mcp` | `engineering` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `pendo` | HTTP MCP | `https://app.pendo.io/mcp/v0/shttp` | `product-management` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `servicenow` | HTTP MCP | `https://mcp.servicenow.com/mcp` | `operations` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `similarweb` | HTTP MCP | `https://mcp.similarweb.com/mcp` | `product-management`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `slack` | HTTP MCP | `https://mcp.slack.com/mcp` | `design`, `engineering`, `enterprise-search`, `finance`, `legal`, `operations`, `product-management`, `productivity`, `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |
| `zoominfo` | HTTP MCP | `https://mcp.zoominfo.com/mcp` | `sales` |  | Reviewed for Codex mapping; see Hosted HTTP MCP Dispositions below |

## Hosted HTTP MCP Dispositions

The connector-heavy domain packs preserve their Claude `.mcp.json` files. Codex
uses pack-local `.mcp.codex.json` files that include only endpoints that
responded to a non-auth MCP `initialize` probe with either initialize success or
an auth/RBAC challenge. Endpoints that returned `404` or failed DNS resolution
are intentionally omitted from Codex configs until a specific issue chooses a
fix or replacement.

| Server | Codex disposition | Auth/setup expectation |
| --- | --- | --- |
| `amplitude` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `apollo` | Omitted from Codex filtered configs | Probe returned `404`; preserve Claude config only until a specific fix/replacement issue exists. |
| `asana` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `atlassian` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `bigquery` | Included in filtered Codex MCP configs | MCP initialize returned `200`; Google auth/project permissions required for tools. |
| `clay` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user login/OAuth setup required. |
| `clickup` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `close` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `datadog` | Omitted from Codex filtered configs | Probe returned `404`; preserve Claude config only until a specific fix/replacement issue exists. |
| `docusign` | Included in filtered Codex MCP configs | Endpoint reached RBAC access denial; user auth and account/RBAC setup required. |
| `figma` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `fireflies` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `github` | Omitted from Codex filtered configs | Probe returned `404`; no native-connector substitution in this repo without a specific issue. |
| `gmail` | Omitted from Codex filtered configs | Claude-hosted endpoint returned `404`; use the separate `google-workspace` CLI plugin for Codex Google Workspace work. |
| `google-calendar` | Omitted from Codex filtered configs | Claude-hosted endpoint returned `404`; use the separate `google-workspace` CLI plugin for Codex Google Workspace work. |
| `google-drive` | Omitted from Codex filtered configs | Host did not resolve; preserve Claude config only until a specific fix/replacement issue exists. |
| `guru` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `hex` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user auth setup required. |
| `hubspot` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `intercom` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `linear` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `monday` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `ms365` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; Microsoft auth setup required. |
| `notion` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user OAuth/token setup required. |
| `outreach` | Omitted from Codex filtered configs | Host did not resolve; preserve Claude config only until a specific fix/replacement issue exists. |
| `pagerduty` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |
| `pendo` | Omitted from Codex filtered configs | Host did not resolve; preserve Claude config only until a specific fix/replacement issue exists. |
| `servicenow` | Omitted from Codex filtered configs | Host did not resolve; preserve Claude config only until a specific fix/replacement issue exists. |
| `similarweb` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; API key or bearer-token setup required. |
| `slack` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token/OAuth setup required. |
| `zoominfo` | Included in filtered Codex MCP configs | Hosted HTTP MCP reached auth challenge; user token setup required. |

Side-effect expectations for the domain packs are documented in
[DOMAIN_PACKS_CODEX.md](DOMAIN_PACKS_CODEX.md). Authenticated live workflow
smoke tests remain install/runtime validation because they require user-specific
SaaS OAuth, scopes, workspaces, and target records.

## Review Rules

- Do not list connector-heavy plugins for Codex by adding manifests only.
- Keep the current MCP configuration as the default source of truth.
- For HTTP MCP servers, verify Codex runtime support, auth setup, and side
  effects before listing the owning plugin.
- For local npm MCP servers, verify package name, package manager/lockfile,
  environment variables, and startup behavior before deciding whether the plugin
  is public or personal/local.
- For Google and Microsoft endpoints, call out any proposed native Codex
  connector substitution in a GitHub issue before changing the migration plan.
