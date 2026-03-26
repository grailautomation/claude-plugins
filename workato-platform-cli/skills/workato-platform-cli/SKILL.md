---
name: workato-platform-cli
description: >-
  Workato Platform CLI reference for managing workspace-level assets. Use when the user
  asks about "workato-platform-cli", "workato platform cli", "workato init",
  "workato pull", "workato push", "workato recipes list",
  "workato recipes validate", "workato recipes start", "workato recipes stop",
  "workato connections create", "workato connections create-oauth", "workato profiles",
  "workato data-tables", "workato api-collections", "workato properties",
  "multi-environment deployment workato", "workspace management cli",
  "workato projects list", "workato assets", or needs to manage Workato workspace-level
  assets (recipes, connections, projects, data tables, environments) via the Python CLI.
  Package: pip install workato-platform-cli (Python 3.11+).
  NOT the Connector SDK CLI (Ruby gem for component-level connector development) --
  for that, use workato-connector-sdk-cli.
  NOT the Developer REST API (curl/httpx) -- for that, use workato-api.
version: 0.1.0
---

# Workato Platform CLI

A modern, type-safe Python CLI for the Workato API. Manage recipes, connections, projects, data tables, and API collections from the command line.

> **Not what you're looking for?**
> - For the **Connector SDK CLI** (Ruby gem `workato-connector-sdk` for local connector development and RSpec testing), see the `workato-connector-sdk-cli` skill.
> - For the **Developer REST API** (curl/httpx for programmatic API calls), see the `workato-api` skill.

## Prerequisites

- Python 3.11+
- Valid Workato account and API token
- Network access to Workato API endpoints

## Installation

```bash
pip install workato-platform-cli
workato --version
```

## Quick Setup

```bash
# 1. Initialize — interactive setup: region, API token, project selection
workato init

# 2. Verify workspace
workato workspace

# 3. Pull current project assets
workato pull
```

API tokens start with `wrk` followed by environment type (e.g., `wrkprod-`). Create via **Workspace Admin > API Clients**. See [overview.md](references/overview.md) for client role setup.

## Command Groups

| Group | Key Commands | Reference |
|-------|-------------|-----------|
| **Setup** | `init`, `workspace`, `profiles`, `guide` | [overview.md](references/overview.md) |
| **Projects** | `pull`, `push`, `projects list/use/switch`, `assets` | [command-reference.md](references/command-reference.md) |
| **Recipes** | `recipes list/validate/start/stop/update-connection` | [command-reference.md](references/command-reference.md) |
| **Connections** | `connections list/create/create-oauth/get-oauth-url/update/pick-list/pick-lists` | [command-reference.md](references/command-reference.md) |
| **Connectors** | `connectors list/parameters` | [command-reference.md](references/command-reference.md) |
| **API & Data** | `api-collections`, `api-clients`, `data-tables`, `properties` | [command-reference.md](references/command-reference.md) |
| **Workflows** | Multi-env deployment, CI/CD, recipe lifecycle | [use-cases.md](references/use-cases.md) |

## Common Workflows

### Multi-Environment Deployment

```bash
# Development
workato profiles use dev
workato push

# Staging
workato profiles use staging
workato pull
workato push --restart-recipes

# Production
workato profiles use production
workato pull
```

### Recipe Lifecycle

```bash
# Validate locally
workato recipes validate --path ./recipes/my_recipe.recipe.json

# Deploy and restart
workato push --restart-recipes

# Monitor
workato recipes list --running
workato recipes list --stop-cause trigger_errors_limit
```

### CI/CD Integration

```bash
# In CI pipeline
workato recipes validate --path ./recipes/*.json
workato push --restart-recipes --include-tags
```

### Connection Management

```bash
# List connections
workato connections list --provider salesforce

# Create OAuth connection
workato connections create-oauth --parent-id 12345 --external-id "user@example.com"

# Get OAuth URL for headless flows
workato connections get-oauth-url --id 12345
```

## Global Options

| Option | Description |
|--------|-------------|
| `--profile TEXT` | Profile to use (or `WORKATO_PROFILE` env var) |
| `--version` | Show CLI version |
| `--help` | Show help for any command |

## Environment Variables

- `WORKATO_PROFILE` — Default profile
- `WORKATO_API_TOKEN` — API token for authentication
- `WORKATO_HOST` — Custom API host URL

## Reference Files

- [**overview.md**](references/overview.md) — Features, prerequisites, authentication setup, installation, `workato init` configuration
- [**command-reference.md**](references/command-reference.md) — Complete command reference with usage, options, examples for all commands
- [**quick-start.md**](references/quick-start.md) — Getting started workflow, initial commands, role-based recommendations
- [**use-cases.md**](references/use-cases.md) — Workflow patterns for individual developers, teams, automation, and enterprise
