# Namecheap Plugin for Claude Code

Interact with the Namecheap API for domain and DNS management directly from Claude Code.

## Features

- List all domains in your Namecheap account
- View and update DNS host records
- Transfer nameservers to external providers (e.g., Cloudflare)
- Get domain information (expiry, status, lock status)

## Prerequisites

1. **Namecheap API Access**: Enable API access in your Namecheap account at Account → Profile → Tools → API Access
2. **Whitelisted IP**: Add your IP address to the API whitelist in Namecheap

## Installation

1. Clone or copy this plugin to your plugins directory
2. Set the required environment variables (see below)
3. Enable the plugin in Claude Code

## Environment Variables

Set these environment variables before starting Claude Code:

```bash
export NAMECHEAP_API_USER="your-api-username"
export NAMECHEAP_API_KEY="your-api-key"
export NAMECHEAP_USERNAME="your-namecheap-username"
```

Typically `NAMECHEAP_API_USER` and `NAMECHEAP_USERNAME` are the same value.

## Available Tools

| Tool | Description |
|------|-------------|
| `list-domains` | Get all domains in your account |
| `get-domain-info` | Get details for a specific domain |
| `get-dns-hosts` | List DNS host records for a domain |
| `set-dns-host` | Add or update a DNS host record |
| `delete-dns-host` | Remove a DNS host record |
| `get-nameservers` | Get current nameservers for a domain |
| `set-nameservers` | Change nameservers (e.g., to Cloudflare) |
| `set-default-nameservers` | Reset to Namecheap default nameservers |

## Common Workflows

### Point domain to Cloudflare Pages

1. List your domains to find the one to configure
2. Set nameservers to Cloudflare's (ns1.cloudflare.com, ns2.cloudflare.com)
3. Configure DNS in Cloudflare to point to your Pages project

### Update DNS records

1. Get current DNS hosts for the domain
2. Set or update the desired host record
3. Verify the change with get-dns-hosts

## Troubleshooting

- **API Access Denied**: Ensure your IP is whitelisted in Namecheap
- **Invalid Credentials**: Verify environment variables are set correctly
- **Domain Not Found**: Check the domain is registered under your account
