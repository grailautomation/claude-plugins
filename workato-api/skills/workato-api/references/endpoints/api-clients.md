The following endpoints allow you to manage your API clients via developer APIs. This allows you to programmatically create new API clients when onboarding new teams or rotate API tokens regularly for all your API clients.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/developer\_api\_clients | List **Developer API Clients**. |
| POST | /api/developer\_api\_clients | Create **Developer API Client**. |
| GET | /api/developer\_api\_clients/:id | Get **Developer API Client by ID**. |
| PUT | /api/developer\_api\_clients/:id | Update **Developer API Clients**. |
| DELETE | /api/developer\_api\_clients/:id | Delete **Developer API Client**. |
| POST | /api/developer\_api\_clients/:id/regenerate | Regenerate **Developer API Client token**. |
| GET | /api/developer\_api\_client\_roles | List **Developer API Client roles**. |

## # List Developer API clients

List all Developer API clients.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| per\_page | **integer** | Number of API clients to return in a single page. Defaults to `100`. Max is `100`. |
| page | **integer** | Page number of the API clients to fetch. Defaults to `1`. |

#### # Sample Request

### # Response

___

## # Create a Developer API client

Create a Developer API client.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **String** | Name of the API client |
| api\_privilege\_group\_id | **integer** | API client role ID |
| all\_folders | **boolean**  
_required_ | Flag indicating whether API client has access to all folders |
| folder\_ids | **array** | Array of folder IDs. Required if `all_folders` is false. |
| environment\_name | **string** | Name of the environment. Required if your workspace has environments enabled. |

#### # Sample Request

### # Response

___

## # Get a Developer API client by ID

Get a Developer API client by ID.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the API Client. |

#### # Sample Request

### # Response

___

## # Update a Developer API client

Update a Developer API client.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the API Client. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **String** | Name of the API client |
| api\_privilege\_group\_id | **integer** | API client role ID |
| all\_folders | **boolean**  
_required_ | Flag indicating whether API client has access to all folders |
| folder\_ids | **array** | Array of folder IDs. Required if `all_folders` is false. |
| environment\_name | **string** | Name of the environment. Required if your workspace has environments enabled. |

#### # Sample Request

### # Response

___

## # Delete a Developer API client

Delete a Developer API client.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the API Client. |

#### # Sample Request

### # Response

___

## # Regenerate a Developer API Client token

Regenerates the API token for an API client. This invalidates the previous API token.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the API Client. |

#### # Sample Request

### # Response

___

## # List Developer API client roles

List all Developer API Client roles.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| per\_page | **integer** | Number of API clients to return in a single page. Defaults to `100`. Max is `100`. |
| page | **integer** | Page number of the API clients to fetch. Defaults to `1`. |

#### # Sample Request

### # Response