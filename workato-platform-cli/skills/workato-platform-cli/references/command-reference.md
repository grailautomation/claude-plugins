# Workato CLI Command Reference

## workato

```shell
Usage: workato [OPTIONS] COMMAND [ARGS]...

  CLI tool for the Workato API

Options:
  --profile TEXT  Profile to use for authentication and region settings
  --version       Show the version and exit.
  --help          Show this message and exit.

Commands:
  api-clients      Manage API clients
  api-collections  Manage API collections (generates recipes and...
  assets           List project assets (data tables, custom connectors,...
  connections      Manage connections
  connectors       Manage connectors
  data-tables      Manage data tables
  guide            AI agent documentation interface
  init             Initialize Workato CLI for a new project
  profiles         Manage Workato profiles for multi-environment...
  projects         Manage Workato projects
  properties       Manage project properties
  pull             Pull latest changes from Workato remote
  push             Push local project changes to Workato
  recipes          Manage recipes
  workspace        Show current workspace, user, and project details
```

## workato init

```shell
Usage: workato init [OPTIONS]

  Initialize Workato CLI for a new project

  Detects WORKATO_API_TOKEN and WORKATO_HOST environment variables if present.

Options:
  --profile TEXT                  Profile name to use (creates new if doesn't
                                  exist)
  --region [us|eu|jp|au|sg|custom]
                                  Workato region
  --api-token TEXT                Workato API token
  --api-url TEXT                  Custom API URL (required when region=custom)
  --project-name TEXT             Project name (creates new project with this
                                  name)
  --project-id INTEGER            Existing project ID to use
  --non-interactive               Run in non-interactive mode (requires all
                                  necessary options)
  --output-mode [table|json]      Output format: table (default) or json (only
                                  with --non-interactive)
  --folder-name TEXT              Custom folder name for the project (defaults
                                  to project name)
  --help                          Show this message and exit.
```

## workato workspace

```shell
Usage: workato workspace [OPTIONS]

  Show current workspace, user, and project details

Options:
  --help  Show this message and exit.
```

## workato pull

```shell
Usage: workato pull [OPTIONS]

  Pull latest changes from Workato remote

Options:
  --help  Show this message and exit.
```

## workato push

```shell
Usage: workato push [OPTIONS]

  Push local project changes to Workato

Options:
  --restart-recipes  Allow restarting of running recipes that are updated
                     during import. Stopped recipes will remain stopped.
  --include-tags     Include tags in import
  --help             Show this message and exit.
```

## workato assets

```shell
Usage: workato assets [OPTIONS]

  List project assets (data tables, custom connectors, properties, etc.)

Options:
  --folder-id INTEGER  Folder ID (uses current project folder if not
                       specified)
  --help               Show this message and exit.
```

## workato api-clients

```shell
Usage: workato api-clients [OPTIONS] COMMAND [ARGS]...

  Manage API clients

Options:
  --help  Show this message and exit.

Commands:
  create          Create a new API client
  create-key      Create a new API key for an existing API client
  list            List API clients, optionally filtered by project
  list-keys       List API keys for a specific API client
  refresh-secret  Refresh the secret for an existing API key
```

## workato api-clients create

```shell
Usage: workato api-clients create [OPTIONS]

  Create a new API client

Options:
  --name TEXT                     Name of the client  [required]
  --description TEXT              Description of the client
  --project-id INTEGER            ID of the project to create the client in
  --api-portal-id INTEGER         ID of the API portal to assign the client
  --email TEXT                    Email address for the client (required if
                                  api-portal-id provided)
  --api-collection-ids TEXT       Comma-separated list of API collection IDs
                                  to assign  [required]
  --api-policy-id INTEGER         ID of the API policy to apply
  --auth-type [token|jwt|oauth2|oidc]
                                  Authentication method (token, jwt, oauth2,
                                  oidc)  [required]
  --jwt-method [hmac|rsa]         JWT signing method (hmac or rsa) - required
                                  when auth-type is jwt
  --jwt-secret TEXT               HMAC shared secret or RSA public key -
                                  required when auth-type is jwt
  --oidc-issuer TEXT              Discovery URL for OIDC identity provider
  --oidc-jwks-uri TEXT            JWKS URL for OIDC identity provider
  --access-profile-claim TEXT     JWT claim key for access profile
                                  identification
  --required-claims TEXT          Comma-separated list of claims to enforce
  --allowed-issuers TEXT          Comma-separated list of allowed issuers
  --mtls-enabled                  Enable mutual TLS for this client
  --validation-formula TEXT       Formula to validate client certificates
  --cert-bundle-ids TEXT          Comma-separated list of certificate bundle
                                  IDs for mTLS
  --help                          Show this message and exit.
```

