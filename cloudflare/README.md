# Cloudflare Plugin for Claude Code

Manage your Cloudflare domains, DNS records, Workers, and storage services directly from Claude Code.

## Features

- **Zone Management**: List and manage domains in your Cloudflare account
- **DNS Records**: Create, update, and delete DNS records (A, AAAA, CNAME, TXT, MX, etc.)
- **Workers**: Deploy, view, and manage Cloudflare Workers scripts
- **Worker Routes**: Map URL patterns to Worker scripts
- **KV Storage**: Manage KV namespaces and key-value pairs
- **R2 Storage**: Create and manage R2 buckets
- **D1 Databases**: Create databases and execute SQL queries
- **Cloudflare Pages**: List and view Pages projects
- **Proactive Assistance**: Claude suggests Cloudflare actions when relevant

## Prerequisites

1. **Node.js**: Required to run the MCP server
2. **Cloudflare Account**: With domains/zones configured
3. **API Token**: With appropriate permissions

## Setup

### 1. Create a Cloudflare API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use "Custom token" with these permissions:
   - **Account**: Workers Pipelines (Edit), Queues (Edit), D1 (Edit), Cloudflare Pages (Read), Workers R2 Storage (Edit), Workers KV Storage (Edit), Workers Scripts (Edit), Account Settings (Read)
   - **Zone (All zones)**: DNS Settings (Read), Zone (Read), Workers Routes (Edit), DNS (Edit)
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

### 4. Install Dependencies

```bash
cd /path/to/cloudflare/mcp-server
pnpm install
```

### 5. Enable the Plugin

```bash
# Test the plugin
claude --plugin-dir /path/to/cloudflare

# Or add to your Claude Code settings
```

## Available Tools

### Zones (Domains)
| Tool | Description |
|------|-------------|
| `zones-list` | List all zones in your account |
| `zones-get` | Get details for a specific zone |

### DNS Records
| Tool | Description |
|------|-------------|
| `dns-records-list` | List DNS records for a zone |
| `dns-records-create` | Create a new DNS record |
| `dns-records-update` | Update an existing record |
| `dns-records-delete` | Delete a DNS record |

### Workers
| Tool | Description |
|------|-------------|
| `workers-list` | List all Worker scripts |
| `workers-get` | Get a Worker script content |
| `workers-put` | Deploy/update a Worker script |
| `workers-delete` | Delete a Worker script |
| `worker-routes-list` | List routes for a zone |
| `worker-route-create` | Create a Worker route |
| `worker-route-delete` | Delete a Worker route |

### KV Storage
| Tool | Description |
|------|-------------|
| `kv-namespaces-list` | List KV namespaces |
| `kv-namespace-create` | Create a KV namespace |
| `kv-keys-list` | List keys in a namespace |
| `kv-get` | Get a value |
| `kv-put` | Store a value |
| `kv-delete` | Delete a value |

### R2 Storage
| Tool | Description |
|------|-------------|
| `r2-buckets-list` | List R2 buckets |
| `r2-bucket-create` | Create an R2 bucket |
| `r2-bucket-delete` | Delete an R2 bucket |

### D1 Databases
| Tool | Description |
|------|-------------|
| `d1-databases-list` | List D1 databases |
| `d1-database-create` | Create a D1 database |
| `d1-database-delete` | Delete a D1 database |
| `d1-query` | Execute SQL query |

### Pages
| Tool | Description |
|------|-------------|
| `pages-projects-list` | List Pages projects |
| `pages-project-get` | Get project details |

## Usage Examples

Once enabled, Claude will proactively suggest Cloudflare actions. You can also ask directly:

- "List my Cloudflare domains"
- "Show DNS records for example.com"
- "Add a CNAME record pointing www to my site"
- "Deploy this Worker script"
- "Create a KV namespace for my app"
- "Run a query against my D1 database"

## Components

- **MCP Server**: Custom implementation using `@modelcontextprotocol/sdk` v1.x
- **Skill**: `cloudflare-domains` for proactive guidance and workflows

## Troubleshooting

### MCP Server Not Starting

Verify environment variables are set:
```bash
echo $CLOUDFLARE_API_TOKEN
echo $CLOUDFLARE_ACCOUNT_ID
```

### Testing the MCP Server

```bash
cd mcp-server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node index.js
```

### API Errors

- Check that your API token has the required permissions
- Verify the account ID is correct
- Ensure the token hasn't expired

### Zone Not Found

- Confirm the domain is added to your Cloudflare account
- Check that DNS is properly configured at your registrar
