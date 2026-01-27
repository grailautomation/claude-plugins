# Salesforce CLI Authentication

## Check Connected Orgs

```bash
# List all orgs
sf org list

# List with connection status
sf org list --skip-connection-status

# Include expired scratch orgs
sf org list --all
```

Output shows:
- Alias
- Username
- Org ID
- Status (Connected/Expired)
- Type (Production/Sandbox/Scratch)

## Display Org Details

```bash
# Default org
sf org display

# Specific org
sf org display --target-org production

# Include sensitive info (auth URL)
sf org display --target-org production --verbose
```

## Login to New Org

### Web-Based Login (Recommended)

```bash
# Production/Developer org
sf org login web

# Sandbox
sf org login web --instance-url https://test.salesforce.com

# With My Domain
sf org login web --instance-url https://mycompany.my.salesforce.com

# Sandbox with My Domain
sf org login web --instance-url https://mycompany--sandbox.sandbox.my.salesforce.com
```

### Set as Default

```bash
# Set as default org for commands
sf org login web --set-default

# Set as default Dev Hub
sf org login web --set-default-dev-hub
```

### Set Alias

```bash
sf org login web --alias production
sf org login web --alias staging --instance-url https://test.salesforce.com
```

### Specify Browser

```bash
sf org login web --browser chrome
sf org login web --browser firefox
sf org login web --browser edge
```

## JWT-Based Login (Headless)

For CI/CD or environments without a browser:

```bash
sf org login jwt \
  --client-id <connected_app_consumer_key> \
  --jwt-key-file <path/to/server.key> \
  --username <username> \
  --instance-url https://login.salesforce.com \
  --alias production
```

## Manage Aliases

```bash
# List aliases
sf alias list

# Set alias for existing auth
sf alias set production=user@example.com

# Unset alias
sf alias unset production
```

## Set Default Org

```bash
# Set default target org
sf config set target-org production

# View config
sf config list
```

## Logout

```bash
# Logout from specific org
sf org logout --target-org production

# Logout from all orgs (careful!)
sf org logout --all
```

## Refresh Token

If authentication expires:

```bash
# Re-authenticate
sf org login web --instance-url <your-instance-url> --alias <existing-alias>
```

## Troubleshooting

### "Invalid grant" Error

Token expired or revoked. Re-authenticate:
```bash
sf org login web --alias <alias>
```

### "No authorization found"

Org not authenticated. Login first:
```bash
sf org login web
```

### Sandbox Refresh

After sandbox refresh, re-authenticate (tokens are invalidated):
```bash
sf org login web --instance-url https://test.salesforce.com --alias sandbox
```

### Check Auth Status

```bash
sf org list auth
```
