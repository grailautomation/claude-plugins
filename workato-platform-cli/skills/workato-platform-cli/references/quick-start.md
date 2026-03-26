## Workato Platform CLI Quick Start

Validated against the installed CLI on 2026-03-26: `workato, version 1.0.5`.

This is a short bootstrap flow for the `workato` binary from `workato-platform-cli`.

## 1. Install and verify

```bash
pip install workato-platform-cli
workato --version
workato --help
```

## 2. Initialize the workspace

Interactive setup:

```bash
workato init
```

Non-interactive setup:

```bash
export WORKATO_API_TOKEN=...
export WORKATO_HOST=https://www.workato.com

workato init --non-interactive --project-id 12345
```

## 3. Check current context

```bash
workato workspace
workato assets
```

## 4. Select the right project and profile

```bash
workato projects list --source both
workato projects use "Customer Onboarding"

workato profiles list
workato profiles use dev
workato profiles status
```

## 5. Validate and deploy recipe changes

```bash
workato recipes validate --path ./recipes/customer_onboarding.recipe.json
workato pull
workato push --restart-recipes
workato recipes list --running
```

`recipes list --running` shows running recipes, not execution logs.

## 6. Discover connection parameters before creating connections

```bash
workato connectors parameters --provider salesforce
workato connections create --provider salesforce --name "Prod Salesforce"
```

For runtime OAuth user connections:

```bash
workato connections create-oauth --parent-id 12345 --external-id "user@example.com"
workato connections get-oauth-url --id 12345
```

## 7. Use the built-in CLI documentation

```bash
workato guide topics
workato guide search recipes
workato guide content connections
```
