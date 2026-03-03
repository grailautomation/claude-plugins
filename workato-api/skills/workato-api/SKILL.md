---
name: workato-api
description: >-
  Workato Developer API reference and execution framework. Use this skill whenever:
  (1) the user asks about Workato recipes, connections, jobs, lookup tables, folders, projects, API platform, or workspace configuration,
  (2) the user wants to query, inspect, start/stop, or manage anything in their Workato workspace,
  (3) the user mentions Workato API, Workato automation, recipe lifecycle, deployment, or environment properties,
  (4) you need to make Workato API calls to answer a question or complete a task.
  This skill covers ALL Workato Developer API endpoints and provides curl-based execution patterns.
  There is no Workato Developer SDK — use bash/curl (or Python httpx) to call the REST API directly.
---

# Workato Developer API

This skill enables you to query and manage a Workato workspace via the Developer API. There is no SDK for the Developer API — all interactions use REST calls via curl or Python httpx.

## Workspace Configuration

If a `.local.md` file exists in this skill directory, read it for workspace-specific configuration (workspace ID, data center, jq path). Also check environment variables:

- `WORKATO_API_TOKEN` — Bearer token (required). From Workato API Client (Workspace Admin > API Clients).
- `WORKATO_WORKSPACE_ID` — Workspace ID override.
- `WORKATO_BASE_URL` — Base URL override (default: `https://www.workato.com`).

## Authentication

```bash
# Token is in the environment as WORKATO_API_TOKEN
# All requests use Bearer token auth:
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/<endpoint>"
```

If `WORKATO_API_TOKEN` is not set, tell the user to configure it. The token comes from a Workato API Client (Workspace Admin > API Clients).

**Base URLs by data center:**
- US: `https://www.workato.com/api/`
- EU: `https://app.eu.workato.com/api/`
- JP: `https://app.jp.workato.com/api/`
- SG: `https://app.sg.workato.com/api/`
- AU: `https://app.au.workato.com/api/`
- Event Streams: `https://event-streams.workato.com/api/v1/`

Default to US (`www.workato.com`) unless overridden by `WORKATO_BASE_URL` or `.local.md`.

## How to Use This Skill