## workato api-clients create-key

```shell
Usage: workato api-clients create-key [OPTIONS]

  Create a new API key for an existing API client

Options:
  --api-client-id INTEGER  ID of the API client to create key for  [required]
  --name TEXT              Name of the API key  [required]
  --active / --inactive    Whether the API key is enabled (default: active)
  --ip-allow-list TEXT     Comma-separated list of IP addresses to allowlist
  --ip-deny-list TEXT      Comma-separated list of IP addresses to deny
  --help                   Show this message and exit.
```

## workato api-clients list

```shell
Usage: workato api-clients list [OPTIONS]

  List API clients, optionally filtered by project

Options:
  --project-id INTEGER  Filter API clients by project ID
  --help                Show this message and exit.
```

## workato api-clients list-keys

```shell
Usage: workato api-clients list-keys [OPTIONS]

  List API keys for a specific API client

Options:
  --api-client-id INTEGER  ID of the API client to list keys for  [required]
  --help                   Show this message and exit.
```

## workato api-clients refresh-secret

```shell
Usage: workato api-clients refresh-secret [OPTIONS]

  Refresh the secret for an existing API key

Options:
  --api-client-id INTEGER  ID of the API client  [required]
  --api-key-id INTEGER     ID of the API key to refresh  [required]
  --force                  Skip confirmation prompt
  --help                   Show this message and exit.
```

## workato api-collections

```shell
Usage: workato api-collections [OPTIONS] COMMAND [ARGS]...

  Manage API collections (generates recipes and endpoints from OpenAPI specs)

Options:
  --help  Show this message and exit.

Commands:
  create           Create a new API collection from OpenAPI spec (creates...
  enable-endpoint  Enable an API endpoint or all endpoints in a collection
  list             List API collections
  list-endpoints   List endpoints for an API collection
```

## workato api-collections create

```shell
Usage: workato api-collections create [OPTIONS]

  Create a new API collection from OpenAPI spec (creates recipes and
  endpoints)

Options:
  --name TEXT                    Name for the API collection (defaults to
                                 project name)
  --format [json|yaml|url]       Format of the OpenAPI spec  [required]
  --content TEXT                 Path to the spec file (for json/yaml) or URL
                                 (for url format)  [required]
  --proxy-connection-id INTEGER  ID of the proxy connection to use
  --help                         Show this message and exit.
```

## workato api-collections enable-endpoint

```shell
Usage: workato api-collections enable-endpoint [OPTIONS]

  Enable an API endpoint or all endpoints in a collection

Options:
  --api-endpoint-id INTEGER    ID of the API endpoint to enable
  --api-collection-id INTEGER  ID of the API collection (use with --all)
  --all                        Enable all endpoints in the collection
                               (requires --api-collection-id)
  --help                       Show this message and exit.
```

## workato api-collections list

```shell
Usage: workato api-collections list [OPTIONS]

  List API collections

Options:
  --page INTEGER      Page number (default: 1)
  --per-page INTEGER  Items per page (default: 100, max: 100)
  --help              Show this message and exit.
```

## workato api-collections list-endpoints

```shell
Usage: workato api-collections list-endpoints [OPTIONS]

  List endpoints for an API collection

Options:
  --api-collection-id INTEGER  ID of the API collection  [required]
  --help                       Show this message and exit.
```

## workato connections

```shell
Usage: workato connections [OPTIONS] COMMAND [ARGS]...

  Manage connections

Options:
  --help  Show this message and exit.

Commands:
  create         Create a new connection
  create-oauth   Create an OAuth runtime user connection
  get-oauth-url  Get OAuth authorization URL for a OAuth connection
  list           List connections with filtering options
  pick-list      Get pick list values from a connection
  pick-lists     List available pick lists by adapter
  update         Update an existing connection
```

## workato connections create

