Use the endpoints below to manage custom OAuth profiles programmatically.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/custom\_oauth\_profiles | List Custom OAuth profiles. |
| GET | /api/custom\_oauth\_profiles/:id | Get a Custom OAuth profile by ID. |
| POST | /api/custom\_oauth\_profiles | Create a Custom OAuth profile. |
| PUT | /api/custom\_oauth\_profiles/:id | Update a Custom OAuth profile. |
| DELETE | /api/custom\_oauth\_profiles/:id | Delete a Custom OAuth profile. |

## # List Custom OAuth profiles

List custom OAuth profiles. Client secrets and tokens are never returned in the response.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| page | **integer** | Page number. Defaults to 1. |
| per\_page | **integer** | Page size. Defaults to 100 (maximum is 100). |

### # Sample request

### # Response

## # Get Custom OAuth profile by ID

Retrieves a custom OAuth profile by ID. Client secrets and tokens are never returned in the response.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the Custom OAuth profile to retrieve |

### # Sample request

### # Response

## # Create a Custom OAuth profile

Create a Custom OAuth profile.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | The name of the OAuth profile. |
| provider | **string**  
_required_ | The name of the app tied to this Custom OAuth profile. |
| data.client\_id | **string**  
_required_ | The Client ID of the Custom OAuth App |
| data.client\_secret | **string**  
_required_ | The Client secret of the Custom OAuth App |
| data.token | **string**  
_optional_ | Only required for Slack Apps. The token of the Custom OAuth App |

#### # Sample request

### # Response

## # Update a Custom OAuth profile

Update a Custom OAuth profile.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | ID of the Custom OAuth profile to update |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | The name of the OAuth profile. |
| provider | **string**  
_required_ | The name of the app tied to this Custom OAuth profile. |
| data.client\_id | **string**  
_required_ | The Client ID of the Custom OAuth App |
| data.client\_secret | **string**  
_required_ | The Client secret of the Custom OAuth App |
| data.token | **string**  
_optional_ | Only required for Slack Apps. The token of the Custom OAuth App |

#### # Sample request

### # Response

## # Delete a Custom OAuth profile

Delete a Custom OAuth profile.

### # Path Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer** | ID of the Custom OAuth profile to delete |

#### # Sample request

### # Response