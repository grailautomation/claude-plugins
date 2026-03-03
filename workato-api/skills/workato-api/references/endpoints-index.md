# Workato API Resources

## API clients

| Type  | Resource                                                                                 | Description                          |
|-------|------------------------------------------------------------------------------------------|--------------------------------------|
| GET   | [/api/developer_api_clients](https://www.workato.com/workato-api/api-client-apis.html#list-developer-api-clients) | List **Developer API Clients**.      |
| POST  | [/api/developer_api_clients](https://www.workato.com/workato-api/api-client-apis.html#create-developer-api-client) | Create a **Developer API Client**.   |
| GET   | [/api/developer_api_clients/:id](https://www.workato.com/workato-api/api-client-apis.html#get-developer-api-client-by-id) | Get a **Developer API Client by ID**.|
| PUT   | [/api/developer_api_clients/:id](https://www.workato.com/workato-api/api-client-apis.html#update-developer-api-client) | Update a **Developer API Clients**.  |
| DELETE| [/api/developer_api_clients/:id](https://www.workato.com/workato-api/api-client-apis.html#delete-developer-api-client) | Delete a **Developer API Client**.   |
| POST  | [/api/developer_api_clients/:id/regenerate](https://www.workato.com/workato-api/api-client-apis.html#regenerate-developer-api-client-token) | Regenerate a **Developer API Client token**. |
| GET   | [/api/developer_api_client_roles](https://www.workato.com/workato-api/api-client-apis.html#list-developer-api-client-roles) | List **Developer API Client roles**. |

---

## API Platform

| Type  | Resource                                                                                     | Description                         |
|-------|----------------------------------------------------------------------------------------------|-------------------------------------|
| GET   | [/api/api_collections](https://www.workato.com/workato-api/api-platform.html#list-api-collections) | List API collections.               |
| POST  | [/api/api_collections](https://www.workato.com/workato-api/api-platform.html#create-api-collection) | Create an API collection.           |
| GET   | [/api/api_endpoints](https://www.workato.com/workato-api/api-platform.html#list-api-endpoints) | List API endpoints in a collection. |
| PUT   | [/api/api_endpoints/:id/enable](https://www.workato.com/workato-api/api-platform.html#enable-api-endpoint) | Enable an API endpoint in a collection. |
| PUT   | [/api/api_endpoints/:id/disable](https://www.workato.com/workato-api/api-platform.html#disable-api-endpoint) | Disable an API endpoint in a collection. |
| GET   | [/api/api_clients](https://www.workato.com/workato-api/api-platform.html#list-api-clients)  | List API clients.                   |
| POST  | [/api/api_clients](https://www.workato.com/workato-api/api-platform.html#create-api-client)  | Create an API client.               |
| GET   | [/api/api_access_profiles](https://www.workato.com/workato-api/api-platform.html#list-access-profiles) | List access profiles belonging to an API client. |
| POST  | [/api/api_access_profiles](https://www.workato.com/workato-api/api-platform.html#create-access-profile) | Create an access profile belonging to an API client. |
| PUT   | [/api/api_access_profiles](https://www.workato.com/workato-api/api-platform.html#update-access-profile) | Update an access profile belonging to an API client. |
| PUT   | [/api_access_profiles](https://www.workato.com/workato-api/api-platform.html#enable-access-profile) | Enable an access profile belonging to an API client. |
| PUT   | [/api_access_profiles](https://www.workato.com/workato-api/api-platform.html#disable-access-profile) | Disable an access profile belonging to an API client. |
| PUT   | [/api/api_access_profiles/:id/refresh_secret](https://www.workato.com/workato-api/api-platform.html#refresh-token-secret) | Refresh access profile key or secret. |

---

## Connections

| Type  | Resource                                                              | Description                           |
|-------|-----------------------------------------------------------------------|---------------------------------------|
| GET   | [/api/connections](https://www.workato.com/workato-api/connections.html) | List connections belonging to user.   |

---

## Custom connectors

| Type  | Resource                                                                                   | Description                           |
|-------|--------------------------------------------------------------------------------------------|---------------------------------------|
| GET   | [/api/custom_connectors](https://www.workato.com/workato-api/custom_connectors.html#search-custom-connector) | Get custom connectors.                |
| POST  | [/api/sdk/generate_schema/json](https://www.workato.com/workato-api/custom_connectors.html#generate-schema-from-json) | Generates Workato schema from a stringified JSON sample. |
| POST  | [/api/sdk/generate_schema/csv](https://www.workato.com/workato-api/custom_connectors.html#generate-schema-from-csv) | Generates Workato schema from a stringified CSV sample. |

---

## Custom OAuth profiles

| Type  | Resource                                                                                     | Description                            |
|-------|----------------------------------------------------------------------------------------------|----------------------------------------|
| GET   | [/api/custom_oauth_profiles](https://www.workato.com/workato-api/custom-oauth-profiles.html#list-custom-oauth-profiles) | List Custom OAuth profiles             |
| GET   | [/api/custom_oauth_profiles/:id](https://www.workato.com/workato-api/custom-oauth-profiles.html#get-custom-oauth-profile-by-id) | Get Custom OAuth profile by ID         |
| POST  | [/api/custom_oauth_profiles](https://www.workato.com/workato-api/custom-oauth-profiles.html#create-custom-oauth-profile) | Create Custom OAuth profile            |
| PUT   | [/api/custom_oauth_profiles/:id](https://www.workato.com/workato-api/custom-oauth-profiles.html#update-custom-oauth-profile) | Update Custom OAuth profile            |
| DELETE| [/api/custom_oauth_profiles/:id](https://www.workato.com/workato-api/custom-oauth-profiles.html#delete-custom-oauth-profile) | Delete Custom OAuth profile            |

---

## Environment management

| Type  | Resource                                                                        | Description                           |
|-------|---------------------------------------------------------------------------------|---------------------------------------|
| POST  | [/api/secrets_management/clear_cache](https://www.workato.com/workato-api/secrets-management.html#clear-secrets-management-cache) | Clears the secrets management cache.  |
| GET   | [/api/activity_logs](https://www.workato.com/workato-api/secrets-management.html#get-audit-log) | Gets audit log records.               |

---

## Environment properties

| Type  | Resource                                                                                | Description                                      |
|-------|-----------------------------------------------------------------------------------------|--------------------------------------------------|
| GET   | [/api/properties](https://www.workato.com/workato-api/account-properties.html#list-properties-by-prefix) | Lists environment properties that match a prefix. |
| POST  | [/api/properties](https://www.workato.com/workato-api/account-properties.html#upsert-property) | Upserts environment properties.                    |

---

## Event streams

| Type  | Resource                                                                                                  | Description                           |
|-------|-----------------------------------------------------------------------------------------------------------|---------------------------------------|
| POST  | [event-streams.workato.com/api/v1/topics/:topic_id/consume](https://www.workato.com/workato-api/pubsub.html#consume-messages) | Consume messages from a topic.        |
| POST  | [event-streams.workato.com/api/v1/topics/:topic_id/publish](https://www.workato.com/workato-api/pubsub.html#publish-message) | Publish a message to a topic.         |
| POST  | [event-streams.workato.com/api/v1/batch/topics/:topic_id/publish](https://www.workato.com/workato-api/pubsub.html#publish-a-batch-of-messages) | Publish a batch of messages to a topic.|

---

## Folders

| Type  | Resource                                                                         | Description            |
|-------|----------------------------------------------------------------------------------|------------------------|
| GET   | [/api/folders](https://www.workato.com/workato-api/folders.html#list-folders)    | List folders.          |
| GET   | [/api/projects](https://www.workato.com/workato-api/folders.html#list-projects)  | List projects.         |
| POST  | [/api/folders](https://www.workato.com/workato-api/folders.html#create-folder)   | Create a folder.       |
| DELETE| [/api/folders/:folder_id](https://www.workato.com/workato-api/folders.html)      | Delete a folder.       |
| DELETE| [/api/projects/:project_id](https://www.workato.com/workato-api/folders.html)    | Delete a project.      |

---

## Jobs

| Type  | Resource                                                                                      | Description                         |
|-------|-----------------------------------------------------------------------------------------------|-------------------------------------|
| GET   | [/api/recipes/:recipe_id/jobs](https://www.workato.com/workato-api/jobs.html#list-jobs-from-a-recipe) | List jobs belonging to recipe.      |
| GET   | [/api/recipes/:recipe_id/jobs/:job_handle](https://www.workato.com/workato-api/jobs.html#get-a-job) | Returns a single job's metadata.    |
| POST  | [/api/job/resume](https://www.workato.com/workato-api/jobs.html#job-resume)                    | Resumes a particular job based on the `resume_token` you provide. This endpoint returns HTTP status code 204, indicating successful request processing without any content included in the response. This endpoint is leveraged by [SDK Wait for resume actions](https://www.workato.com/developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html). |

---

## Lookup tables

| Type  | Resource                                                                                  | Description                        |
|-------|-------------------------------------------------------------------------------------------|------------------------------------|
| GET   | [/api/lookup_tables](https://www.workato.com/workato-api/lookup-tables.html#list-lookup-tables) | List tables.                       |
| GET   | [/api/lookup_tables/:lookup_table_id/lookup](https://www.workato.com/workato-api/lookup-tables.html#lookup-row) | Look up a row                      |
| GET   | [/api/lookup_tables/:lookup_table_id/rows](https://www.workato.com/workato-api/lookup-tables.html#list-rows) | List rows.                         |
| GET   | [/api/lookup_tables/:lookup_table_id/rows/:row_id](https://www.workato.com/workato-api/lookup-tables.html#get-row) | Get a row.                         |
| POST  | [/api/lookup_tables/:lookup_table_id/rows](https://www.workato.com/workato-api/lookup-tables.html#add-row) | Add a row.                         |
| POST  | [/api/lookup_tables](https://www.workato.com/workato-api/lookup-tables.html#lut-create)    | Create a new lookup table.         |
| POST  | [/api/lookup_tables/batch_delete](https://www.workato.com/workato-api/lookup-tables.html#lut-delete) | Delete lookup tables in batch.     |
| PUT   | [/api/lookup_tables/:lookup_table_id/rows/:row_id](https://www.workato.com/workato-api/lookup-tables.html#update-row) | Update a row.                      |
| DELETE| [/api/lookup_tables/:lookup_table_id/rows/:row_id](https://www.workato.com/workato-api/lookup-tables.html#delete-row) | Delete a row.                      |

---

## Projects

| Type  | Resource                                                                                 | Description                                                                                      |
|-------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| POST  | [/api/projects/:id/build](https://www.workato.com/workato-api/projects.html#build-a-project) | Builds a project. Use the [Deploy a project build](https://www.workato.com/workato-api/projects.html#deploy-a-project-build) endpoint to deploy the project to an environment. |
| GET   | [/api/project_builds/:id](https://www.workato.com/workato-api/projects.html#get-a-project-build) | Retrieves a project build by its unique ID.                                                      |
| POST  | [/api/project_builds/:id/deploy?environment_type=:environment_type](https://www.workato.com/workato-api/projects.html#deploy-a-project-build) | Deploys a project build to an environment. Use the [Build a project](https://www.workato.com/workato-api/projects.html#build-a-project) endpoint to build the project first. |
| POST  | [/api/projects/:id/deploy?environment_type=:environment_type](https://www.workato.com/workato-api/projects.html#deploy-a-project) | Builds and deploys a project to an environment.                                                  |
| GET   | [/api/deployments/:id](https://www.workato.com/workato-api/projects.html#get-a-deployment) | Retrieves a single deployment by its unique ID.                                                  |
| GET   | [/api/deployments](https://www.workato.com/workato-api/projects.html#list-deployments)   | Retrieves a list of deployments. Query parameters may be used to filter results to a specific project, folder, date range, etc. |

---

## Project properties

| Type  | Resource                                                                                           | Description                                                   |
|-------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| GET   | [/api/properties](https://www.workato.com/workato-api/project-properties.html#list-project-properties) | List project-level properties that match a prefix and project ID. |
| POST  | [/api/properties](https://www.workato.com/workato-api/project-properties.html#upsert-project-properties) | Upsert project-level properties.                               |

---

## Recipes

| Type  | Resource                                                                                     | Description                     |
|-------|----------------------------------------------------------------------------------------------|---------------------------------|
| GET   | [/api/recipes/:id](https://www.workato.com/workato-api/recipes.html#get-recipe-details)       | Get recipe details.             |
| POST  | [/api/recipes](https://www.workato.com/workato-api/recipes.html#create-a-recipe)              | Create recipe.                  |
| POST  | [/api/recipes](https://www.workato.com/workato-api/recipes.html#copy-a-recipe)                | Copy recipe.                    |
| PUT   | [/api/recipes/:id](https://www.workato.com/workato-api/recipes.html#update-a-recipe)          | Update recipe.                  |
| GET   | [/api/recipes](https://www.workato.com/workato-api/recipes.html#list-recipes-belonging-to-user) | List recipes belonging to user. |
| PUT   | [/api/recipes/:id/start](https://www.workato.com/workato-api/recipes.html#start-recipe)       | Start recipe.                   |
| PUT   | [/api/recipes/:id/stop](https://www.workato.com/workato-api/recipes.html#stop-recipe)         | Stop recipe.                    |
| DELETE| [/api/recipes/:id](https://www.workato.com/workato-api/recipes.html#delete-recipe)            | Delete recipe.                  |
| POST  | [/api/recipes/:recipe_id/reset_trigger](https://www.workato.com/workato-api/recipes.html#reset-recipe-trigger) | Reset recipe trigger.           |
| PUT   | [/api/recipes/:recipe_id/connect](https://www.workato.com/workato-api/recipes.html#update-connection-for-recipe) | Update connection for an application in a stopped recipe.  |
| POST  | [/api/recipes/:recipe_id/poll_now](https://www.workato.com/workato-api/recipes.html#activate-polling-trigger-for-recipe) | Activate a polling trigger for a recipe. |

---

## Recipe Lifecycle Management

| Type  | Resource                                                                                  | Description                        |
|-------|-------------------------------------------------------------------------------------------|------------------------------------|
| GET   | [/api/export_manifests/folder_assets](https://www.workato.com/workato-api/recipe-lifecycle-management.html#manifest-folder-assets) | View assets in a folder.           |
| POST  | [api/export_manifests](https://www.workato.com/workato-api/recipe-lifecycle-management.html#manifest-create) | Create an export manifest.         |
| PUT   | [api/export_manifests/:id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#manifest-update) | Update an export manifest.         |
| GET   | [api/export_manifests/:id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#manifest-view) | View an export manifest.           |
| DELETE| [/api/export_manifests/:id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#manifest-delete) | Delete an export manifest.         |
| POST  | [/api/packages/export/:manifest_id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#export-package-based-on-a-manifest) | Export package based on a manifest. |
| POST  | [/api/packages/import/:folder_id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#import-package-into-a-folder) | Import a package into a folder.    |
| GET   | [/api/packages/:id](https://www.workato.com/workato-api/recipe-lifecycle-management.html#get-package-by-id) | Get a package by its ID.           |
| GET   | [/api/packages/:id/download](https://www.workato.com/workato-api/recipe-lifecycle-management.html#download-package) | Download a package.                |

---

## Roles

| Type  | Resource                                                                       | Description               |
|-------|--------------------------------------------------------------------------------|---------------------------|
| GET   | [/api/roles](https://www.workato.com/workato-api/roles.html#list-custom-roles) | List custom roles.        |
| POST  | [/api/roles/:role_id/copy](https://www.workato.com/workato-api/roles.html#copy-a-custom-role) | Makes a copy of a custom role. |

---

## Test Automation

| Type  | Resource                                                                                      | Description                            |
|-------|-----------------------------------------------------------------------------------------------|----------------------------------------|
| POST  | [/api/test_cases/run_requests](https://www.workato.com/workato-api/test-automation.html#request-run) | Run test cases.                        |
| GET   | [/api/test_cases/run_requests/{id}](https://www.workato.com/workato-api/test-automation.html#run-result-get) | Get the current state of a test case run request. |
| GET   | [/api/recipes/{recipe_id}/test_cases](https://www.workato.com/workato-api/test-automation.html#test-cases-get) | Get test cases.                        |

---

## Workspace collaborators

| Type  | Resource                                                                                    | Description                                |
|-------|---------------------------------------------------------------------------------------------|--------------------------------------------|
| POST  | [/api/member_invitations](https://www.workato.com/workato-api/team.html#invite-collaborator) | Invite a collaborator to your workspace.   |
| GET   | [/api/members](https://www.workato.com/workato-api/team.html#all-users-get)                  | Get a list of members in your workspace.   |
| GET   | [/api/members/:id](https://www.workato.com/workato-api/team.html#user-details-get)           | Get details about a user you specify.      |
| PUT   | [/api/members/:id](https://www.workato.com/workato-api/team.html#update-collaborator-roles)  | Update a collaborator's roles.             |
| GET   | [/api/members/:id/privileges](https://www.workato.com/workato-api/team.html#user-privileges-get) | Get the role and privileges for a workspace user you specify. |

---

## Workspace details

| Type  | Resource                                                                | Description                   |
|-------|-------------------------------------------------------------------------|-------------------------------|
| GET   | [/api/users/me](https://www.workato.com/workato-api/users.html#auth-user-details-get) | Get details about your workspace. |