```shell
Usage: workato connections create [OPTIONS]

  Create a new connection

  Connection input parameters vary by provider. Use 'workato connectors
  parameters' to discover what parameters are required for each provider.

  Examples:

  # Find parameters for a provider workato connectors parameters --provider
  salesforce

  # Create connection with inline JSON workato connections create --provider
  salesforce --name "My Salesforce"   --input '{"security_token": "token"}'

  # Create shell connection (no authentication test) workato connections
  create --provider jira --name "Dev JIRA" --shell-connection

Options:
  --name TEXT          Name of the connection (e.g., "Prod JIRA connection")
                       [required]
  --provider TEXT      The application type/provider (e.g., "jira",
                       "salesforce")  [required]
  --parent-id INTEGER  ID of the parent connection (must be same provider
                       type)
  --folder-id INTEGER  ID of the project/folder (uses current project if not
                       specified)
  --external-id TEXT   External ID assigned to the connection
  --shell-connection   Create as shell connection (no authentication test)
  --input TEXT         Connection parameters as JSON string
  --help               Show this message and exit.
```

## workato connections create-oauth

```shell
Usage: workato connections create-oauth [OPTIONS]

  Create an OAuth runtime user connection

  This command creates a runtime user connection for OAuth-enabled providers.
  The parent connection must be an established OAuth connection. This
  initiates the OAuth flow and provides a URL for end user authorization.

  Parameters: - parent_id: ID of parent OAuth connector (connection must be
  established) - name: Optional name for the runtime user connection -
  folder_id: Folder to put connection (uses current project if not specified)
  - external_id: End user string ID for identifying the connection -
  callback_url: Optional URL called back after successful token acquisition -
  redirect_url: Optional URL where user is redirected after successful
  authorization

  Examples:

  # Create OAuth connection with minimal parameters workato connections
  create-oauth --parent-id 12345 --external-id "user@example.com"

  # Create with custom name and URLs workato connections create-oauth
  --parent-id 12345 --name "John's Google Drive"   --external-id
  "john.doe@company.com" --callback-url "https://myapp.com/oauth/callback"
  --redirect-url "https://myapp.com/success"

Options:
  --parent-id INTEGER  ID of the parent OAuth connection (must be
                       established/authorized)  [required]
  --name TEXT          Name of the runtime user connection (optional)
  --folder-id INTEGER  ID of the project/folder (uses current project if not
                       specified)
  --external-id TEXT   End user string ID for identifying the connection
                       [required]
  --callback-url TEXT  URL called back after successful token acquisition
                       (optional)
  --redirect-url TEXT  URL to redirect user after successful token acquisition
                       (optional)
  --help               Show this message and exit.
```

## workato connections get-oauth-url

```shell
Usage: workato connections get-oauth-url [OPTIONS]

  Get OAuth authorization URL for a OAuth connection

  This command retrieves the OAuth authorization URL for an existing OAuth
  connection. Use this if you need to re-authorize or get a fresh OAuth URL.

  Examples:

  # Get OAuth URL and open in browser workato connections get-oauth-url --id
  73389

  # Get OAuth URL without opening browser workato connections get-oauth-url
  --id 73389 --no-open-browser

Options:
  --id TEXT       OAuth connection ID  [required]
  --open-browser  Automatically open OAuth URL in browser
  --help          Show this message and exit.
```

## workato connections list

```shell
Usage: workato connections list [OPTIONS]

  List connections with filtering options

  Discover and manage connections in your workspace with detailed information
  about authorization status, providers, and relationships.

  Examples:

  # List all connections workato connections list

  # Filter by provider workato connections list --provider salesforce

  # Show only unauthorized connections workato connections list --unauthorized

  # List connections in specific folder workato connections list --folder-id
  123

  # Find child connections of a parent workato connections list --parent-id
  456

  # Include tags and runtime connections workato connections list --include-
  tags --include-runtime

Options:
  --folder-id INTEGER  Filter by folder ID
  --parent-id INTEGER  Filter by parent connection ID
  --external-id TEXT   Filter by external ID
  --include-runtime    Include runtime user connections
  --tags TEXT          Filter by connection tags
  --provider TEXT      Filter by provider type (e.g., salesforce, jira)
  --unauthorized       Show only authorized connections
  --help               Show this message and exit.
```

## workato connections pick-list

```shell
Usage: workato connections pick-list [OPTIONS]

  Get pick list values from a connection

Options:
  --id INTEGER           Connection ID  [required]
  --pick-list-name TEXT  Name of the pick list  [required]
  --params TEXT          Pick list params as JSON string (e.g.
                         '{"sobject_name": "Invoice__c"}')
  --help                 Show this message and exit.
```

