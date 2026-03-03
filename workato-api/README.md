# workato-api

Workato Developer API reference and execution framework for managing workspace resources via REST.

## What This Plugin Does

Provides Claude Code with complete reference documentation for all 120+ Workato Developer API endpoints across 21 resource categories. When activated, Claude can:

- Query and manage Workato recipes, connections, jobs, lookup tables, folders, and projects
- Execute API calls via curl with proper authentication and response parsing
- Handle pagination, response envelope variations, and async operations
- Follow safety rules (confirm before write operations)

## Setup

### 1. API Token

Create a Developer API Client in your Workato workspace:
**Workspace Admin > API Clients > Create client**

Set the token as an environment variable:

```bash
export WORKATO_API_TOKEN="your-token-here"
```

### 2. Optional: Workspace Configuration

Create a `.local.md` file in `skills/workato-api/` with your workspace-specific config:

```markdown
## Workspace Configuration

- Workspace ID: YOUR_WORKSPACE_ID
- Workspace name: Your Workspace
- Data center: US (www.workato.com)
```

Or use environment variables:

```bash
export WORKATO_WORKSPACE_ID="your-workspace-id"
export WORKATO_BASE_URL="https://www.workato.com"  # US default
```

### 3. Script Usage

The included curl wrapper script simplifies API calls:

```bash
./scripts/workato_api.sh GET /api/users/me
./scripts/workato_api.sh GET "/api/recipes?per_page=10&running=true"
./scripts/workato_api.sh POST /api/recipes '{"recipe":{"name":"test"}}'
```

## Data Centers

| Region | Base URL |
|--------|----------|
| US | `https://www.workato.com` |
| EU | `https://app.eu.workato.com` |
| JP | `https://app.jp.workato.com` |
| SG | `https://app.sg.workato.com` |
| AU | `https://app.au.workato.com` |

## Resource Categories

Recipes, Jobs, Connections, Folders, Projects, Lookup Tables, Environment Properties, Project Properties, Event Streams, API Clients, API Platform, Connectors, Custom Connectors, Custom OAuth Profiles, Roles, Workspace Collaborators, Workspace Details, Recipe Lifecycle Management, On-Premise Agents, Test Automation, Environment Management.
