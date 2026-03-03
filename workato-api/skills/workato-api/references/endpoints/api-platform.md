The API Platform APIs allow users to programmatically create and manage API Platform assets like endpoints, collections, clients, and access profiles.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/api\_collections | List **API collections**. The endpoint returns the `project_id` of the project to which the collections belong in the response. |
| POST | /api/api\_collections | Create an **API collection** within a project you specify. |
| GET | /api/api\_endpoints | List **API endpoints** in a collection. |
| PUT | /api/api\_endpoints/:api\_endpoint\_id/enable | Enable an **API endpoint** in a collection. |
| PUT | /api/api\_endpoints/:api\_endpoint\_id/disable | Disable an **API endpoint** in a collection. |
| GET | /api/api\_clients | List all **API clients**. Workato includes the `project_id` of the project to which the API client belongs in the response. |
| POST | /api/api\_clients | Create a new **API client** within a project you specify. |
| GET | /api\_access\_profiles | List **access profiles** belonging to an API client. |
| POST | /api\_access\_profiles | Create an **access profile** belonging to an API client. |
| PUT | /api\_access\_profiles/:api\_access\_profile\_id | Update an **access profile** belonging to an API client. |
| PUT | /api/api\_access\_profiles/:api\_access\_profile\_id/enable | Enable an **access profile** belonging to an API client. |
| PUT | /api/api\_access\_profiles/:api\_access\_profile\_id/disable | Disable an **access profile** belonging to an API client. |
| PUT | /api\_access\_profiles/:access\_profile\_id/refresh\_secret | Refreshes access profile **token or secret**. |

## # List API collections

List all API collections. The endpoint returns the `project_id` of the project to which the collections belong in the response.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| per\_page | **integer** | Number of API collections to return in a single page. Defaults to `100`. Max is `100`. |
| page | **integer** | Page number of the API collections to fetch. Defaults to `1`. |

### # Response

## # Create an API collection

Create an API collection within a project you specify.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| project\_id | **string**  
_required_ | The ID of a specific project. Retrieve a list of project IDs using the list projects endpoint. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the collection |

#### # Sample request

### # Response

## # List API endpoints

Lists all API endpoints. Specify the `api_collection_id` to obtain the list of endpoints in a specific collection.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_collection\_id | **string** | ID of the API collection. If the parameter is not provided, all API endpoints are returned. |
| per\_page | **integer** | Number of API endpoints to return in a single page. Defaults to `100`. Max is `100`. |
| page | **integer** | Page number of the API endpoints to fetch. Defaults to `1`. |

#### # Sample request

### # Response

## # Enable an API endpoint

Enables an API endpoint. The underlying recipe must be started to enable the API endpoint successfully.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_endpoint\_id | **string**  
 | ID of the API endpoint. |

#### # Sample request

## # Disable an API endpoint

Disables an active API endpoint. The endpoint can no longer be called by a client.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_endpoint\_id | **string**  
 | ID of the API endpoint. |

#### # Sample request

## # List API clients

List all API clients. This endpoint includes the `project_id` to which the API client belongs in the response.

### # Response

## # Create an API client

Create a new API client within a project you specify.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| project\_id | **string**  
_required_ | The ID of a specific project. Retrieve a list of project IDs by using the list projects endpoint. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the client. |

#### # Sample request

### # Response

## # List access profiles

List all access profiles belonging to an API client. If you don't provide an API client ID, the resource lists all access profiles for all API clients.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_client\_id | **string** | Provide an API client ID to retrieve access profiles belonging to a specific API client. |
| per\_page | **integer** | Number of access profiles returned in a single page. Defaults to `100`. Max is `100`. |
| page | **integer** | Choose the page of access profiles to return. The starting page is `1`. Defaults to `1`. |

#### # Sample request

### # Response

## # Create an access profile

Create an access profile belonging to an API client. To use this endpoint, the account must contain at least 1 API collection to assign to the access profile.

The response returned depends on the auth type chosen (Auth token, JSON web token or OAuth 2.0).

-   Auth token authorization will return the auth token in the `secret` response
-   JWT token has 2 signing methods: HMAC and RSA. Depending on the chosen method, the respective secret or public is required in the payload
-   OAuth 2.0 authorization will return the client ID and secret in `oauth_client_id` and `oauth_client secret`

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_client\_id | **string**  
 | ID of the API client. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the access profile |