1. **Identify which resource** the user is asking about from the Reference Files table below
2. **Read the corresponding reference file** for endpoint details, parameters, and response shapes
3. **Execute via curl** using the patterns in this file
4. **Parse responses with jq** — use `jq` (ensure it's installed; override path via `JQ` env var if needed)
5. **Handle pagination** according to the endpoint's pattern (see Response Patterns below)

For a complete index of all endpoints across all resources, see `references/endpoints-index.md`.

## Reference Files

Each file maps 1:1 to a Workato API resource category. Read the relevant file when you need endpoint details.

| Resource | Reference File | Key Endpoints |
|----------|---------------|---------------|
| Introduction & Auth | `references/introduction.md` | Base URLs, auth, HTTP codes |
| Recipes | `references/endpoints/recipes.md` | GET/POST/PUT/DELETE recipes, start/stop, reset trigger, poll now |
| Jobs | `references/endpoints/jobs.md` | List/get jobs, resume a job |
| Connections | `references/endpoints/connections.md` | List/create/update/delete/disconnect connections |
| Folders | `references/endpoints/folders.md` | List/create/delete folders and projects |
| Projects (Build/Deploy) | `references/endpoints/projects.md` | Build, deploy, list deployments |
| Lookup Tables | `references/endpoints/lookup-tables.md` | List tables, list/lookup/add/update/delete rows |
| Environment Properties | `references/endpoints/environment-properties.md` | List/upsert env properties by prefix |
| Project Properties | `references/endpoints/project-properties.md` | List/upsert project-scoped properties |
| Event Streams | `references/endpoints/event-streams.md` | Consume/publish messages, topic management |
| API Clients (Developer) | `references/endpoints/api-clients.md` | List/create/update/delete/regenerate dev API clients |
| API Platform | `references/endpoints/api-platform.md` | API collections, endpoints, platform clients, access profiles |
| Connectors | `references/endpoints/connectors.md` | Get connector metadata, list all platform connectors |
| Custom Connectors | `references/endpoints/custom-connectors.md` | Search/create/update/release/share custom connectors |
| Custom OAuth Profiles | `references/endpoints/custom-oauth-profiles.md` | List/create/update/delete OAuth profiles |
| Roles | `references/endpoints/roles.md` | List/copy custom roles |
| Workspace Collaborators | `references/endpoints/workspace-collaborators.md` | List/get/update members, invite collaborators |
| Workspace Details | `references/endpoints/workspace-details.md` | GET /api/users/me |
| Recipe Lifecycle Mgmt | `references/endpoints/recipe-lifecycle-management.md` | Export manifests, package export/import |
| On-Premise Agents | `references/endpoints/on-premise-agents.md` | List/create/delete OPA groups and agents |
| Test Automation | `references/endpoints/test-automation.md` | Run test cases, get results |
| Environment Management | `references/endpoints/environment-management.md` | Clear secrets cache, audit logs |
| All Endpoints Index | `references/endpoints-index.md` | Complete endpoint table across all resources |

## Response Envelope Patterns

Different endpoints use different response shapes — this matters for parsing with jq:

| Pattern | Endpoints | Shape | jq accessor |
|---------|-----------|-------|-------------|
| **Paginated items** | Recipes | `{ items: [...], count, page, per_page }` | `.items[]` |
| **Nested result** | Dev API Clients | `{ result: { items: [...], count, page, per_page } }` | `.result.items[]` |
| **Bare array** | Connections, Folders, Lookup Tables, Roles, Projects, On-Prem Agents | `[...]` | `.[]` |
| **Data/total** | Members, Activity Logs | `{ data: [...], total }` | `.data[]` |
| **Job-specific** | Jobs | `{ items: [...], job_count, job_succeeded_count, job_failed_count }` | `.items[]` |
| **Flat object** | Users/me, Properties | `{ key: value, ... }` | `.` |

## Common Workflows

### List all running recipes
```bash
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/recipes?running=true&per_page=100" \
  > /tmp/workato_response.json \
  && jq '.items[] | {id, name, last_run_at}' /tmp/workato_response.json
```

### Get recent failed jobs for a recipe
```bash
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/recipes/RECIPE_ID/jobs?status=failed" \
  > /tmp/workato_response.json \
  && jq '.items[] | {id, title, started_at, error}' /tmp/workato_response.json
```

### Search lookup table rows
```bash
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/lookup_tables/TABLE_ID/rows?by[column_name]=value" \
  > /tmp/workato_response.json \
  && jq '.' /tmp/workato_response.json
```

### Get workspace overview
```bash
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/users/me" \
  > /tmp/workato_response.json \
  && jq '{name, recipes_count, active_recipes_count, plan_id}' /tmp/workato_response.json
```

## Safety Rules

**Before executing any write operation** (POST, PUT, DELETE that creates, updates, or deletes data):
1. Confirm with the user what will be changed
2. Show the exact API call you plan to make
3. Wait for explicit approval

**Read-only operations** (GET) can be executed without confirmation.

**Rate limits:**
- Custom Connectors API: 1 request/second
- Event Streams (legacy domain): 1000 requests/minute
- General: no documented global rate limit, but be reasonable

## Execution Pattern

Always save response to a temp file first, then parse — this avoids pipe issues with jq:

```bash
curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  "https://www.workato.com/api/ENDPOINT" \
  > /tmp/workato_response.json \
  && jq 'QUERY' /tmp/workato_response.json
```

For write operations:
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WORKATO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  "https://www.workato.com/api/ENDPOINT" \
  > /tmp/workato_response.json \
  && jq '.' /tmp/workato_response.json
```

## Paginating Large Result Sets

For endpoints with page-based pagination, iterate:

```bash
page=1
while true; do
  curl -s -H "Authorization: Bearer $WORKATO_API_TOKEN" \
    "https://www.workato.com/api/recipes?per_page=100&page=$page" \
    > /tmp/workato_page.json
  count=$(jq '.items | length' /tmp/workato_page.json)
  jq '.items[]' /tmp/workato_page.json >> /tmp/workato_all.json
  [ "$count" -lt 100 ] && break
  page=$((page + 1))
done
```

For cursor-based pagination (Jobs use `offset_job_id`, Activity Logs use `page[after]`), see the respective reference files.

## Key Gotchas

- **Cannot update a running recipe** — stop it first
- **Job run-time data** (step inputs/outputs) is NOT available via API, only in Workato UI
- **Lookup table `lookup`** returns 404 on no match, not an empty result
- **Properties endpoint** (`/api/properties`) is overloaded — same path for environment and project properties, differentiated by `project_id` query param
- **Dev API client tokens** only appear in create/regenerate responses — store immediately
- **Package export/import and test runs** are async — poll with GET for status
- **OAuth connections** cannot be fully authenticated via API — only a shell connection is created