## workato connections pick-lists

```shell
Usage: workato connections pick-lists [OPTIONS]

  List available pick lists by adapter

Options:
  --adapter TEXT  Show pick lists for a specific adapter/connector
  --help          Show this message and exit.
```

## workato connections update

```shell
Usage: workato connections update [OPTIONS]

  Update an existing connection

  Update connection properties like name, folder, parent, or authentication
  parameters. Use 'workato connectors parameters' to discover what parameters
  are available.

  Examples:

  # Update connection name workato connections update --connection-id 123
  --name "Updated Salesforce"

  # Move connection to different folder workato connections update
  --connection-id 123 --folder-id 456

  # Update authentication parameters workato connections update --connection-
  id 123 --input '{"username": "new@example.com", "password": "newpass"}'

  # Update from configuration file workato connections update --connection-id
  123 --input-file updated-config.json

  # Convert to shell connection workato connections update --connection-id 123
  --shell-connection true

Options:
  --connection-id INTEGER     ID of the connection to update  [required]
  --name TEXT                 New name for the connection
  --parent-id TEXT            ID of the parent connection (must be same
                              provider type)
  --folder-id INTEGER         ID of the project/folder to move connection to
  --external-id TEXT          External ID assigned to the connection
  --shell-connection BOOLEAN  Set as shell connection (true/false)
  --input TEXT                Updated connection parameters as JSON string
  --input-file TEXT           Path to JSON file containing updated connection
                              parameters
  --help                      Show this message and exit.
```

## workato connectors

```shell
Usage: workato connectors [OPTIONS] COMMAND [ARGS]...

  Manage connectors

Options:
  --help  Show this message and exit.

Commands:
  list        List connectors (platform connectors include trigger and...
  parameters  List connection parameters for connectors
```

## workato connectors list

```shell
Usage: workato connectors list [OPTIONS]

  List connectors (platform connectors include trigger and action metadata)

Options:
  --platform  List platform connectors with trigger and action metadata
  --custom    List custom connectors
  --help      Show this message and exit.
```

## workato connectors parameters

```shell
Usage: workato connectors parameters [OPTIONS]

  List connection parameters for connectors

  Shows configuration requirements for creating connections to different
  services.

Options:
  --provider TEXT  Show parameters for a specific provider
  --oauth-only     Show only OAuth-enabled providers
  --search TEXT    Search provider names (case-insensitive)
  --all            Output full schema as JSON
  --pretty         Pretty-print JSON output (use with --all)
  --help           Show this message and exit.
```

## workato data-tables

```shell
Usage: workato data-tables [OPTIONS] COMMAND [ARGS]...

  Manage data tables

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new data table with schema definition
  list    List all data tables using the Workato API
```

## workato data-tables create

```shell
Usage: workato data-tables create [OPTIONS]

  Create a new data table with schema definition

  Schema can be provided via --schema-json (JSON string).

  Schema format example: [     {         "name": "id",         "type":
  "integer",         "optional": false,         "hint": "Unique identifier"
  },     {         "name": "name",         "type": "string",
  "optional": false,         "default_value": "Unknown"     },     {
  "name": "created_at",         "type": "date_time",         "optional": true
  } ]

Options:
  --name TEXT          Name of the data table  [required]
  --folder-id INTEGER  Folder ID (uses current project folder if not
                       specified)
  --schema-json TEXT   JSON string containing table schema  [required]
  --help               Show this message and exit.
```

## workato data-tables list

```shell
Usage: workato data-tables list [OPTIONS]

  List all data tables using the Workato API

Options:
  --help  Show this message and exit.
```

## workato guide

```shell
Usage: workato guide [OPTIONS] COMMAND [ARGS]...

  AI agent documentation interface

Options:
  --help  Show this message and exit.

Commands:
  content    Get full content of a specific topic
  index      Generate full documentation index for AI consumption
  search     Search documentation content
  structure  Show structure and relationships for a topic
  topics     List all available documentation topics
```

## workato guide content

```shell
Usage: workato guide content [OPTIONS] TOPIC

  Get full content of a specific topic

Options:
  --help  Show this message and exit.
```

## workato guide index

```shell
Usage: workato guide index [OPTIONS]

  Generate full documentation index for AI consumption

Options:
  --help  Show this message and exit.
```

## workato guide search

