The Roles APIs allow users to programmatically manage custom roles for their teams.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/roles | List custom roles. |
| PUT | /api/roles/:role\_id | Updates a custom role's project privilege |
| POST | /api/roles/:role\_id/copy | Makes a copy of a custom role. |

## # List custom roles

Lists all custom roles.

### # Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| per\_page | **integer**  
_optional_ | The number of custom roles to retrieve. |
| page | **integer**  
_optional_ | The page number. If the total number of custom roles exceed the page limit, subsequent records can be retrieved by calling the next page. |

#### # Sample request

### # Response

## # Update a custom role

Updates the projects accessible to a custom collaborator role. You can set the privilege to all projects or specific projects by their folder IDs. The folder IDs can be obtained with the GET folders API endpoint.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| all\_folders | **string**  
_required_ | Either "true" or "false". Must be "false" if "folder\_ids" is specified. |
| folder\_ids | **array**  
 | Array of project IDs. |

#### # Sample request

### # Response

## # Copy a custom role

Creates a copy of a custom collaborator role with the ability to change the folders accessible by the role. The folder IDs can be obtained with the GET folders API endpoint.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the custom role. |
| folder\_ids | **array**  
 | Array of project IDs. |

#### # Sample request

### # Response