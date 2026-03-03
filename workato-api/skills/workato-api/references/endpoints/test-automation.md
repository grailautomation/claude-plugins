The following endpoints enable you to use the Test Automation feature programmatically.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| POST | /api/test\_cases/run\_requests | Run test cases. |
| GET | /api/test\_cases/run\_requests/{id} | Get the current state of a test case run request. |
| GET | /api/recipes/{recipe\_id}/test\_cases | Get test cases. |

## # Run test cases

Use this endpoint to run test cases. You can specify the test cases to run in the following ways:

-   All test cases of all recipes in a manifest
-   All test cases of all recipes in a project
-   All test cases of all recipes in a folder
-   All test cases belonging to a particular recipe
-   Test cases you specify

This endpoint is asynchronous. You can use the run request `id` to poll the current state of the request using the /api/test\_cases/run\_requests/{id} endpoint.

### # Request body

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| manifest\_id | **integer** _optional_ | Run test cases for all recipes in the export manifest you specify. |
| project\_id | **integer** _optional_ | Run test cases for all recipes in the project you specify. Use the list projects endpoint to retrieve the IDs of all projects in your workspace. |
| folder\_id | **integer** _optional_ | Run test cases for all recipes in the folder you specify. |
| recipe\_id | **integer** _optional_ | Run all test cases for the recipe you specify. |
| test\_case\_ids | **array of strings** _optional_ | Run specific test cases by ID. |

### # Sample request

### # Sample response

## # Get the current state of a test case run request

Get the current state of a test case run request. For completed requests, Workato also returns the test coverage data along with the results.

### # URL parameters

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| id | **string** _required_ | The run request's ID. |

### # Sample request

### # Sample response

## # Get test cases

Returns a collection of test cases belonging to the recipe you specify.

### # URL Parameters

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| recipe\_id | **integer** _required_ | The ID of the recipe you plan to retrieve test case details from. |

### # Sample request

### # Sample response