| api\_collection\_ids | **array**  
_required_ | IDs of collections to add to the access profile |
| active | **boolean**  
_required_ | Whether the access profile is disabled or enabled. A client with a disabled access profile cannot call any APIs. |
| auth\_type | **string**  
_required_ | Authentication method to validate requests. Available types are: `token`, `jwt`, `oauth2` and `oidc`. |
| jwt\_method | **string** | The JWT signing method. If the _auth\_type_ is `jwt`, this is required. Available methods are `hmac` and `rsa` for HMAC and RSA respectively. |
| ip\_allow\_list | **array** | List of IP addresses to be allowlisted |
| jwt\_secret | **string** | Based on the method, specify the HMAC shared secret or the RSA public key. |
| oidc\_issuer | Discovery URL of identity provider or OIDC service. Provide only one of this or _oidc\_jwks\_uri_, not both.  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| oidc\_jwks\_uri | JWKS URL of identity provider or OIDC service. Provide only one of this or _oidc\_issuer_, not both.  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| access\_profile\_claim | If you wish to use a custom claim to identify this access profile, provide the JWT claim key here. Learn more  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| required\_claims | Provide a list of claims that you wish to enforce.Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| allowed\_issuers | Provide a list of issuers (`iss` value in JWT claims) that you wish to allow. Leave If `iss` claim is enforced in _required\_claims_, leave this blank to require any `iss` value. Only application if _auth\_type_ is `jwt` or `oidc`. |  |

#### # Sample request (Auth token)

#### # Sample request (JWT RSA)

### # Response (Auth token)

## # Update an access profile

Update an access profile belonging to an API client.

The response returned depends on the auth type chosen (Auth token, JSON web token or OAuth 2.0).

-   Auth token authorization will return the auth token in the `secret` response
-   JWT token has 2 signing methods: HMAC and RSA. Depending on the chosen method, the respective secret or public is required in the payload
-   OAuth 2.0 authorization will return the client ID and secret in `oauth_client_id` and `oauth_client secret`

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_access\_profile\_id | **string**  
_required_ | API access profile ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Existing/Updated name of the access profile |
| api\_collection\_ids | **array**  
_required_ | Existing/updated API collection IDs to be configured for the access profile |
| active | **boolean**  
_required_ | Whether the access profile is disabled or enabled. A client with a disabled access profile cannot call any APIs. |
| auth\_type | **string**  
_required_ | Authentication method to validate requests. Available types are: `token`, `jwt`, `oauth2` and `oidc`. |
| ip\_allow\_list | **array** | List of IP addresses to be allowlisted |
| jwt\_method | **string** | The JWT signing method. If the _auth\_type_ is `jwt`, this is required. Available methods are `hmac` and `rsa` for HMAC and RSA respectively. |
| jwt\_secret | **string** | Based on the method, specify the HMAC shared secret or the RSA public key. |
| oidc\_issuer | Discovery URL of identity provider or OIDC service. Provide only one of this or _oidc\_jwks\_uri_, not both.  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| oidc\_jwks\_uri | JWKS URL of identity provider or OIDC service. Provide only one of this or _oidc\_issuer_, not both.  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| access\_profile\_claim | If you wish to use a custom claim to identify this access profile, provide the JWT claim key here. Learn more  
Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| required\_claims | Provide a list of claims that you wish to enforce.Only application if _auth\_type_ is `jwt` or `oidc`. |  |
| allowed\_issuers | Provide a list of issuers (`iss` value in JWT claims) that you wish to allow. Leave If `iss` claim is enforced in _required\_claims_, leave this blank to require any `iss` value. Only application if _auth\_type_ is `jwt` or `oidc`. |  |

#### # Sample request (Auth token)

## # Enable an access profile

Enable an access profile belonging to an API client. Enabling an access profile will allow API calls to be accepted with the enabled profile.

This call returns `success` or error messages for Unauthorized/Bad requests.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_access\_profile\_id | **string**  
_required_ | ID of the access profile. |

#### # Sample request (Auth token)

## # Disable an access profile

Disable an access profile belonging to an API client. Disabling an access profile will stop allowing API calls to be accepted with the access profile.

This call returns `success` or error messages for Unauthorized/Bad requests.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| api\_access\_profile\_id | **string**  
_required_ | ID of the access profile. |

#### # Sample request (Auth token)

## # Refresh token/secret

Refreshes the auth token or OAuth 2.0 client secret. This endpoint will fail if the authorization type on the access profile is `JWT`.

The response returned depends on the authorization type of the access profile (Auth token or OAuth 2.0).

-   Auth token authorization will return a new auth token in the `secret` response
-   OAuth 2.0 authorization will return a new client ID and secret in `oauth_client_id` and `oauth_client secret`

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| access\_profile\_id | **string**  
_required_ | API access profile ID |

### # Response (Auth token)