Use the following endpoints to manage project properties programmatically.

## # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/properties | List project-level properties that match a prefix and project ID. |
| POST | /api/properties | Upsert project-level properties. |

## # List project properties

Returns a list of project-level properties belonging to a specific project in a customer workspace that matches a `project_id` you specify. You must also include a prefix. For example, if you provide the prefix `salesforce_sync.`, any project property with a name beginning with `salesforce_sync.`, such as `salesforce_sync.admin_email`, with the `project_id` you provided is returned.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| prefix | **string**  
_required_ | Returns properties that contain the prefix you provided. For example, if the prefix is `salesforce_sync.` the property `salesforce_sync.admin_email` is returned. |
| project\_id | **string**  
_required_ | Returns project-level properties that match the `project_id` you specify. If this parameter is not present, this call returns environment properties. |

#### # Sample request

### # Response

## # Upsert project properties

Upserts project properties belonging to a specific project in a customer workspace that matches a `project_id` you specify. This endpoint maps to properties based on the names you provide in the request.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| project\_id | **string**  
_required_ | Provide the project ID that contains the project properties you plan to upsert. If this parameter is not present, this call upserts environment properties. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| properties | **Hash**  
_required_ | Contains the names and values of the properties you plan to upsert. |

#### # Sample request

### # Response