Use the endpoints below to manage environment properties programmatically.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/properties | Lists environment properties that matches a prefix. |
| POST | /api/properties | Upserts environment properties. |

## # List properties by prefix

Returns a list of environment properties belonging to a customer that matches a prefix. For example, if the prefix provided is `salesforce_sync.`, any environment property with a name **beginning** with 'salesforce\_sync.' will be returned.

### # Parameters

| Name | Type | Description |
| --- | --- | --- |
| prefix | **string**  
_required_ | Return properties with the given prefix. E.g: `salesforce_sync.`. |

#### # Sample request

### # Response

## # Upsert property

Upserts environment properties. Matches by the names of the properties provided in the request.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| properties | **Hash**  
_required_ | Contains the names and values of the properties to upsert. |

#### # Sample request

### # Response