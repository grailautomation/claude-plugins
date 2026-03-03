WHO CAN USE THESE APIS?

Accounts with the Environments feature enabled can use the APIs in this guide. Requests sent from accounts without this feature will receive a `400 - Environments not provisioned` response.

In Workato, projects are used to organize automation assets and control access. A project holds a set of related assets for your automations, including connections, recipes, and subfolders.

The Project APIs enable you to programmatically manage and deploy projects to the environments provisioned in your workspace.

___

## # Understanding project deployment

In Workato, there are two ways to deploy projects:

-   **Build and then deploy**. This approach can be used if you want to commit the package to an external version control system. Steps for accomplishing this would be similar to the following:
    
    1
    
    Build the project: `POST /api/projects/:id/build`
    
    2
    
    Verify the project built successfully: `GET /api/project_builds/:id`
    
    3
    
    If committing to a version control system like GitHub, use the `download_url` from Step 2's response to download the package.
    
    4
    
    Commit the package to your version control system.
    
    5
    
    Deploy the project build to an environment: `POST /api/project_builds/:id/deploy?environment_type=:environment_type`
    
    6
    
    Verify the project deployed successfully: `GET /api/deployments/:id`
    
-   **Build and deploy in one step**. If you don't need to commit the project to a version control system, you can use this approach:
    
    1
    
    Build and deploy the project to an environment: `POST /api/projects/:id/deploy?environment_type=:environment_type`
    
    2
    
    Verify the project deployed successfully: `GET /api/deployments/:id`
    

___

## # Quick reference

| Endpoint | Description |
| --- | --- |
| POST /projects/:id/build | Builds a project. Use the Deploy a project build endpoint to deploy the project to an environment. |
| GET /project\_builds/:id | Retrieves a project build by its unique ID. |
| POST /project\_builds/:id/deploy?environment\_type=:environment\_type | Deploys a project build to an environment. Use the Build a project endpoint to build the project first. |
| POST /projects/:id/deploy?environment\_type=:environment\_type | Builds and deploys a project to an environment. |
| GET /deployments/:id | Retrieves a single deployment by its unique ID. |
| GET /deployments | Retrieves a list of deployments. Query parameters may be used to filter results to a specific project, folder, date range, etc. |

___

## # Build a project

Builds a project. Use the Deploy a project build endpoint to deploy the project to an environment.

### # Request

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer**  
_required_ | A project ID. This parameter accepts the following:
-   A valid `project_id`
-   A valid `folder_id`, formatted as `f{:folder_id}`. For example: `f660222`. Use the List folders endpoint to retrieve these IDs.

 |

#### # Request body arguments

| Name | Type | Description |
| --- | --- | --- |
| **description** | **string**  
_optional_ | A brief description of the build. |
| **include\_test\_cases** | **boolean**  
_optional_ | Instructs the build to include test cases or not. |

#### # Request examples

#### # Using a project ID

#### # Using a folder ID

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a single project build object.

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The build ID. |
| **created\_at** | **timestamp** | The time the build was created. |
| **updated\_at** | **timestamp** | The time the build was last updated. |
| **description** | **string** | The build description. This is `null` if not provided in the request. |
| **include\_test\_cases** | **boolean** | Whether the build includes test cases or not. This is `null` if not provided in the request. |
| **project\_build\_id** | **integer** | The ID of the project build associated with the build. |
| **project\_id** | **string** | The ID of the project that was built. |
| **state** | **string** | The current state of the build. |
| **performed\_by\_name** | **string** | The name of the user who built the project. |
| **download\_url** | **string** | A URL from which the project build can be downloaded. |

400 BAD REQUEST - MISSING REQUIRED PARAMETERS

The API may return a `400 BAD REQUEST` status and the following errors if the request is malformed:

**Missing environment\_type parameter:**

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid `id`

-   Invalid `environment_type`404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___

## # Get a project build

Retrieves a project build by its unique ID.

### # Request

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer**  
_required_ | The ID of the project build to retrieve. |

#### # Request examples

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a single project build object.

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The build ID. |
| **created\_at** | **timestamp** | The time the build was created. |
| **updated\_at** | **timestamp** | The time the build was last updated. |
| **description** | **string** | The build description. This will be `null` if not provided in the request that created the build. |
| **project\_id** | **string** | The ID of the project that was built. |
| **state** | **string** | The current state of the build. |
| **performed\_by\_name** | **string** | The name of the user who built the project. |
| **download\_url** | **string** | A URL from which the project build can be downloaded. |

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid project build `id`

404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___

## # Deploy a project build

Deploys a project build to an environment. Use the Build a project endpoint to build the project first.

### # Request

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer**  
_required_ | The ID of the build to be deployed. |

#### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| **environment\_type** | **string**  
_required_ | The environment the build will be deployed to. Accepted values:
-   `test`
-   `prod`

 |

#### # Request body arguments

| Name | Type | Description |
| --- | --- | --- |
| **description** | **string**  
_optional_ | A brief description of the build. |

#### # Request example

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a single deployment object.

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The deployment ID. |
| **created\_at** | **timestamp** | The time the deployment was created. |
| **updated\_at** | **timestamp** | The time the deployment was last updated. |
| **description** | **string** | The deployment description. This will be `null` if not provided in the request. |
| **project\_build\_id** | **integer** | The ID of the project build associated with the deployment. |
| **environment\_type** | **string** | The environment the build was deployed to. |
| **project\_id** | **string** | The ID of the project associated with the deployed build. |
| **state** | **string** | The current state of the deployment. |
| **performed\_by\_name** | **string** | The name of the user who deployed the build. |