```shell
Usage: workato guide search [OPTIONS] QUERY

  Search documentation content

Options:
  --topic TEXT           Limit to specific topic
  --max-results INTEGER  Maximum results to return
  --help                 Show this message and exit.
```

## workato guide structure

```shell
Usage: workato guide structure [OPTIONS] TOPIC

  Show structure and relationships for a topic

Options:
  --help  Show this message and exit.
```

## workato guide topics

```shell
Usage: workato guide topics [OPTIONS]

  List all available documentation topics

Options:
  --help  Show this message and exit.
```

## workato profiles

```shell
Usage: workato profiles [OPTIONS] COMMAND [ARGS]...

  Manage Workato profiles for multi-environment configurations

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new profile with API credentials
  delete  Delete a profile
  list    List all available profiles
  rename  Rename a profile
  show    Show details of a specific profile
  status  Show current profile status and configuration
  use     Set the current active profile (context-aware: workspace or...
```

## workato profiles create

```shell
Usage: workato profiles create [OPTIONS] PROFILE_NAME

  Create a new profile with API credentials

Options:
  --region [us|eu|jp|au|sg|custom]
                                  Workato region
  --api-token TEXT                Workato API token
  --api-url TEXT                  Custom API URL (required when region=custom)
  --non-interactive               Run in non-interactive mode (requires
                                  --region and --api-token)
  --help                          Show this message and exit.
```

## workato profiles delete

```shell
Usage: workato profiles delete [OPTIONS] PROFILE_NAME

  Delete a profile

Options:
  --yes   Confirm the action without prompting.
  --help  Show this message and exit.
```

## workato profiles list

```shell
Usage: workato profiles list [OPTIONS]

  List all available profiles

Options:
  --output-mode [table|json]  Output format: table (default) or json
  --help                      Show this message and exit.
```

## workato profiles rename

```shell
Usage: workato profiles rename [OPTIONS] OLD_NAME NEW_NAME

  Rename a profile

Options:
  --output-mode [table|json]  Output format: table (default) or json
  --yes                       Skip confirmation prompt
  --help                      Show this message and exit.
```

## workato profiles show

```shell
Usage: workato profiles show [OPTIONS] PROFILE_NAME

  Show details of a specific profile

Options:
  --help  Show this message and exit.
```

## workato profiles status

```shell
Usage: workato profiles status [OPTIONS]

  Show current profile status and configuration

Options:
  --output-mode [table|json]  Output format: table (default) or json
  --help                      Show this message and exit.
```

## workato profiles use

```shell
Usage: workato profiles use [OPTIONS] PROFILE_NAME

  Set the current active profile (context-aware: workspace or global)

Options:
  --help  Show this message and exit.
```

## workato projects

```shell
Usage: workato projects [OPTIONS] COMMAND [ARGS]...

  Manage Workato projects

Options:
  --help  Show this message and exit.

Commands:
  list    List available projects from local workspace and/or server
  switch  Interactively switch to a different project
  use     Switch to a specific project by name
```

## workato projects list

```shell
Usage: workato projects list [OPTIONS]

  List available projects from local workspace and/or server

Options:
  --profile TEXT                Profile to use for authentication and region
                                settings
  --source [local|remote|both]  Source of projects to list: local (default),
                                remote (server), or both
  --output-mode [table|json]    Output format: table (default) or json
  --help                        Show this message and exit.
```

## workato projects switch

```shell
Usage: workato projects switch [OPTIONS]

  Interactively switch to a different project

Options:
  --help  Show this message and exit.
```

## workato projects use

```shell
Usage: workato projects use [OPTIONS] PROJECT_NAME

  Switch to a specific project by name

Options:
  --help  Show this message and exit.
```

## workato properties

```shell
Usage: workato properties [OPTIONS] COMMAND [ARGS]...

  Manage project properties

Options:
  --help  Show this message and exit.

Commands:
  list    List project properties with a given prefix
  upsert  Upsert (create or update) project properties
```

## workato properties list

```shell
Usage: workato properties list [OPTIONS]

  List project properties with a given prefix

Options:
  --prefix TEXT         Property name prefix to filter by  [required]
  --project-id INTEGER  Project ID to get properties for. Defaults to current
                        project.
  --help                Show this message and exit.
```

## workato properties upsert

