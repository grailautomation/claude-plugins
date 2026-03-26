## Workato Platform CLI Use Cases

Validated against the installed CLI on 2026-03-26: `workato, version 1.0.5`.

These are command patterns derived from the installed CLI help and package source. Output examples are intentionally omitted because they depend on the authenticated workspace, current project, and local filesystem state.

## Bootstrap a local project

Use this flow when setting up a workspace directory for the first time.

```bash
workato init
workato workspace
workato assets
workato pull
```

For non-interactive automation:

```bash
export WORKATO_API_TOKEN=...
export WORKATO_HOST=https://www.workato.com

workato init --non-interactive --project-id 12345 --folder-name customer-onboarding
```

## Manage environments with profiles

Use named profiles when you need to move between development, staging, and production.

```bash
workato profiles create dev
workato profiles create staging
workato profiles create production

workato profiles list
workato profiles use dev
workato profiles status
```

A simple promotion flow:

```bash
workato profiles use dev
workato push

workato profiles use staging
workato pull
workato push --restart-recipes

workato profiles use production
workato pull
```

## Validate and operate recipes

Use the recipes group for validation, lifecycle operations, and connection swaps.

```bash
workato recipes validate --path ./recipes/customer_onboarding.recipe.json
workato recipes list --running
workato recipes list --stop-cause trigger_errors_limit
workato recipes start --id 12345
workato recipes stop --id 12345
workato recipes update-connection 12345 --adapter-name salesforce --connection-id 67890
```

## Create and maintain connections

Inspect connector requirements before creating or updating connections.

```bash
workato connectors list --platform
workato connectors parameters --provider salesforce
workato connectors parameters --search oauth
```

Standard connection management:

```bash
workato connections list --provider salesforce
workato connections create --provider salesforce --name "Prod Salesforce"
workato connections update --connection-id 12345 --name "Prod Salesforce EU"
workato connections pick-lists --adapter salesforce
workato connections pick-list --id 12345 --pick-list-name objects
```

Runtime OAuth user flow:

```bash
workato connections create-oauth --parent-id 12345 --external-id "user@example.com"
workato connections get-oauth-url --id 12345
```

## Work with projects and assets

Use these commands when you need to inspect or switch the current project context.

```bash
workato projects list --source both
workato projects switch
workato projects use "Customer Onboarding"
workato workspace
workato assets
```

## Manage API collections and API clients

Use the API commands for OpenAPI imports and client credential management.

```bash
workato api-collections list
workato api-collections create --name "Customer API" --format json --content ./openapi.json
workato api-collections list-endpoints --api-collection-id 456
workato api-collections enable-endpoint --api-endpoint-id 789
```

```bash
workato api-clients list
workato api-clients create --name "Customer API Client" --api-collection-ids 456 --auth-type token
workato api-clients create-key --api-client-id 123 --name "Default key"
workato api-clients list-keys --api-client-id 123
workato api-clients refresh-secret --api-client-id 123 --api-key-id 456 --force
```

## Manage data tables and project properties

Use these commands for workspace data and configuration values.

```bash
workato data-tables list
workato data-tables create --name customers --schema-json '[{"name":"id","type":"integer","optional":false}]'
```

```bash
workato properties list --prefix customer_
workato properties upsert --property customer.base_url=https://example.com --property customer.timeout=30
```

## Use the built-in guide for AI and operator workflows

The CLI ships with a documentation interface that can be queried directly from the terminal.

```bash
workato guide topics
workato guide search recipes
workato guide search oauth --topic connections --max-results 5
workato guide content recipes
workato guide structure connections
workato guide index
```
