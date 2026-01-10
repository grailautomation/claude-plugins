---
name: Cloudflare Domains
description: This skill should be used when the user asks to "list my domains", "manage DNS", "deploy to Cloudflare Pages", "create a landing page", "connect domain to Pages", "check my zones", "add DNS record", "set up a parked domain", or is working with Cloudflare Workers, Pages, KV, R2, D1, or DNS. Also use proactively when the user is working on static sites, landing pages, or domain management tasks.
version: 0.1.0
---

# Cloudflare Domains Management

Provide guidance for managing domains, DNS records, and Cloudflare Pages deployments using the Cloudflare MCP tools.

## Overview

This skill enables proactive assistance with Cloudflare services:
- **Zones**: List and manage domains/zones in the account
- **DNS**: Create, update, and delete DNS records
- **Pages**: Deploy static sites and connect custom domains
- **Storage**: Work with KV, R2, D1, Queues, and Vectorize

## When to Proactively Suggest Cloudflare Actions

Suggest Cloudflare operations when:

1. **User mentions domains or DNS**: Offer to list zones, check DNS records, or suggest configurations
2. **User is building a static site or landing page**: Suggest deploying to Cloudflare Pages
3. **User discusses "for sale" or parked domains**: Offer to deploy landing pages and configure DNS
4. **User asks about hosting options**: Recommend Cloudflare Pages for static content
5. **User is working with Workers code**: Offer deployment assistance

## Available MCP Tools

The Cloudflare MCP server provides tools for:

### Zone Management
- List all zones in the account
- Get zone details and settings
- Check zone status

### DNS Operations
- List DNS records for a zone
- Create new DNS records (A, AAAA, CNAME, TXT, MX, etc.)
- Update existing records
- Delete records

### Cloudflare Pages
- List Pages projects
- Create new Pages projects
- Deploy static sites
- Connect custom domains to projects
- View deployment status

### Storage Services
- **KV**: Key-value storage operations
- **R2**: Object storage (upload, download, list)
- **D1**: SQL database queries
- **Queues**: Message queue operations
- **Vectorize**: Vector database operations

## Common Workflows

### Listing Domains

To see all domains in the account:
1. Use the zones list tool
2. Display zone names, status, and IDs
3. Offer to show DNS records for any zone

### Setting Up a "For Sale" Landing Page

For parked domains needing landing pages:

1. **Create a Pages project** with a simple HTML landing page
2. **Deploy the static content** to the project
3. **Connect the custom domain** to the Pages project
4. **Configure DNS** to point to Pages (CNAME record)

Example DNS configuration for Pages:
```
Type: CNAME
Name: @ (or subdomain)
Target: <project-name>.pages.dev
Proxied: Yes
```

### DNS Record Management

Common DNS record patterns:

**Root domain to Pages:**
```
Type: CNAME
Name: @
Target: project.pages.dev
Proxied: Yes
```

**WWW subdomain:**
```
Type: CNAME
Name: www
Target: project.pages.dev
Proxied: Yes
```

**Email (MX records):**
```
Type: MX
Name: @
Target: mail.provider.com
Priority: 10
```

**Domain verification (TXT):**
```
Type: TXT
Name: @
Content: "verification-string"
```

### Deploying Static Sites

To deploy a static site to Cloudflare Pages:

1. **Prepare the static files** (HTML, CSS, JS, images)
2. **Create a Pages project** with appropriate name
3. **Upload/deploy the files** to the project
4. **Verify deployment** succeeded
5. **Add custom domain** if needed

## Environment Variables

The MCP server requires these environment variables:

- `CLOUDFLARE_API_TOKEN`: API token with appropriate permissions
- `CLOUDFLARE_ACCOUNT_ID`: The Cloudflare account ID

These should be set in the user's shell environment or Claude Code configuration.

## Proactive Assistance Patterns

### When User Mentions a Domain Name

When user mentions a specific domain:
1. Offer to check if it exists in their Cloudflare zones
2. If found, offer to show current DNS configuration
3. Suggest relevant actions (add records, deploy site, etc.)

### When User Creates HTML/Static Content

When user creates a landing page or static site:
1. Ask if they want to deploy to Cloudflare Pages
2. Suggest creating a Pages project
3. Offer to deploy the content
4. Help connect a custom domain if needed

### When User Discusses Domain Strategy

When user discusses domain management:
1. Offer to list all zones in account
2. Suggest organizational approaches
3. Help with bulk DNS operations if needed

## Best Practices

### DNS Management
- Prefer proxied mode for web traffic (orange cloud) unless DNS-only is specifically needed
- Keep TTL at "Auto" unless specific caching needs exist
- Document changes as they're made

### Pages Deployments
- Use descriptive project names
- Verify custom domain DNS before connecting
- Check deployment logs for errors

### Security
- Never expose API tokens in code or output
- Use minimal required permissions for API tokens
- Prefer environment variables for credentials

## Error Handling

Common issues and solutions:

**Zone not found**: Verify the domain is added to Cloudflare account

**DNS record conflict**: Check for existing records with same name/type

**Pages deployment failed**: Check file paths and content validity

**Custom domain error**: Ensure DNS is correctly configured and propagated

## Additional Resources

For detailed Cloudflare documentation:
- [Cloudflare Pages](https://developers.cloudflare.com/pages/) - Deployment and custom domains
- [DNS Records](https://developers.cloudflare.com/dns/manage-dns-records/) - Record types and management
- [Cloudflare API](https://developers.cloudflare.com/api/) - Full API reference
