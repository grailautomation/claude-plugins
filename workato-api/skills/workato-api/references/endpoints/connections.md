Use the following endpoints to manage connections.

## # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/connections | Returns all connections and associated data. |
| POST | /api/connections | Create a connection. |
| PUT | /api/connections/:connection\_id | Updates a connection. |
| POST | /api/connections/:connection\_id/disconnect | Disconnects a connection. |
| DELETE | /api/connections/:connection\_id | Deletes a connection. |

## # List connections

Returns all connections and associated data for the authenticated Workato user.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| folder\_id | **string**  
_optional_ | Folder ID of the connection. |
| parent\_id | **string**  
_optional_ | Parent ID of the connection. Connection must be of the same provider. |
| external\_id | **string**  
_optional_ | External identifier usually given to the user who owns the connection. |
| include\_runtime\_connections | **string**  
_optional_ | When `"true"` is supplied, all runtime user connections are also returned. |

#### # Sample request

### # Response

## # Create a connection

Create a new connection. This endpoint supports the following actions:

-   Create a shell connection
-   Create and authenticate a connection

Feature compatibility: OAuth type connections

This endpoint does not support creating and authenticating a connection for OAuth type connections. However, you can use this endpoint to create a shell connection for your OAuth connections.

### # Payload

Include the following properties in the request body to filter results:

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_optional_ | Name of the connection. For example: `Prod JIRA connection` |
| provider | **string**  
_optional_ | The application type of the connection. For example: `jira` |
| parent\_id | **string**  
_optional_ | The ID of the parent connection. The parent connection must be the same `provider` type. Learn more. |
| folder\_id | **string**  
_optional_ | The ID of the project or folder containing the connection. |
| external\_id | **string**  
_optional_ | The external ID assigned to the connection, usually given to the user who owns the connection. |
| input | **Object**  
_optional_ | Connection parameters.
For a list of providers and connection parameters, refer to the Platform API connection parameter reference.

 |

### # Sample requests

-   Shell connection
-   Connection with credentials

#### # Shell connection request

This creates a connection in a `Disconnected` state.

#### # Connection with credentials

This creates and authenticates a connection.

### # Response

## # Update a connection

Updates a connection in a non-embedded workspace.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| connection\_id | **string**  
_required_ | The ID of the connection. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_optional_ | Name of the connection. For example: `Prod Salesforce connection` |
| parent\_id | **string**  
_optional_ | The ID of the parent connection. Learn more. |
| folder\_id | **string**  
_optional_ | The ID of the project or folder containing the connection. |
| external\_id | **string**  
_optional_ | An external ID assigned to the connection. This value could reference a record in one of your other applications. |
| input | **object**  
_optional_ | Connection parameters.
For a list of providers and connection parameters, refer to the Platform API connection parameter reference.

 |

### # Sample requests

-   Update a Jira connection
-   Update an Outreach connection

#### # Update a Jira connection

### # Response

#### # Update an Outreach connection

## # Disconnect a connection

Disconnects an active connection in a non-embedded workspace. If the connection is already disconnected, no action is taken.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| connection\_id | **string**  
_required_ | The ID of the connection. |
| force | **boolean**  
_optional_ | Value must be `true` to forcefully disconnect an active connection used by active recipes. Defaults to `false`. |

### # Payload

No payload is expected.

### # Sample request

### # Response

-   Successfully disconnected an active connection or connection already disconnected.

-   Provided connection ID does not exist

___

## # Delete a connection

Deletes a disconnected connection in a non-embedded workspace. If the connection is active or used by active recipes, this API request fails.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| connection\_id | **string**  
_required_ | The ID of the connection. |

### # Sample request

### # Response

-   Successfully deleted a disconnected connection.

-   Provided connection is active

-   Provided connection is used in active recipes

-   Provided connection ID does not exist