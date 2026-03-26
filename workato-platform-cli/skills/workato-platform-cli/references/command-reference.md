## Workato CLI command reference

Command reference for the Workato Platform CLI tool.

---

## workato

Root command for the Workato Platform CLI. Provides access to all Workato automation and integration management capabilities.

### Usage

```shell
workato [GLOBAL_OPTIONS] <COMMAND> [COMMAND_OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--profile TEXT** | Profile to use for authentication and region settings. You can also set using the \`WORKATO\_PROFILE\` environment variable. |
| **\--version** | Show the CLI version and exit. |
| **\--help** | Show help message and available commands. |

### Result

Displays available commands and global options when run without arguments.

### Examples

Show all available commands.

```bash
workato --help
```

Use a specific profile.

```bash
workato --profile production recipes list
```

---

## workato init

Initialize the Workato CLI for a new project. Sets up authentication, selects region, and configures project workspace.

### Usage

```shell
workato init [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--profile TEXT** | Profile name to use. Creates new profile if it doesn't exist. |
| **\--region CHOICE** | Workato region, such as US, EU, JP, AU, SG, or custom. |
| **\--api-token TEXT** | Workato API token for authentication. |
| **\--api-url TEXT** | Custom API URL. Required when using a custom region. |
| **\--project-name TEXT** | Name text for the new project. |
| **\--project-id INTEGER** | Use existing project ID. |
| **\--non-interactive** | Run without prompts. Requires all options. |
| **\--output-mode CHOICE** | Output format, including table (default) and JSON. |

### Result

Creates configuration files, authenticates with the Workato API, and sets up project structure.

### Examples

Interactive setup

```bash
workato init
```

Non-interactive setup with a specific region.

```bash
workato init --profile prod --region eu --api-token wrkprod-xxx --project-name 'Production Integration'
```

---

## workato workspace

Display current workspace information, including active profile, project, and connection status.

### Usage

```shell
workato workspace
```

### Result

Shows current profile, project details, API endpoint, and authentication status.

### Examples

Check current workspace.

```bash
workato workspace
```

---

## workato pull

Pull latest assets from Workato workspace to local project directory. Synchronizes recipes, connections, and data tables.

### Usage

```shell
workato pull [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--force** | Overwrite local changes without confirmation. |

### Result

Downloads and updates local files with latest versions from Workato workspace.

### Examples

Pull the latest changes.

```bash
workato pull
```

Force pull and overwrite local changes.

```bash
workato pull --force
```

---

## workato push

Push local changes to Workato workspace. Uploads modified recipes, connections, and other assets.

### Usage

```shell
workato push [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--force** | Push changes without confirmation prompts. |
| **\--restart-recipes** | Automatically restart affected running recipes after push. |

### Result

Uploads local changes to Workato workspace and optionally restarts recipes.

### Examples

Push changes with confirmation.

```bash
workato push
```

Force push and restart recipes.

```bash
workato push --force --restart-recipes
```

---

List all configured authentication profiles with their regions and status.

### Usage

```shell
workato profiles list
```

### Result

Displays table of profiles showing name, region, API endpoint, and active status.

### Examples

Show all profiles.

```bash
workato profiles list
```

---

Switch to a different authentication profile for subsequent commands.

### Usage

```shell
workato profiles use <PROFILE_NAME>
```

### Input

| Input | Description |
| --- | --- |
| **PROFILE\_NAME** | Name of the profile to activate. |

### Result

Sets the specified profile as active for future CLI operations.

### Examples

Switch to production profile.

```bash
workato profiles use production
```

---

Displays the current active profile and its configuration details.

### Usage

```shell
workato profiles status
```

### Options

| Option | Description |
| --- | --- |
| **\--verbose, -v** | Optional. Show detailed profile information including API endpoint and authentication status. |
| **\--json\`** | Optional. Output profile status in JSON format for scripting. |

### Result

Shows the name of the active profile, associated workspace, and connection status.

### Examples

Check which profile is currently active.

```bash
workato profiles status
```

View detailed profile configuration.

```bash
workato profiles status --verbose
```

Get profile status in JSON format for automation.

```bash
workato profiles status --json
```

---

Remove a profile from the CLI configuration.

### Usage

```shell
workato profiles delete <PROFILE_NAME>
```

### Input

| Input | Description |
| --- | --- |
| **PROFILE\_NAME** | Name of the profile to delete. |

### Result

Removes the specified profile and its associated configuration.

### Examples

Delete development profile.

```bash
workato profiles delete development
```

---

## workato projects list

List all available projects in the current Workato workspace.

### Usage

```shell
workato projects list
```

### Result

Displays table of projects with ID, name, description, and folder count.

### Examples

Show all projects.

```bash
workato projects list
```

---

## workato projects use

Switch to a different project context for CLI operations.

### Usage

```shell
workato projects use <PROJECT_NAME>
```

### Input

| Input | Description |
| --- | --- |
| **PROJECT\_NAME** | Name of the project to switch to. |

### Result

Changes active project context and updates local workspace.

### Examples

Switch to customer integration project.

```bash
workato projects use 'Customer Integration'
```

---

## workato recipes list

List recipes in the workspace with filtering and pagination options.

### Usage

```shell
workato recipes list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--folder-id INTEGER** | Filter recipes by folder ID. |
| **\--running** | Show only currently running recipes. |
| **\--page INTEGER** | Page number for pagination. Default is 1. |
| **\--per-page INTEGER** | Number of recipes per page. Default is 10. Maximum is 100. |
| **\--adapter-names-all TEXT** | Comma-separated adapter names. Recipes must use all specified. |
| **\--adapter-names-any TEXT** | Comma-separated adapter names. Recipes must use any specified. |
| **\--order CHOICE** | Sort order: activity or default. |

### Result

Displays table of recipes with ID, name, status, folder, and last activity.

### Examples

List all recipes

```bash
workato recipes list
```

Show running recipes in specific folder

```bash
workato recipes list --folder-id 123 --running
```

Find recipes using Salesforce

```bash
workato recipes list --adapter-names-any salesforce
```

---

## workato recipes validate

Validate recipe JSON file syntax and structure against Workato schema requirements.

### Usage

```shell
workato recipes validate --path <FILE_PATH>
```

### Options

| Option | Description |
| --- | --- |
| **\--path TEXT** | Path to the recipe JSON file to validate. |

### Result

Reports validation results including syntax errors, missing fields, and schema violations.

### Examples

Validate recipe file.

```bash
workato recipes validate --path ./my_recipe.recipe.json
```

---

## workato recipes start

Start a stopped recipe by ID or name, enabling it to process triggers and execute actions.

### Usage

```shell
workato recipes start [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--id TEXT** | Recipe ID to start. |
| **\--name TEXT** | Recipe name to start. Use as an alternative to ID. |
| **\--folder-id TEXT** | Folder ID to help locate recipe by name. |

### Result

Starts the specified recipe and reports the new running status.

### Examples

Start recipe by ID.

```bash
workato recipes start --id 12345
```

Start recipe by name.

```bash
workato recipes start --name 'Daily Sales Report'
```

---

## workato recipes stop

Stop a running recipe, preventing it from processing new triggers while completing current jobs.

### Usage

```shell
workato recipes stop [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--id TEXT** | Recipe ID to stop. |
| **\--name TEXT** | Recipe name to stop. Use as alternative to ID. |
| **\--folder-id TEXT** | Folder ID to help locate recipe by name. |

### Result

Stops the specified recipe and reports the new stopped status.

### Examples

Stop recipe by ID.

```bash
workato recipes stop --id 12345
```

Stop recipe by name in specific folder.

```bash
workato recipes stop --name 'Data Sync' --folder-id 456
```

---

## workato recipes update-connection

Updates the connection used by a specific connector in a stopped recipe.

### Usage

```shell
workato recipes update-connection RECIPE_ID [OPTIONS]
```

### Input

| Input | Description |
| --- | --- |

### Options

| Option | Description |
| --- | --- |
| **\--adapter-name, -a** | Name of the adapter or connector to update. |
| **\--connection-id, -c** | Required. ID of the connection from your workspace to use. Must be a valid connection ID. |

### Result

The recipe's connection for the specified adapter is updated to use the new connection. The recipe must be stopped before you can perform this operation.

### Examples

Update a Salesforce connection in a recipe.

```bash
workato recipes update-connection 12345 --adapter-name salesforce --connection-id 67890
```

Switch Slack connection for a notification recipe.

```bash
workato recipes update-connection 54321 -a slack -c 98765
```

---

## workato connections list

List all connections in the workspace with filtering options for provider, folder, and external ID.

### Usage

```shell
workato connections list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--provider TEXT** | Filter by connector provider. |
| **\--folder-id INTEGER** | Filter connections by folder ID |
| **\--external-id TEXT** | Filter by external identifier for runtime connections. |
| **\--parent-id INTEGER** | Filter by parent connection ID |

### Result

Displays table of connections with ID, name, provider, status, and folder information.

### Examples

List all connections.

```bash
workato connections list
```

Show Salesforce connections.

```bash
workato connections list --provider salesforce
```

List connections in specific folder.

```bash
workato connections list --folder-id 789
```

---

## workato connections create

Create a new connection for a specific application provider with authentication details.

### Usage

```shell
workato connections create [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--name TEXT** | Name for the connection. |
| **\--provider TEXT** | Application provider name. |
| **\--folder-id INTEGER** | Folder ID where connection should be stored. |
| **\--input TEXT** | JSON string with connection parameters. |
| **\--parent-id INTEGER** | Parent connection ID for child connections. |

### Result

Creates new connection and returns connection ID and authentication status.

### Examples

Create Salesforce connection.

```bash
workato connections create --name 'Prod SF' --provider salesforce
```

Create connection with parameters.

```bash
workato connections create --name 'JIRA Prod' --provider jira --input '{"server_url":"https://company.atlassian.net"}'
```

---

## workato connections create-oauth

Create OAuth-based connection by opening browser for user authentication flow.

### Usage

```shell
workato connections create-oauth [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--name TEXT** | Name for the OAuth connection. |
| **\--provider TEXT** | OAuth provider identifier. |
| **\--external-id TEXT** | External identifier for runtime user connections. |
| **\--parent-id INTEGER** | Parent connection ID for OAuth child connections. |

### Result

Opens browser for OAuth flow and creates authenticated connection upon completion.

### Examples

Create OAuth connection.

```bash
workato connections create-oauth --name 'Google Drive OAuth' --provider google_drive
```

---

## workato connections get-oauth-url

Generates the OAuth authorization URL for establishing a new connection.

### Usage

```shell
workato connections get-oauth-url CONNECTION_ID [OPTIONS]
```

### Input

| Input | Description |
| --- | --- |

### Options

| Option | Description |
| --- | --- |
| **\--redirect-url** | Custom redirect URL for OAuth callback. Optional. Uses default if not specified. |

### Result

Returns the OAuth authorization URL that users must visit to grant permissions and authenticate the connection.

### Examples

Get OAuth URL for a new Salesforce connection.

```bash
workato connections get-oauth-url 12345
```

Generate OAuth URL with custom redirect.

```bash
workato connections get-oauth-url 12345 --redirect-url https://example.com/callback
```

---

## workato connections update

Update existing connection properties such as name or configuration parameters.

### Usage

```shell
workato connections update [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--connection-id INTEGER** | ID of the connection to update. |
| **\--name TEXT** | New name for the connection. |
| **\--input TEXT** | JSON string with updated connection parameters. |

### Result

Updates connection properties and returns confirmation of changes.

### Examples

Update connection name.

```bash
workato connections update --connection-id 123 --name 'Updated Connection Name'
```

---

## workato connections pick-list

Retrieve dynamic pick list values from a connection for use in recipe configuration.

### Usage

```shell
workato connections pick-list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--connection-id INTEGER** | ID of the connection to query. |
| **\--object-name TEXT** | Name of the object/pick list to retrieve. |
| **\--parameters TEXT** | JSON parameters for the pick list query. |

### Result

Returns available pick list options that can be used in recipe field mappings.

### Examples

Get Salesforce objects.

```bash
workato connections pick-list --connection-id 123 --object-name sobjects
```

---

## workato connectors list

List all available connectors in the Workato platform, including both standard and custom connectors.

### Usage

```shell
workato connectors list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--custom** | Show only custom connectors. |

### Result

Displays table of connectors with name, provider ID, authentication type, and availability.

### Examples

List all connectors.

```bash
workato connectors list
```

Show only custom connectors.

```bash
workato connectors list --custom
```

---

## workato connectors parameters

Show connection parameters and authentication requirements for specific connectors.

### Usage

```shell
workato connectors parameters [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--provider TEXT** | Show parameters for specific provider or connector. |
| **\--oauth-only** | Show only OAuth-enabled connectors. |
| **\--search TEXT** | Search connector names. Case-insensitive). |

### Result

Displays connection fields, authentication methods, and configuration options.

### Examples

Show Salesforce connection parameters.

```bash
workato connectors parameters --provider salesforce
```

Find OAuth connectors.

```bash
workato connectors parameters --oauth-only
```

---

## workato data-tables list

List all data tables in the current workspace with schema and record count information.

### Usage

```shell
workato data-tables list
```

### Result

Displays table of data tables with ID, name, schema fields, and record counts.

### Examples

Show all data tables.

```bash
workato data-tables list
```

---

## workato data-tables create

Create a new data table with specified schema for storing structured data in recipes.

### Usage

```shell
workato data-tables create [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--name TEXT** | Name for the new data table. |
| **\--folder-id INTEGER** | Folder ID where table should be created. |
| **\--schema-json TEXT** | JSON schema definition for table fields. |

### Result

Creates new data table and returns table ID and schema confirmation.

### Examples

Create simple data table.

```bash
workato data-tables create --name 'Customer Data'
```

Create table with schema.

```bash
workato data-tables create --name 'Products' --schema-json '[{"name":"product_id","type":"string","optional":false}]'
```

---

## workato properties list

List environment or project properties that can be used in recipes for configuration management.

### Usage

```shell
workato properties list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--prefix TEXT** | Filter properties by name prefix, for example 'salesforce\_'. |
| **\--project-id INTEGER** | Show project-specific properties instead of environment properties. |

### Result

Displays properties with names, values (masked for sensitive data), and scope.

### Examples

List all properties.

```bash
workato properties list
```

Show Salesforce-related properties.

```bash
workato properties list --prefix salesforce_
```

---

## workato properties upsert

Create or update properties for environment or project-level configuration.

### Usage

```shell
workato properties upsert [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--project-id INTEGER** | Target project for property updates. |
| **\--file TEXT** | JSON file containing property key-value pairs. |
| **\--key-value TEXT** | Single property in key=value format. |

### Result

Creates or updates properties and confirms changes made.

### Examples

Update property from file

```bash
workato properties upsert --project-id 123 --file properties.json
```

Set single property

```bash
workato properties upsert --key-value api_endpoint=https://api.example.com
```

---

List API collections that expose recipes as REST endpoints for external consumption.

### Usage

```shell
workato api-collections list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--page INTEGER** | Page number for pagination. Default is 1. |
| **\--per-page INTEGER** | Number of collections per page. Default is 100. Maximum is 100. |

### Result

Displays API collections with ID, name, project, and endpoint count.

### Examples

List all API collections.

```bash
workato api-collections list
```

---

Create a new API collection to group and manage recipe endpoints.

### Usage

```shell
workato api-collections create [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--name TEXT** | Name for the API collection Default is project name. |
| **\--project-id INTEGER** | Project ID where collection should be created. |

### Result

Creates new API collection and returns collection ID and configuration details.

### Examples

Create API collection.

```bash
workato api-collections create --name 'Customer API'
```

---

List all API endpoints within a specific collection showing their status and configuration.

### Usage

```shell
workato api-collections list-endpoints [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--api-collection-id INTEGER** | ID of the API collection to examine. |

### Result

Displays endpoints with ID, name, HTTP method, path, and enabled status.

### Examples

Show endpoints in collection.

```bash
workato api-collections list-endpoints --api-collection-id 456
```

---

Enable a specific API endpoint to make it available for external API calls.

### Usage

```shell
workato api-collections enable-endpoint [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--api-endpoint-id INTEGER** | ID of the API endpoint to enable. |

### Result

Enables the endpoint and provides the public URL for API access.

### Examples

Enable API endpoint.

```bash
workato api-collections enable-endpoint --api-endpoint-id 789
```

---

## workato api-clients list

List API clients used for programmatic access to Workato APIs with their permissions and status.

### Usage

```shell
workato api-clients list [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--project-id INTEGER** | Filter API clients by project ID. |

### Result

Displays API clients with ID, name, description, and permission scope.

### Examples

List all API clients.

```bash
workato api-clients list
```

---

## workato api-clients create

Create a new API client for programmatic access to Workato APIs.

### Usage

```shell
workato api-clients create [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--name TEXT** | Name for the API client. |
| **\--description TEXT** | Description of the API client's purpose. |
| **\--project-id INTEGER** | Project ID to associate with the client. |

### Result

Creates API client and returns client ID and initial access credentials.

### Examples

Create API client.

```bash
workato api-clients create --name 'Integration Client' --description 'For external system integration'
```

---

## workato guide topics

List all available documentation topics in the integrated help system.

### Usage

```shell
workato guide topics
```

### Result

Displays available help topics with descriptions and content summaries.

### Examples

Show all help topics.

```bash
workato guide topics
```

---

Search the integrated documentation for specific terms or concepts.

### Usage

```shell
workato guide search <QUERY> [OPTIONS]
```

### Input

| Input | Description |
| --- | --- |
| **QUERY** | Search terms to find in documentation. |

### Options

| Option | Description |
| --- | --- |
| **\--topic TEXT** | Limit search to specific topic area. |
| **\--max-results INTEGER** | Maximum number of results to return (default: 10) |

### Result

Returns relevant documentation sections with highlighted search terms.

### Examples

Search for connection help.

```bash
workato guide search 'oauth connection'
```

Search within recipes topic.

```bash
workato guide search 'trigger' --topic recipes --max-results 5
```

---

## workato guide content

Display the full content of a specific documentation topic.

### Usage

```shell
workato guide content <TOPIC>
```

### Input

| Input | Description |
| --- | --- |
| **TOPIC** | Name of the documentation topic to display. |

### Result

Shows complete documentation content for the specified topic.

### Examples

Show recipe documentation.

```bash
workato guide content recipes
```

---

## workato assets

List all assets in the current workspace including recipes, connections, data tables, and folders.

### Usage

```shell
workato assets [OPTIONS]
```

### Options

| Option | Description |
| --- | --- |
| **\--output-format CHOICE** | Output format: table (default) or json |

### Result

Displays comprehensive asset inventory with types, names, IDs, and folder locations.

### Examples

Show all assets.

```bash
workato assets
```

Export assets as JSON.

```bash
workato assets --output-format json
```

---

## Environment Variables

The CLI supports the following environment variables:

- **WORKATO\_PROFILE**: Default profile to use
- **WORKATO\_API\_TOKEN**: API token for authentication
- **WORKATO\_API\_HOST**: Custom API host URL

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

- `--output-format table`: Human-readable table (default)
- `--output-format json`: Machine-readable JSON

The CLI provides the following features to assist you with errors:

- Detailed error messages with context
- Suggestions for common issues
- HTTP status code information for API errors
- Validation feedback for malformed inputs

## Common Workflows

The following examples demonstrate typical workflows for getting started, developing recipes, managing connections, and working with APIs. These patterns can be combined and adapted to fit your specific requirements.

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
workato connections create-oauth --parent-id 123
```

### API Management

```bash
workato api-collections create --name "Customer API"
workato api-collections list-endpoints --api-collection-id 456
workato api-collections enable-endpoint --api-endpoint-id 789
```

  
**Last updated:** 11/3/2025, 7:56:11 PM