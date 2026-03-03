Use the following endpoints to manage folders and projects (top level folders) in your workspace.

ENDPOINT ACCESS

To access these endpoints, your API client must have the appropriate privileges. This is determined by the API client role.

To enable endpoint access:

You can enable access to these endpoints by editing an existing API client role, or by creating a new API client role:

1

Navigate to **Workspace admin > API clients > Client roles**.

Select the role you plan to edit.

Alternatively, click **\+ Add client role** to create a new API client role.

2

Select **Projects** and navigate to **Project assets > Projects & folders**.

3

Select the checkbox(es) next to the endpoint(s) you plan to enable for this role. The following options are available:

-   **Projects & folders**
    -   Select this option to enable all endpoints for this role.
-   **List folders** `GET /api/folders`
-   **List projects** `GET /api/projects`
-   **Create folder** `POST /api/folders`
-   **Delete folder** `DELETE /api/folders/:id`
-   **Delete project** `DELETE /api/projects/:id`

_Select the endpoints you plan to enable_

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/folders | List folders. |
| GET | /api/projects | List projects. |
| POST | /api/folders | Create a folder. |
| DELETE | /api/folders/:folder\_id | Delete a folder. |

## # List folders

Lists all folders.

### # URL Parameters

| Name | Type | Description |
| --- | --- | --- |
| parent\_id | **string** | Parent folder ID. Defaults to Home folder. |
| page | **integer** | Page number. Defaults to 1. |
| per\_page | **integer** | Page size. Defaults to 100 (maximum is 100). |

#### # Sample request

### # Response

## # List projects

Lists all projects. Projects are top level folders that normally encompass a single use case.

### # URL Parameters

| Name | Type | Description |
| --- | --- | --- |
| page | **integer** | Page number. Defaults to 1. |
| per\_page | **integer** | Page size. Defaults to 100 (maximum is 100). |

#### # Sample request

### # Response

## # Create a folder

Creates a new folder in the specified parent folder. If no parent folder ID is specified, the folder created will be a top level folder (in the Home folder).

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the folder. |
| parent\_id | **string** | Parent folder ID. Defaults to Home folder. |

#### # Sample request

### # Response

## # Delete a folder

Delete a folder within your workspace.

WARNING

This action deletes a folder and all of its contents (recipes and connections).

To use this endpoint, your API client role must have the following privilege:

-   **Delete folder** `DELETE /api/folders/:id`

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| folder\_id | **string**  
_required_ | The ID of the folder you plan to delete. You can retrieve a list of folder IDs by calling the list folders endpoint. |

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| force | **boolean**  
_optional_ | Set this parameter to `true` to delete a folder that is not empty. When `true`, the folder you specify using the `folder_id` parameter, and its contents (all recipes and connections) within the folder are deleted. If set to `false`, this action can only delete an empty folder. |

#### # Sample request

### # Response

-   Successful response
-   Unsuccessful response

#### # Successful response

#### # Unsuccessful response

If you attempt to delete a folder that isn't empty, but do not set the `force` parameter to `true` Workato cannot delete the folder you've specified.

If the folder contains a connection, Workato provides the following response:

If the folder contains a recipe, Workato provides the following response:

## # Delete a project

Delete a project within your workspace. Projects are top-level folders that typically encompass a single use case.

WARNING

This action deletes a project and all of its contents. This includes all child folders, recipes, connections, and Workflow apps assets (if applicable) inside the project.

To use this endpoint, your API client role must have the following privilege:

-   **Delete projects** `DELETE /api/projects/:id`

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| project\_id | **string**  
_required_ | The ID of the project you plan to delete. Retrieve a list of all projects in your workspace by calling the list projects endpoint. |

#### # Sample request

### # Response

-   Successful response
-   Unsuccessful response

#### # Successful response

#### # Unsuccessful response

If you attempt to delete a project and do not have the appropriate privileges, Workato returns the following response.