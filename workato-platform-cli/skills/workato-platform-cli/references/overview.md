## Workato Platform CLI Overview

Validated against the installed CLI on 2026-03-26: `workato, version 1.0.5`.

`workato` is the command installed by the Python package `workato-platform-cli`. The installed package metadata declares `Requires-Python: >=3.11`.

## Command surface

The installed CLI exposes these top-level command groups:

- Setup and context: `init`, `workspace`, `profiles`, `guide`
- Project sync: `pull`, `push`, `assets`, `projects`
- Recipe and connection management: `recipes`, `connections`, `connectors`
- Workspace assets: `properties`, `data-tables`
- API assets: `api-collections`, `api-clients`

## Configuration and authentication

The CLI resolves configuration from profiles and environment variables:

- Global option: `--profile`
- Global profile env var: `WORKATO_PROFILE`
- Auth env vars detected by `workato init`: `WORKATO_API_TOKEN`, `WORKATO_HOST`

The `init` command supports these region values:

- `us`
- `eu`
- `jp`
- `au`
- `sg`
- `custom`

Interactive setup:

```bash
workato init
```

Non-interactive setup requires either `--profile` or both auth inputs, plus a project identifier:

```bash
export WORKATO_API_TOKEN=...
export WORKATO_HOST=https://www.workato.com

workato init --non-interactive --project-id 12345 --folder-name customer-onboarding
```

If you prefer named environments, the CLI exposes a dedicated profiles workflow:

```bash
workato profiles create dev
workato profiles list
workato profiles show dev
workato profiles use dev
workato profiles status
```

## Project workflow

Once initialized, the main project-oriented commands are:

```bash
workato workspace
workato projects list --source both
workato projects use "Customer Onboarding"
workato assets
workato pull
workato push --restart-recipes
```

`projects switch` is the interactive alternative to `projects use`.

## Recipe and connection workflow

Validated recipe lifecycle commands:

```bash
workato recipes list --running
workato recipes validate --path ./recipes/customer_onboarding.recipe.json
workato recipes start --id 12345
workato recipes stop --id 12345
workato recipes update-connection 12345 --adapter-name salesforce --connection-id 67890
```

Validated connection workflow commands:

```bash
workato connectors parameters --provider salesforce
workato connections create --provider salesforce --name "Prod Salesforce"
workato connections create-oauth --parent-id 12345 --external-id "user@example.com"
workato connections get-oauth-url --id 12345
workato connections update --connection-id 12345 --name "Renamed connection"
```

## Built-in documentation interface

The CLI includes an AI-oriented documentation interface under `guide`:

```bash
workato guide topics
workato guide search oauth
workato guide content connections
workato guide structure recipes
workato guide index
```

## Scope note

This overview stays within what the installed CLI and package metadata expose directly. When exact flags matter, defer to [command-reference.md](command-reference.md).
