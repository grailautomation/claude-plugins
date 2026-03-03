Use these API endpoints to obtain information about standard Workato connectors. This is useful if you plan to generate a marketplace of apps.

## # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| Get | api/integrations | Returns a list of connectors and metadata specified in request. |
| Get | api/integrations/all | Returns a paginated list of all connectors and associated metadata in a non-embedded workspace. The response includes standard and platform connectors. |

Returns a list of connectors and associated metadata specified in the API request.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| applications | **string**  
_required_ | Comma separated connector identifiers. |

### # Sample request

### # Response

## # List all platform connectors

Returns a paginated list of all connectors and associated metadata in a non-embedded workspace. This includes both standard and platform connectors. Workato includes the total number of records at the end of the response.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| page | **integer**  
_optional_ | Page number. Defaults to 1. If the total number of connectors exceeds the record per page limit, call the next page to retrieve subsequent pages. |
| per\_page | **integer**  
_optional_ | Number of records per page. Defaults to 1 and has a maximum of 100. If you enter more than 100, Workato only returns 100 records in the response. |

### # Sample request

### # Response

ABRIDGED RESPONSE

The preceding response is abridged to display the total record count returned in the response. For an example of the connectors and associated metadata Workato returns for each record, see the list connector metadata API.