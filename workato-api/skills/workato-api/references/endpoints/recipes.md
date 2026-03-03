### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/recipes/:id | Get recipe details. |
| POST | /api/recipes | Create a recipe. |
| POST | /api/recipes/:id/copy | Copy a recipe. |
| PUT | /api/recipes/:id | Update a recipe. |
| GET | /api/recipes | List recipes belonging to user. |
| PUT | /api/recipes/:id/start | Start recipe. |
| PUT | /api/recipes/:id/stop | Stop recipe. |
| DELETE | /api/recipes/:id | Delete recipe. |
| POST | /api/recipes/:recipe\_id/reset\_trigger | Reset recipe trigger. |
| PUT | /api/recipes/:recipe\_id/connect | Update connection for an Application in a stopped recipe. |
| POST | /api/recipes/:recipe\_id/poll\_now | Activate a Polling Trigger for a Recipe. |

## # Get recipe details

Returns details about a recipe object. Lifetime task count has task data starting from March 19, 2021.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | Recipe ID. |

#### # Sample request

### # Response

## # Create a recipe

Creates a recipe in Workato based on parameters in the request.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| recipe | **object**  
_required_ | The recipe object. |
| recipe\[name\] | **string**  
_optional_ | Name of the recipe. |
| recipe\[code\] | **string**  
_required_ | JSON string representing the recipe lines. |
| recipe\[config\] | **string**  
_optional_ | JSON string representing the connection lines. |
| recipe\[folder\_id\] | **string**  
_optional_ | Folder for the recipe |
| recipe\[description\] | **string**  
_optional_ | Description of the recipe. |

#### # Sample request

### # Response

## # Update a recipe

Updates an existing recipe in Workato specified based on recipe ID. Recipe details are defined based on parameters in the request.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | Recipe ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| recipe | **object**  
_optional_ | The recipe object. |
| recipe\[name\] | **string**  
_optional_ | Name of the recipe. |
| recipe\[code\] | **string**  
_optional_ | JSON string representing the recipe lines. |
| recipe\[config\] | **string**  
_optional_ | JSON string representing the connection lines. |
| recipe\[folder\_id\] | **string**  
_optional_ | Folder for the recipe |
| recipe\[description\] | **string**  
_optional_ | Description of the recipe. |

#### # Sample request

### # Response

You cannot update a running recipe

Any update call to a running recipe will return an error.

## # Copy a recipe

Copy an existing recipe in Workato specified based on recipe ID.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_required_ | Recipe ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| folder\_id | **string**  
_optional_ | Folder id for the copied recipe |

#### # Sample request

### # Response

## # List recipes belonging to a user

Returns a list of recipes belonging to the authenticated user. Recipes are returned in descending ID order.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| adapter\_names\_all | **string**  
_optional_ | List of adapters names, separated by commas. Resulting recipes should use all of the given adapters. |
| adapter\_names\_any | **string**  
_optional_ | List of adapters names, separated by commas. Resulting recipes should use at least one of the given adapters. |
| folder\_id | **string**  
_optional_ | Return the recipes in the specified folder. |
| order | **string**  
_optional_ | Set ordering method. Possible options: activity, default. |
| page | **integer**  
_optional_ | Page number (defaults to 1). |
| per\_page | **integer**  
_optional_ | Page size (defaults to 10, maximum allowed is 100 per page). |
| running | **boolean**  
_optional_ | If `true`, returns running recipes. |
| since\_id | **integer**  
_optional_ | Use this parameter to retrieve recipes with IDs lower than the ID provided in the request. For example, if `since_id=15500`, Workato returns all recipes with IDs lower than `15500` (`0`\-`14999`). |
| stopped\_after | **string**  
_optional_ | Filter the list of recipes to exclude only those stopped after the date and time you specify. The date and time must be provided in ISO 8601 format according to the following pattern: `YYYY-MM-DDTHH:MM:SSZ`. |
| stop\_cause | **string**  
_optional_ | Reason that the recipe stopped. Possible reasons include —  
`trigger_errors_limit`: Recipe was stopped due to consecutive trigger errors  
`action_quota_limit`: Customer exceeded plan's task limit  
`trial_expired`: Customer's trial expired  
`txn_quota_limit`: Customer exceeded plan's job limit |
| updated\_after | **string**  
_optional_ | Filter the list of recipes to include only those updated after the date and time you specify. The date and time must be provided in ISO 8601 format according to the following pattern: `YYYY-MM-DDTHH:MM:SSZ`. |

#### # Sample request

### # Response

## # Start a recipe

Starts a recipe specified by recipe ID.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_optional_ | Recipe ID. |

#### # Sample request

### # Response

## # Stop a recipe

Stops a recipe specified by a recipe ID.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_optional_ | Recipe ID. |

#### # Sample request

### # Response

## # Delete a recipe

Delete a recipe specified by ID.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_optional_ | Recipe ID. |

#### # Sample request

### # Response

## # Reset recipe trigger

Reset recipe trigger cursor by recipe ID. Use this endpoint to re-sync data from the source application. The recipe should be designed to handle duplicate records because a re-sync processes every record again. Using this endpoint outside data orchestration scenarios may result in unintended behaviors, including data loss or corruption. Resetting a recipe trigger retains job history and records an event in the recipe's Activity audit log.

If you reset the trigger of an active recipe, Workato completes all jobs with a running, deferred, or pending status first. Then, it proceeds to the new jobs created by the reset trigger.

TRIGGER COMPATIBILITY

This endpoint is only compatible with polling and scheduled triggers. Resetting other triggers may have no effect, or cause unintended behaviors. These triggers include:

-   New CSV file in folder triggers
-   Function triggers
-   API triggers
-   RecipeOps triggers
-   Workbot triggers
-   Deprecated Kafka triggers (compatible with latest triggers)

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| recipe\_id | **integer**  
_required_ | ID of the recipe to reset. |

#### # Sample request

### # Response

## # Update a connection for a recipe

Updates the chosen connection for a specific connector in a stopped recipe.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| recipe\_id | **integer**  
_required_ | ID of the recipe. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| adapter\_name | **string**  
_required_ | The internal name of the connector. e.g. `salesforce` |
| connection\_id | **integer**  
_required_ | The ID of the connection that replaces the existing one. |

#### # Sample request

### # Response

## # Activate a polling trigger for a recipe

Initiate the polling function of a recipe with polling triggers by providing the recipe ID. This action causes the recipe's polling trigger to execute immediately.

Use the jobs APIs to check the status of a particular recipe.

### # Path parameters

| Name | Type | Description |
| --- | --- | --- |
| recipe\_id | **integer**  
_required_ | The ID of the recipe you plan to start. |

#### # Sample request

### # Response

-   Job started
-   Job already in progress
-   Error codes

#### # Job started

#### # Job already in progress

#### # Error codes

| Name | Description | Sample reply |
| --- | --- | --- |
| 404 | Not found | `{"success": false, "message": "Not Found"}` |
| 429 | Too many requests. A Retry-After header (opens new window) specifies how long to wait before making a new request. | `{"message": "Recipe is currently in trigger back off mode till 2023-06-23T11:02"}`, or `{"message": "Not enough transaction credit"},` or `{"message": "Not enough action quota"}` |
| 400 | Bad request | `{"message":"Trial has expired"}` |