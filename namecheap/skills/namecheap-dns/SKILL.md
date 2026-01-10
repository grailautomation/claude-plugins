---
name: Namecheap DNS Management
description: This skill should be used when the user asks to "list my domains", "check domain DNS", "update DNS records", "point domain to Cloudflare", "change nameservers", "transfer nameservers", or mentions Namecheap domain management. Provides guidance for managing domains and DNS through the Namecheap API.
version: 0.1.0
---

# Namecheap DNS Management

Guidance for managing domains and DNS records through the Namecheap API using the namecheap MCP server tools.

## Available Tools

The namecheap MCP server provides these tools:

| Tool | Purpose |
|------|---------|
| `list-domains` | List all domains in the Namecheap account |
| `get-domain-info` | Get domain details (status, expiry, nameservers) |
| `get-dns-hosts` | List DNS host records for a domain |
| `set-dns-host` | Add or update DNS records (replaces all records) |
| `delete-dns-host` | Remove a specific DNS record |
| `get-nameservers` | Get current nameservers for a domain |
| `set-nameservers` | Change to custom nameservers (e.g., Cloudflare) |
| `set-default-nameservers` | Reset to Namecheap default nameservers |

## Common Workflows

### Listing and Exploring Domains

To see all domains in the account:
```
Use list-domains to get all domains with expiry dates and status
```

To get detailed information about a specific domain:
```
Use get-domain-info with the domain name to see status, expiry, lock status, and current nameservers
```

### Viewing DNS Records

To see current DNS configuration:
```
Use get-dns-hosts with the domain name to list all host records (A, CNAME, MX, TXT, etc.)
```

### Updating DNS Records

**Critical:** The `set-dns-host` tool replaces ALL existing records. Always:
1. First retrieve current records with `get-dns-hosts`
2. Include all existing records to keep in the new set
3. Add or modify the desired record in the array

Example workflow to add a new record:
1. Call `get-dns-hosts` for the domain
2. Note all existing records
3. Call `set-dns-host` with array containing:
   - All existing records to preserve
   - The new record to add

Record types supported: A, AAAA, CNAME, MX, TXT, URL, URL301, FRAME

### Transferring DNS to Cloudflare

To point a domain to Cloudflare for DNS management:

1. Get current state: `get-domain-info` to see current nameservers
2. Set Cloudflare nameservers: `set-nameservers` with:
   - `nameservers: ["ns1.cloudflare.com", "ns2.cloudflare.com"]`
3. Wait for propagation (can take up to 48 hours)
4. Configure DNS records in Cloudflare dashboard

Note: After changing nameservers to Cloudflare, manage DNS records in Cloudflare, not Namecheap.

### Pointing to Cloudflare Pages

For domains using Cloudflare Pages hosting:

1. Transfer nameservers to Cloudflare (see above)
2. In Cloudflare:
   - Add CNAME record: `@` → `your-project.pages.dev`
   - Or add A records pointing to Cloudflare's IPs
3. Add custom domain in Cloudflare Pages project settings

### Resetting to Namecheap DNS

To return a domain to Namecheap's nameservers:
```
Use set-default-nameservers with the domain name
```

After reset, manage DNS records using Namecheap tools again.

## Record Format Reference

When using `set-dns-host`, each record needs:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Host name: `@` for root, `www`, `mail`, subdomain, etc. |
| `type` | Yes | Record type: A, AAAA, CNAME, MX, TXT, URL, URL301, FRAME |
| `address` | Yes | Record value: IP address, hostname, or text content |
| `ttl` | No | Time-to-live in seconds (default: 1800) |
| `mxPref` | For MX | Priority value for MX records |

### Common Record Examples

**A record (root domain):**
```json
{ "name": "@", "type": "A", "address": "192.0.2.1" }
```

**CNAME record (www subdomain):**
```json
{ "name": "www", "type": "CNAME", "address": "example.com" }
```

**MX record (email):**
```json
{ "name": "@", "type": "MX", "address": "mail.example.com", "mxPref": 10 }
```

**TXT record (verification):**
```json
{ "name": "@", "type": "TXT", "address": "v=spf1 include:_spf.google.com ~all" }
```

## Troubleshooting

### API Access Denied
- Verify IP address is whitelisted in Namecheap account
- Check API is enabled in Account → Profile → Tools → API Access

### Domain Not Found
- Confirm domain is registered under the authenticated account
- Check spelling and TLD

### DNS Changes Not Reflected
- DNS propagation can take up to 48 hours
- Use `dig` or online DNS checkers to verify propagation
- Clear local DNS cache if testing locally

### Cannot Modify DNS
- If using custom nameservers (Cloudflare, etc.), manage DNS there instead
- Reset to default nameservers first if returning to Namecheap DNS

## Environment Variables

The MCP server requires these environment variables:

| Variable | Description |
|----------|-------------|
| `NAMECHEAP_API_USER` | API username (usually same as account username) |
| `NAMECHEAP_API_KEY` | API key from Namecheap account |
| `NAMECHEAP_USERNAME` | Account username (optional, defaults to API_USER) |

Set these before starting Claude Code:
```bash
export NAMECHEAP_API_USER="username"
export NAMECHEAP_API_KEY="api-key"
export NAMECHEAP_USERNAME="username"
```
