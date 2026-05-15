---
name: cloudflare-domains
description: This skill should be used when the user asks to list Cloudflare domains or zones, manage DNS, deploy to Cloudflare Pages, connect a custom domain, add or update DNS records, set up a parked domain, or work with Cloudflare Workers, Pages, KV, R2, D1, Queues, Vectorize, Registrar, or DNS.
version: 0.1.0
---

# Cloudflare CLI Workflows

Use Cloudflare CLIs before MCP. The default order is:

1. `cf` technical preview for zones, DNS, Registrar, Accounts, and generated API-backed commands.
2. `wrangler` for Workers, Pages, KV, R2, D1, Queues, and local development.
3. `flarectl` as a legacy fallback for zones, DNS, firewall access rules, page rules, and cache purge.
4. `cli4` as a generic Cloudflare API v4 fallback.
5. Legacy MCP only when the user explicitly enables it locally.

## Authentication

Prefer environment variables:

```bash
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_ZONE_ID
```

`cf` also supports `cf auth login`, `cf auth whoami`, and project context in
`.cfrc`. Keep tokens least-privilege and use read-only tokens for inspection
whenever possible.

Before recommending a persistent global install, check existing install lanes:

```bash
type -a cf wrangler flarectl cli4
which -a cf wrangler flarectl cli4
```

Prefer one-off execution:

```bash
pnpm dlx cf --help
pnpm dlx wrangler --help
```

## Zones and DNS

Use `cf` for zone and DNS work:

```bash
pnpm dlx cf zones list --fields id,name,status --ndjson
pnpm dlx cf dns records list --zone example.com --fields id,type,name,content,proxied --ndjson
pnpm dlx cf dns records create --zone example.com --dryRun --body '{"type":"CNAME","name":"www","content":"project.pages.dev","proxied":true}'
pnpm dlx cf dns records update --zone example.com --dryRun --body '{"type":"TXT","name":"@","content":"verification-string"}'
pnpm dlx cf dns records delete --zone example.com --dryRun --body '{"id":"record-id"}'
```

Always dry-run creates, updates, deletes, imports, batches, and scan-review
operations before applying them. Confirm the exact zone, record ID, record
content, and proxied state before making changes.

Use `flarectl` only when it is already installed and a simple DNS/firewall/page
rule operation is clearer there:

```bash
flarectl --json zone list
flarectl --json dns list --zone example.com
flarectl --json dns create --zone example.com --name www --type CNAME --content project.pages.dev --proxy
```

Use `cli4` only for API paths not exposed by `cf` or `wrangler`:

```bash
cli4 /zones/:example.com/dns_records
cli4 --post name=www type=CNAME content=project.pages.dev proxied=true /zones/:example.com/dns_records
```

## Workers, Pages, and Storage

Use `wrangler` for project-oriented development and deployments:

```bash
pnpm dlx wrangler deploy
pnpm dlx wrangler pages deploy ./dist --project-name my-project
pnpm dlx wrangler kv namespace list
pnpm dlx wrangler r2 bucket list
pnpm dlx wrangler d1 list
pnpm dlx wrangler d1 execute <database> --command 'select 1'
```

Use `cf` for generated account-level commands or resource APIs that Wrangler
does not expose:

```bash
pnpm dlx cf agent-context workers
pnpm dlx cf workers routes list --zone example.com --fields id,pattern,script --ndjson
```

## Proactive Assistance

Suggest Cloudflare actions when the user:

- Mentions a domain, DNS record, zone, parked domain, or nameserver change.
- Builds static HTML, a landing page, or a docs site that could deploy to Pages.
- Works on Worker code, KV, R2, D1, Queues, or Vectorize.
- Needs to inspect Cloudflare account resources before changing deployment or DNS.

When the user mentions a specific domain, first inspect whether it exists as a
Cloudflare zone, then list the relevant DNS records before proposing changes.

When deploying static content:

1. Prepare the local static files.
2. Deploy with `pnpm dlx wrangler pages deploy`.
3. Inspect or add DNS with `pnpm dlx cf dns records ...`.
4. Dry-run DNS mutations before applying them.
5. Verify the custom domain and deployment after propagation.

## Safety

- Never expose API tokens in code, output, or committed files.
- Confirm before deleting zones, Workers, Pages projects, KV namespaces, R2 buckets, D1 databases, DNS records, or routes.
- Prefer `--fields` and `--ndjson` to keep responses small and structured.
- Prefer `--body` for complex `cf` payloads so the exact request can be reviewed.
- Treat the legacy MCP server as opt-in compatibility tooling, not the default path.

## References

- [Cloudflare `cf` CLI technical preview](https://blog.cloudflare.com/cf-cli-local-explorer/)
- [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Cloudflare DNS records API](https://developers.cloudflare.com/api/resources/dns/subresources/records/)
- [flarectl source](https://github.com/cloudflare/cloudflare-go/tree/v0/cmd/flarectl)
- [cli4 source](https://github.com/cloudflare/python-cloudflare-cli4)