```shell
Usage: workato properties upsert [OPTIONS]

  Upsert (create or update) project properties

Options:
  --project-id INTEGER  Project ID to upsert properties for
  --property TEXT       Property in key=value format (can be used multiple
                        times)
  --help                Show this message and exit.
```

## workato recipes

```shell
Usage: workato recipes [OPTIONS] COMMAND [ARGS]...

  Manage recipes

Options:
  --help  Show this message and exit.

Commands:
  list               List recipes with optional filtering
  start              Start recipes (individual, all in project, or all in...
  stop               Stop recipes (individual, all in project, or all in...
  update-connection  Update a connection for a specific connector in a...
  validate           Validate a recipe file
```

## workato recipes list

```shell
Usage: workato recipes list [OPTIONS]

  List recipes with optional filtering

Options:
  --adapter-names-all TEXT        Comma-separated adapter names (recipes must
                                  use ALL)
  --adapter-names-any TEXT        Comma-separated adapter names (recipes must
                                  use ANY)
  --folder-id INTEGER             Return recipes in specified folder
  --order [activity|default]      Ordering method
  --running                       Return only running recipes
  --since-id INTEGER              Return recipes with IDs lower than this
                                  value
  --stopped-after TEXT            Exclude recipes stopped after this date (ISO
                                  8601 format)
  --stop-cause [trigger_errors_limit|action_quota_limit|trial_expired|txn_quota_limit]
                                  Filter by stop reason
  --updated-after TEXT            Include recipes updated after this date (ISO
                                  8601 format)
  --include-tags TEXT             Filter by recipe tags (comma-separated)
  --exclude-code                  Exclude recipe code from response (faster)
  --recursive                     Recursively list recipes in subfolders
  --help                          Show this message and exit.
```

## workato recipes start

```shell
Usage: workato recipes start [OPTIONS]

  Start recipes (individual, all in project, or all in folder)

Options:
  --id INTEGER         Recipe ID to start
  --all                Start all recipes in current project
  --folder-id INTEGER  Start all recipes in specified folder
  --help               Show this message and exit.
```

## workato recipes stop

```shell
Usage: workato recipes stop [OPTIONS]

  Stop recipes (individual, all in project, or all in folder)

Options:
  --id INTEGER         Recipe ID to stop
  --all                Stop all recipes in current project
  --folder-id INTEGER  Stop all recipes in specified folder
  --help               Show this message and exit.
```

## workato recipes update-connection

```shell
Usage: workato recipes update-connection [OPTIONS] RECIPE_ID

  Update a connection for a specific connector in a recipe

Options:
  --adapter-name TEXT      The internal name of the connector (e.g., box,
                           salesforce)  [required]
  --connection-id INTEGER  The ID of the connection to use  [required]
  --help                   Show this message and exit.
```

## workato recipes validate

```shell
Usage: workato recipes validate [OPTIONS]

  Validate a recipe file

Options:
  --path TEXT  Path to the recipe JSON file  [required]
  --help       Show this message and exit.
```

## Environment Variables

The CLI supports the following environment variables:

- **WORKATO_PROFILE**: Default profile to use
- **WORKATO_API_TOKEN**: API token for authentication
- **WORKATO_HOST**: Custom API host URL (or WORKATO_API_HOST)

## Global Patterns

The following patterns apply across all CLI commands and provide consistent behavior for authentication, data handling, and error management.

### Authentication

All commands require authentication through:

- Profile configuration (recommended)
- Environment variables
- Command-line options

### Pagination

List commands support pagination with:

- `--page INTEGER`: Page number (default: 1)
- `--per-page INTEGER`: Items per page (default varies, max: 100)

### Output Formats

Many commands support:

- `--output-mode table`: Human-readable table (default)
- `--output-mode json`: Machine-readable JSON

## Common Workflows

### Initial Setup

```bash
workato init                    # Interactive setup
workato workspace              # Verify configuration
workato pull                   # Sync with workspace
```

### Development Cycle

```bash
workato recipes validate --path recipe.json
workato push --restart-recipes
workato recipes list --running
```

### Connection Management

```bash
workato connectors list --search salesforce
workato connections create --provider salesforce --name "Prod SF"
workato connections create-oauth --parent-id 123 --external-id "user@example.com"
```

### API Management

```bash
workato api-collections create --name "Customer API" --format json --content ./openapi.json
workato api-collections list-endpoints --api-collection-id 456
workato api-collections enable-endpoint --api-endpoint-id 789
```
