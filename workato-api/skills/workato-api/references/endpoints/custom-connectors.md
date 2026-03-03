## # Connector SDK

The following endpoints allow you to create and manage custom connectors, as well as generate a Workato Schema from sample JSON and CSV documents. These endpoints are also used in the SDK CLI tool for schema generation commands.

## # Quick reference

The Custom connectors resource contains the following endpoints:

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/custom\_connectors/search | Search for custom connectors. |
| GET | /api/custom\_connectors/:id/code | Fetches code for a custom connector. |
| POST | /api/sdk/generate\_schema/json | Generates Workato schema from a stringified JSON sample. |
| POST | /api/sdk/generate\_schema/csv | Generates Workato schema from a stringified CSV sample. |
| POST | /api/custom\_connectors | Creates a custom connector. |
| POST | /api/custom\_connectors/:id/release | Releases the latest version of a custom connector. |
| POST | /api/custom\_connectors/:id/share | Shares a custom connector. |
| PUT | /api/custom\_connectors/:id | Updates a custom connector. |

## # Generate schema from JSON

Generates Workato schema from a stringified JSON sample.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| sample | **string**  
_optional_ | Stringified JSON of the sample document to parse. |

#### # Sample Request

### # Response

## # Generate schema from CSV

Generates Workato schema from a stringified CSV sample.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| sample | **string**  
_optional_ | Stringified CSV of the sample document to parse. |
| col\_sep | **string**  
_optional_ | Column delimiter for the CSV sample. Must be one of `comma`, `semicolon`, `space`, `tab`, `colon`, `pipe`. |

#### # Sample Request

### # Response

## # Custom connector developer APIs

Refer to the following sections for available custom connector operations. The following limits apply to custom connector developer APIs:

-   Custom connector code supports a maximum of 10MB of data
-   Custom connector API endpoints have a rate limit of 1 per second
-   Custom connector code must be UTF-8 and JSON compatible

### # Search custom connector

The Search operation allows you to search for a custom connector in your workspace by title.

LIMITED TO TEN MOST RECENT RELEASES

Only the ten most recently released versions are returned.

#### # Payload

| Name | Type | Description |
| --- | --- | --- |
| title | String _required_ | The case-sensitive title of the custom connector for which you plan to search. The search returns partial matches. |

#### # Sample request

#### # Sample response

### # Get custom connector code

The Get custom connector code operation allows you to fetch a custom connector's code.

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| ID | Integer _required_ | The ID of the custom connector for which you plan to fetch the code. You can find your custom connector ID in the search custom connector endpoint. |

#### # Sample request

#### # Sample response

### # Create custom connector

The Create operation allows you to create a custom connector in your workspace.

#### # Payload

| Name | Type | Description |
| --- | --- | --- |
| title | String | The title of the custom connector you plan to create. |
| logo | String | The logo you plan to add to your custom connector. Your logo must be encoded in Base64 format. |
| description | String | A description of your custom connector. Your description is visible when you share your custom connector through a private link or through the community library. Markdown is allowed. |
| note | String | Notes for the initial version of your custom connector. |
| code | String | The Ruby code for your custom connector. Ensure that the code is stringified. Your code cannot exceed 10MB in size. |

#### # Sample request

#### # Sample response

### # Update custom connector

The Update operation allows you to update a custom connector in your workspace.

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| ID | Integer _required_ | The ID of the custom connector you plan to update. You can find your custom connector ID in the search custom connector endpoint. |

#### # Sample request

#### # Sample response

### # Release custom connector

The Release operation allows you to release the latest version of your custom connector. After you release the new version, it is used in all future jobs.

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| ID | Integer _required_ | The ID of the custom connector you plan to release. You can find your custom connector ID in the search custom connector endpoint. |

### # Sample request

#### # Sample response

##### # HTTP response codes

| Name | Description | Sample reply |
| --- | --- | --- |
| `200` | Success | `{"message": "Connector released successfully"}` |
| `400` | Bad request | `{"message": "Fix code errors before releasing the connector"}` or `{"message": "Connector’s released version is already the latest version"}` |

#### # 400 error examples

**Syntax example**

**Semantic example**

**Logical example**

The Share operation allows you to share the most recently released version of your custom connector. After you share your custom connector, all workspaces that have installed your connector through a private link or from the community library receive an update notification.

#### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| ID | Integer _required_ | The ID of the custom connector you plan to share. You can find your custom connector ID in the search custom connector endpoint. |

#### # Sample request

#### # Sample response

##### # HTTP response codes

| Name | Description | Sample reply |
| --- | --- | --- |
| `200` | Success | `{"message": "Connector shared successfully"}` |
| `400` | Bad request | `{"message": "There is no released version to share"}` or `{"message": "Connector’s shared version is already the latest released version"}` |

##### # 400 error examples

**Logical: No released version to share example**

**Logical: Latest release version is already shared example**