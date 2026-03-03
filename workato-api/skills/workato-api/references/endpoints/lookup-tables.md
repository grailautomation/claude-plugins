Use the endpoints below to manage lookup tables programmatically.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/lookup\_tables | List tables. |
| GET | /api/lookup\_tables/:lookup\_table\_id/rows | List rows. |
| GET | /api/lookup\_tables/:lookup\_table\_id/lookup | Look up a row. |
| GET | /api/lookup\_tables/:lookup\_table\_id/rows/:row\_id | Get a row. |
| POST | /api/lookup\_tables/:lookup\_table\_id/rows | Add a row. |
| POST | /api/lookup\_tables | Create a new lookup table. |
| POST | /api/lookup\_tables/batch\_delete | Delete lookup tables in batch. |
| PUT | /api/lookup\_tables/:lookup\_table\_id/rows/:row\_id | Update a row. |
| DELETE | /api/lookup\_tables/:lookup\_table\_id/rows/:row\_id | Delete a row. |

## # List lookup tables

Returns a list of lookup tables belonging to a customer. Workato includes the `project_id` of the project to which the lookup table belongs in the response.

### # Parameters

| Name | Type | Description |
| --- | --- | --- |
| page | **integer** | Page number. Defaults to 1. |
| per\_page | **integer** | Page size. Defaults to 100 (maximum is 100). |

### # Sample request

### # Response

## # List rows

Returns a lists of rows from the lookup table. Supports filtering and pagination.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| page | **integer** | Page number. Defaults to 1. |
| per\_page | **integer** | Page size. Defaults to 500 (maximum is 1000). |
| by\[`<col name>`\] | **string**  
 | Filter criteria. The column name should be provided as follows: `by[<col name>]`. To match by multiple columns, provide multiple parameters. Refer to the sample request for more details. When not supplied, all rows are returned. |

### # Sample request

#### # Request 1: list rows

#### # Request 2: filter and list rows

### # Response

#### # Response 1: list rows

#### # Response 2: filter and list rows

## # Lookup a row

Finds the first row matching the given criteria in the lookup table. Returns a 404 when the lookup fails.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| by\[`<col name>`\] | **string**  
_required_ | Lookup criteria. The column name should be provided as follows: `by[<col name>]`. To match by multiple columns, provide multiple parameters. Refer to the sample request for more details. |

#### # Sample request

### # Response

## # Get a row

Get a row from the lookup table.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |
| row\_id | **integer**  
_required_ | Row id |

#### # Sample request

### # Response

## # Add a row

Adds a row to the lookup table.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| data | **Hash**  
_required_ | The hash contains the data for the new row. |

#### # Sample request

### # Response

## # Create a new lookup table

Create a new lookup table. Depending on your requirements, you can choose to make the lookup table available for general access across your workspace or limit its scope to a specific project.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Provide a name for your new lookup table. |
| project\_id | **integer**  
_optional_ | Specify a `project_id` to scope the lookup table to a specific project. If you do not provide a `project_id`, the lookup table's scope is global.  
Use the list projects API to obtain a list of projects in your workspace. |
| schema | **hash**  
_required_ | Determine the structure of your lookup table by supplying a schema and specifying the name of each of the columns in your table, for example: `[{ "label": "Name" }]`.  
Lookup tables support a maximum of ten columns. |

### # Sample request

#### # Response

## # Delete lookup tables in batch

Use this endpoint to delete lookup tables in batch.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| ids | **hash**  
_required_ | Include the ID(s) of the lookup table(s) you plan to delete. |

### # Sample request

#### # Response

## # Update a row

Updates a row in the lookup table.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |
| row\_id | **integer**  
_required_ | Row id |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| data | **Hash**  
_required_ | The hash containing the data for the updated row. Only the columns provided are updated. |

#### # Sample request

### # Response

## # Delete a row

Delete a row from the lookup table

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| lookup\_table\_id | **integer**  
_required_ | Lookup table id |
| row\_id | **integer**  
_required_ | Row id |

#### # Sample request

### # Response