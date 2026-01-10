# Cloudflare Plugin for Claude Code

Manage your Cloudflare domains, DNS records, and Pages deployments directly from Claude Code.

## Features

- **Zone Management**: List and manage domains in your Cloudflare account
- **DNS Records**: Create, update, and delete DNS records
- **Cloudflare Pages**: Deploy static sites and connect custom domains
- **Storage Services**: Access KV, R2, D1, Queues, and Vectorize
- **Proactive Assistance**: Claude suggests Cloudflare actions when relevant

## Prerequisites

1. **Node.js**: Required to run the MCP server via npx
2. **Cloudflare Account**: With domains/zones configured
3. **API Token**: With appropriate permissions

## Setup

### 1. Create a Cloudflare API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use "Custom token" with these permissions:
   - **Account**: Workers Pipelines (Edit), Queues (Edit), Vectorize (Edit), D1 (Edit), Cloudflare Pages (Edit), Workers R2 Storage (Edit), Workers KV Storage (Edit), Workers Scripts (Edit), Account Settings (Read)
   - **Zone (All zones)**: DNS Settings (Read), Zone (Edit), Workers Routes (Edit), DNS (Edit)
   - **User**: Memberships (Read), User Details (Read)
4. Copy the token

### 2. Get Your Account ID

1. Go to any zone in Cloudflare Dashboard
2. Find "Account ID" in the right sidebar (API section)
3. Copy the ID

### 3. Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export CLOUDFLARE_API_TOKEN="your-api-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id-here"
```

Then reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### 4. Enable the Plugin

```bash
# Test the plugin
claude --plugin-dir /Users/dave/Documents/DEV/claude-plugins/cloudflare

# Or add to your Claude Code settings
```

## Usage

Once enabled, Claude will proactively suggest Cloudflare actions. You can also ask directly:

- "List my Cloudflare domains"
- "Show DNS records for example.com"
- "Deploy this landing page to Cloudflare Pages"
- "Add a CNAME record pointing to my Pages project"
- "Create a 'for sale' landing page for mydomain.com"

## Components

- **MCP Server**: `@cloudflare/mcp-server-cloudflare` for API access
- **Skill**: `cloudflare-domains` for proactive guidance and workflows

## Troubleshooting

### MCP Server Not Starting

Verify environment variables are set:
```bash
echo $CLOUDFLARE_API_TOKEN
echo $CLOUDFLARE_ACCOUNT_ID
```

### API Errors

- Check that your API token has the required permissions
- Verify the account ID is correct
- Ensure the token hasn't expired

### Zone Not Found

- Confirm the domain is added to your Cloudflare account
- Check that DNS is properly configured at your registrar
