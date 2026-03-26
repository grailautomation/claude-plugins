---
name: workato-platform-cli
description: >-
  Workato Platform CLI reference validated against the installed `workato` CLI.
  Use when the user asks about "workato-platform-cli", "workato platform cli",
  "workato init", "workato pull", "workato push", "workato workspace",
  "workato guide", "workato profiles", "workato projects",
  "workato recipes list", "workato recipes validate", "workato recipes start",
  "workato recipes stop", "workato recipes update-connection",
  "workato connections create", "workato connections create-oauth",
  "workato connections get-oauth-url", "workato data-tables",
  "workato api-collections", "workato api-clients", "workato properties",
  or needs to manage Workato workspace assets via the Python CLI package
  `workato-platform-cli` (`workato` binary). Not the Connector SDK CLI
  (`workato-connector-sdk`) and not direct Workato REST API usage.
version: 0.1.0
---

# Workato Platform CLI

Validated against the installed CLI on 2026-03-26: `workato, version 1.0.5`.

Use this skill for the `workato` binary from the Python package `workato-platform-cli`. It covers the help-visible command surface and the configuration behavior verified from the installed package.

> **Not what you're looking for?**
> - For the Ruby Connector SDK CLI used for connector development and RSpec testing, use `workato-connector-sdk-cli`.
> - For direct HTTP/API usage, use `workato-api`.

## Package Facts

- Package: `workato-platform-cli`
- Binary: `workato`
- Python requirement: 3.11+
- Global option: `--profile`
- Primary env vars: `WORKATO_PROFILE`, `WORKATO_API_TOKEN`, `WORKATO_HOST`

## First Run

```bash
workato init
workato workspace
workato pull
```

`workato init` detects `WORKATO_API_TOKEN` and `WORKATO_HOST` if they are already set. In non-interactive mode, the CLI requires either `--profile` or both auth inputs plus `--project-name` or `--project-id`.

## Command Groups

| Group | Commands | Reference |
|-------|----------|-----------|
| Setup | `init`, `workspace`, `profiles`, `guide` | [overview.md](references/overview.md) |
| Project sync | `pull`, `push`, `assets`, `projects list/switch/use` | [command-reference.md](references/command-reference.md) |
| Recipes | `recipes list/validate/start/stop/update-connection` | [command-reference.md](references/command-reference.md) |
| Connections | `connections list/create/create-oauth/get-oauth-url/update/pick-list/pick-lists` | [command-reference.md](references/command-reference.md) |
| Connectors | `connectors list/parameters` | [command-reference.md](references/command-reference.md) |
| API and data | `api-collections`, `api-clients`, `data-tables`, `properties` | [command-reference.md](references/command-reference.md) |

## Common Workflows

### Non-interactive bootstrap

```bash
export WORKATO_API_TOKEN=...
export WORKATO_HOST=https://www.workato.com

workato init --non-interactive --project-id 12345 --folder-name customer-onboarding
```

### Multi-environment deployment

```bash
workato profiles use dev
workato push

workato profiles use staging
workato pull
workato push --restart-recipes

workato profiles use production
workato pull
```

### Recipe lifecycle

```bash
workato recipes validate --path ./recipes/customer_onboarding.recipe.json
workato recipes list --running
workato recipes start --id 12345
workato recipes stop --id 12345
workato recipes update-connection 12345 --adapter-name salesforce --connection-id 67890
```

### Connection management

```bash
workato connectors parameters --provider salesforce
workato connections create --provider salesforce --name "Prod Salesforce" --input '{"security_token":"..."}'
workato connections create-oauth --parent-id 12345 --external-id "user@example.com"
workato connections get-oauth-url --id 12345
```

### API asset management

```bash
workato api-collections create --name "Customer API" --format json --content ./openapi.json
workato api-clients list
workato properties list --prefix customer_
workato data-tables list
```

## Notes

- `guide` is the built-in AI-facing documentation interface: `topics`, `search`, `content`, `structure`, and `index`.
- `init`, `projects list`, `profiles list`, `profiles rename`, and `profiles status` expose `--output-mode`; it is not a global flag.
- This skill uses the installed CLI as the source of truth. Prefer [command-reference.md](references/command-reference.md) when exact flags matter.

## Reference Files

- [overview.md](references/overview.md) - package facts, configuration, auth, project setup
- [command-reference.md](references/command-reference.md) - help-derived command and option reference
- [quick-start.md](references/quick-start.md) - short bootstrap flow for a new workspace
- [use-cases.md](references/use-cases.md) - validated command patterns for common workflows
