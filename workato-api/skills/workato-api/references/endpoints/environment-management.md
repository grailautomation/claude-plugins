The following endpoints enable you to manage and secure your environments by providing tools for working with external secrets managers and monitoring user activities with audit log records.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| POST | /api/secrets\_management/clear\_cache | Clears the secrets management cache. |
| GET | /api/activity\_logs | Gets audit log records. |

## # Clear secrets management cache

Clears the secrets management cache to retrieve the latest available credentials from an external secrets manager. You don't need to disconnect and reconnect the connection for the refreshed credentials to take effect.

For example, when you update a secret in your external secrets manager, you can send a request to the Workato API simultaneously to clear the secrets management cache. This ensures that Workato retrieves the latest secret when required. This allows you to programmatically sync secrets with Workato every time they're changed as part of the secrets rotation process.

Note that the request doesn't require a body.

### # Sample request

### # Sample response

## # Get audit log

Retrieves detailed information on activities within a specific environment. Each log entry includes the event's unique identifier, timestamp, type, and details about the workspace, user, and resource involved:

-   The `workspace` object contains the workspace ID, name, email, and environment.
-   The `user` object includes the user ID, name, and email.
-   The `details` object provides additional information about the request, such as IP address, user agent, and specific activity performed.
-   The `resource` object describes the resource involved, including its ID, name, type, and associated email if applicable.

CREATE SEPARATE API CLIENTS FOR EACH ENVIRONMENT ACTIVITY LOGS

To obtain logs from DEV, TEST, and PROD environments, create separate API clients for each environment and combine the data as required for your use case.

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| page\[after\] | **integer**  
_optional_ | Specify the starting point for the next set of results, based on the last result of the current page. |
| page\[size\] | **integer**  
_optional_ | Specify the number of results per page. The default and maximum number of records is 100. |
| from | **string**  
_optional_ | Specify the start of the time range for which to retrieve audit logs. Provide in ISO 8601 format. |
| to | **string**  
_optional_ | Specify the end of the time range for which to retrieve audit logs. Provide in ISO 8601 format. |
| users\_ids\[\] | **array of integers**  
_optional_ | Filter logs to include activities performed by specified user IDs. |
| include\_resource\_types\[\] | **array of strings**  
_optional_ | Filter logs to include activities related to specified resource types. |
| exclude\_resource\_types\[\] | **array of strings**  
_optional_ | Exclude activities related to specified resource types. |
| include\_event\_types\[\] | **array of strings**  
_optional_ | Filter logs to include activities of specified event types. |
| exclude\_event\_types\[\] | **array of strings**  
_optional_ | Exclude activities of the specified event types. |

TIMEZONE

All data centers use the system timezone, Pacific Daylight Time (PDT). When you specify a timezone in the `from` and `to` query parameters, the system converts it to and displays it as PDT.

### # Sample requests

-   Request 1: Without query parameters
-   Request 2: Get the last three records
-   Request 3: Get the activities of one day for two users
-   Request 4: Include activities with specific resource\_types and event\_types
-   Request 5: Exclude activities with specific resource\_types and event\_types
-   Request 6: Get activities with a non-existent event type or user ID

#### # Request 1: Without query parameters

The following example request returns a list of all activities in the environment associated with the API client:

Response 1: Without query parameters

#### # Request 2: Get the last three records

The following example request retrieves the three most recent activity log entries. This request returns activities for the environment associated with the API client:

Response 2: Get the last three records

#### # Request 3: Get the activities of one day for two users

The following example request retrieves the activities of two users on June 6, 2024. This request returns activities for the environment associated with the API client:

Response 3: Get the activities of one day for two users

#### # Request 4: Include activities with specific resource\_types and event\_types

The following example request includes activities with the `resource_type` `ApiPrivilegeGroup` and `event_type` `api_privilege_group_updated`. This request returns activities for the environment associated with the API client:

Response 4: Include activities with specific resource\_types and event\_types

#### # Request 5: Exclude activities with specific resource\_types and event\_types

The following example request excludes activities with the `resource_type` `User` and `event_type` `user_logout`. This request returns activities for the environment associated with the API client:

Response 5: Exclude activities with specific resource\_types and event\_types

#### # Request 6: Get activities with a non-existent event type or user ID

The following example request attempts to retrieve the activities of a non-existent event type and user ID. Filtering activities by a non-existent event type or user ID results in an empty array:

Response 6: Get activities with a non-existent event type or user ID