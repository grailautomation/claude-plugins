# Cloudflare Plugin

Manage Cloudflare zones, DNS, Registrar, Workers, Pages, KV, R2, and D1 from Claude Code or Codex using Cloudflare CLIs first.

## Residency

This plugin is intended to stay in the public marketplace. Reusable workflow
guidance lives in this repository; account-specific credentials, account IDs,
zone IDs, domain lists, and deployment defaults must stay in environment
variables, Cloudflare CLI config, Claude/Codex config, or gitignored local
notes.

## Integration Policy

This plugin is CLI-first. Prefer these surfaces in order:

1. `cf` technical preview for zones, DNS, Registrar, Accounts, and generated
   API-backed commands.
2. `wrangler` for Workers and Pages app deployment plus KV, R2, D1, Queues, and
   local development workflows.
3. `flarectl` only as a legacy fallback for zones, DNS, firewall access rules,
   page rules, and cache purge.
4. `cli4` only as a generic Cloudflare API v4 fallback when `cf`, `wrangler`,
   and `flarectl` do not expose the needed operation.
5. Legacy MCP only when explicitly enabled by a local user or project.

Do not use the legacy MCP server as the default integration path. For Claude,
that means no root `.mcp.json` and no inline `mcpServers` in
`.claude-plugin/plugin.json`. For Codex, that means no `mcpServers` field in
`.codex-plugin/plugin.json`. The previous MCP config is preserved as
`.mcp.legacy.json` for explicit opt-in testing or compatibility work.

## Prerequisites

- Node.js 20+ for `cf` and `wrangler`
- Cloudflare account with the needed zones/resources
- Cloudflare API token with least-privilege scopes for the operation
- Optional: `flarectl` for legacy DNS/firewall workflows
- Optional: `cli4` for generic API fallback workflows

Use project-local or one-off execution rather than adding duplicate global CLI
installs:

```bash
pnpm dlx cf --help
pnpm dlx wrangler --help
```

If a persistent global install is intentional, first check existing install
lanes:

```bash
type -a cf wrangler flarectl cli4
which -a cf wrangler flarectl cli4
```

## Authentication

Prefer environment variables:

```bash
export CLOUDFLARE_API_TOKEN="your-api-token"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
export CLOUDFLARE_ZONE_ID="your-zone-id-or-domain"
```

`cf` also supports OAuth login and context defaults:

```bash
pnpm dlx cf auth login
pnpm dlx cf auth whoami
pnpm dlx cf context set account-id <account-id> --project
pnpm dlx cf context set zone example.com --project
```

Keep write tokens scoped to the smallest useful resource set. For read-heavy
inspection, use read-only tokens where possible.

## Common CLI Workflows

### Zones and DNS

Use `cf` first:

```bash
pnpm dlx cf zones list --fields id,name,status --ndjson
pnpm dlx cf dns records list --zone example.com --fields id,type,name,content,proxied --ndjson
pnpm dlx cf dns records create --zone example.com --dryRun --body '{"type":"CNAME","name":"www","content":"project.pages.dev","proxied":true}'
pnpm dlx cf dns records create --zone example.com --body '{"type":"CNAME","name":"www","content":"project.pages.dev","proxied":true}'
```

Use `flarectl` only when it is already available and better fits an older
DNS/firewall workflow:

```bash
flarectl --json zone list
flarectl --json dns list --zone example.com
flarectl --json dns create --zone example.com --name www --type CNAME --content project.pages.dev --proxy
```

Use `cli4` only for API paths not yet exposed by `cf` or `wrangler`:

```bash
cli4 /zones/:example.com/dns_records
cli4 --post name=www type=CNAME content=project.pages.dev proxied=true /zones/:example.com/dns_records
```

### Workers, Pages, and Storage

Use `wrangler` for project-oriented Workers and Pages workflows:

```bash
pnpm dlx wrangler deploy
pnpm dlx wrangler pages deploy ./dist --project-name my-project
pnpm dlx wrangler kv namespace list
pnpm dlx wrangler r2 bucket list
pnpm dlx wrangler d1 list
pnpm dlx wrangler d1 execute <database> --command 'select 1'
```

Use `cf` for generated API-backed Workers commands when Wrangler does not expose
the account-level operation:

```bash
pnpm dlx cf agent-context workers
pnpm dlx cf workers routes list --zone example.com --fields id,pattern,script --ndjson
```

### Parked Domain or Landing Page

1. Build static files locally.
2. Deploy with `pnpm dlx wrangler pages deploy`.
3. Inspect or add DNS with `pnpm dlx cf dns records ...`.
4. Use `--dryRun` before DNS creates, updates, or deletes.
5. Verify the record and custom domain after propagation.

## Safety Rules

- Always run `--dryRun` before `cf` create, update, delete, batch, import, or scan-review commands.
- Confirm before deleting zones, Workers, Pages projects, KV namespaces, R2 buckets, D1 databases, DNS records, or routes.
- Use `--fields` and `--ndjson` to keep agent output small and machine-readable.
- Prefer read-only API tokens for inspection.
- Never print full API tokens, account secrets, or private zone inventories into committed files.

## Legacy MCP

The legacy MCP server remains in `mcp-server/` and can be used explicitly for
compatibility testing:

```bash
cp .mcp.legacy.json .mcp.json
cd mcp-server
pnpm install
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node index.js
```

Do not commit a restored `.mcp.json` unless the plugin is deliberately moved
back to an MCP-first design.

## Development

This is a content-first plugin. Use `pnpm` for the legacy MCP server only; do
not add a second lockfile or a new global JavaScript CLI lane.

## References

- [Cloudflare `cf` CLI technical preview](https://blog.cloudflare.com/cf-cli-local-explorer/)
- [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Cloudflare DNS records API](https://developers.cloudflare.com/api/resources/dns/subresources/records/)
- [flarectl source](https://github.com/cloudflare/cloudflare-go/tree/v0/cmd/flarectl)
- [cli4 source](https://github.com/cloudflare/python-cloudflare-cli4)