400 BAD REQUEST - MISSING REQUIRED PARAMETERS

The API may return a `400 BAD REQUEST` status and the following errors if the request is malformed:

**Missing environment\_type parameter:**

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid `id`

-   Invalid `environment_type`404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___

## # Deploy a project

Builds and deploys a project to an environment.

### # Request

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer**  
_required_ | A project ID. This parameter accepts the following:
-   A valid `project_id`
-   A valid `folder_id`, formatted as `f{:folder_id}`. For example: `f660222`. Use the List folders endpoint to retrieve these IDs.

 |

#### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| **environment\_type** | **string**  
_required_ | The environment the project will be deployed to. Accepted values:
-   `test`
-   `prod`

 |

#### # Request body arguments

| Name | Type | Description |
| --- | --- | --- |
| **description** | **string**  
_optional_ | A brief description of the deployment. |

#### # Request examples

##### # Using a project ID

##### # Using a folder ID

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a single deployment object.

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The deployment ID. |
| **created\_at** | **timestamp** | The time the deployment was created. |
| **updated\_at** | **timestamp** | The time the deployment was last updated. |
| **description** | **string** | The deployment description. This will be `null` if not provided in the request. |
| **project\_build\_id** | **integer** | The ID of the project build associated with the deployment. |
| **environment\_type** | **string** | The environment the project was deployed to. |
| **project\_id** | **string** | The ID of the project that was deployed. |
| **state** | **string** | The current state of the deployment. |
| **performed\_by\_name** | **string** | The name of the user who deployed the project. |

400 BAD REQUEST - MISSING REQUIRED PARAMETERS

The API may return a `400 BAD REQUEST` status and the following errors if the request is malformed:

**Missing environment\_type parameter:**

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid `id`

-   Invalid `environment_type`404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___

## # Get a deployment

Retrieves a single deployment by its unique ID.

### # Request

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer**  
_required_ | The ID of the deployment to be retrieved. |

#### # Request example

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a single deployment object.

| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The deployment ID. |
| **created\_at** | **timestamp** | The time the deployment was created. |
| **updated\_at** | **timestamp** | The time the deployment was last updated. |
| **description** | **string** | The deployment description. This will be `null` if not provided in the request that created the deployment. |
| **project\_build\_id** | **integer** | The ID of the project build associated with the deployment. |
| **environment\_type** | **string** | The environment associated with the deployment. |
| **project\_id** | **string** | The ID of the project associated with the deployment. |
| **state** | **string** | The current state of the deployment. |
| **performed\_by\_name** | **string** | The name of the user who performed the deployment. |

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid `deployment_id`

404 NOT FOUND - INVALID PARAMETERS

The API may return a `404 NOT FOUND` status and a `Not found` error for the following reasons:

-   Invalid `id`

-   Invalid `environment_type`404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___

## # List deployments

Retrieves a list of deployments. Query parameters may be used to filter results to a specific project, folder, date range, etc.

### # Request

#### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| **project\_id** | **string**  
_optional_ | A project ID. If provided, only deployments associated with the project will be included in the response. |
| **folder\_id** | **string**  
_optional_ | A folder ID, formatted as `f{:folder_id}`. For example: `f660222`. If provided, only deployments associated with the folder will be included in the response.
Use the List folders endpoint to retrieve these IDs.

 |
| **environment\_type** | **string**  
_optional_ | An environment type. If provided, only deployments associated with the environment will be included in the response. Must be one of:

-   `test`
-   `prod`

 |
| **state** | **string**  
_optional_ | The state of the deployments to retrieve. If provided, only deployments with the provided state will be included in the response. Must be one of:

-   `pending`
-   `success`
-   `failed`

 |
| **from** | **timestamp**  
_optional_ | Deployments created after this time will be included in the response. The value must be an ISO 8601 timestamp. |
| **to** | **timestamp**  
_optional_ | Deployments created after this time will be included in the response. The value must be an ISO 8601 timestamp. |

#### # Request examples

##### # Without query parameters

##### # With a folder ID

### # Responses

200 OK

If successful, the API will return a `200 OK` status and a list of deployment objects.

| Name | Type | Description |
| --- | --- | --- |
| **items** | **array** | A list of deployment objects.
| Name | Type | Description |
| --- | --- | --- |
| **id** | **integer** | The deployment ID. |
| **created\_at** | **timestamp** | The time the deployment was created. |
| **updated\_at** | **timestamp** | The time the deployment was last updated. |
| **description** | **string** | The deployment description. This will be `null` if not provided in the request that created the deployment. |
| **project\_build\_id** | **integer** | The ID of the project build associated with the deployment. |
| **environment\_type** | **string** | The environment associated with the deployment. |
| **project\_id** | **string** | The ID of the project associated with the deployment. |
| **state** | **string** | The current state of the deployment. |
| **performed\_by\_name** | **string** | The name of the user who performed the deployment. |

 |

404 NOT FOUND - INVALID URI

The API may return a `404 NOT FOUND` status and an `API not found` error for the following reasons:

-   Unsupported method

-   Incorrect URI

___