Use the following endpoints to manage collaborators in your workspace.

ENDPOINT ACCESS

Your API client must be assigned specific privileges for the **Invite a collaborator**, **Get list of users**, **Get user details**, and **Get user privileges** endpoints. These privileges are determined by your API client role.

Additionally, if your workspace uses environments, these privileges are only available to API clients with `DEV` access.

To enable endpoint access:

You can enable access to these endpoints by editing an existing API client role or by creating a new API client role:

1

Navigate to **Workspace admin > API clients > Client roles**.

Select the role you plan to edit.

Alternatively, click **\+ Add client role** to create a new API client role.

2

Select **Admin** and navigate to **Workspace collaborators > Collaborators**.

3

Select the checkboxes next to the endpoints you plan to enable for this role.

-   **Invite** `POST /api/member_invitations`
-   **Get collaborators** `GET /api/members`
-   **Get collaborator** `GET /api/members/:id`
-   **Get collaborator privileges** `GET /api/members/:id/privileges`

_Select the endpoints you plan to enable_

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| POST | /api/member\_invitations | Invite a collaborator to your workspace. |
| GET | /api/members | Get a list of members in your workspace. |
| GET | /api/members/:id | Get details about a user you specify. |
| GET | /api/members/:id/privileges | Get the role and privileges for a workspace user you specify. |

## # Invite a collaborator

Invite a collaborator to your workspace. If the email you provide doesn't belong to an existing user, the API sends an email invitation. Collaborators can join your workspace after they create a Workato account. You can invite a specific email and workspace combination once every twenty minutes.

ENDPOINT ACCESS

Your API client role must be assigned the **Invite** `POST /api/member_invitations` privilege to use this endpoint.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | The name of the collaborator. |
| email | **string**  
_required_ | The email of the collaborator. |
| role\_name | **string**  
_conditional_ | The role to assign the collaborator.  
**Required** if `env_roles` is not provided. |
| env\_roles | **object**  
_conditional_ | The environment roles object.  
**Required** if `role_name` is not provided. |
| env\_roles\[environment\_type\] | **string**  
_conditional_ | The environment type of the workspace you're inviting the collaborator to.  
**Required** if `role_name` is not provided. |
| env\_roles\[name\] | **string**  
_conditional_ | The role to assign the collaborator for the specific environment.  
**Required** if `role_name` is not provided. |

SPECIFY ROLES FOR DIFFERENT ENVIRONMENTS

You must provide either `role_name` or `env_roles` in the payload. `role_name` only assigns a role in the `dev` environment. Use `env_roles` to specify the environment type and role for other environments.

Workato does not support a mixed approach to assigning roles. This means that when you combine the `env_roles` and `role_name` in the payload, Workato ignores the `role_name` and only assigns the roles specified by the `env_roles` object.

### # Sample requests

-   Request 1: Invite a collaborator using `role_name`
-   Request 2: Invite a collaborator using `env_roles`
-   Request 3: Invite a collaborator using `env_roles`: No access
-   Request 4: Invite a collaborator with a nonexistent or unavailable role
-   Request 5: Invite a collaborator to a nonexistent environment

#### # Request 1: Invite a collaborator using `role_name`

This example request creates an invitation for the `dev` environment only.

Response 1

#### # Request 2: Invite a collaborator using `env_roles`

This example request creates an invitation for the `dev`, `test`, and `prod` environments. It assigns the collaborator an `Admin` role in the `dev` environment, an `Analyst` role in the `test` environment, and an `Operator` role in the `prod` environment.

Response 2

#### # Request 3: Invite a collaborator using `env_roles` - No access

This example creates an invitation solely for the `prod` environment. By omitting additional environments and roles from the `env_roles` object, the default behavior assigns the collaborator a `No access` role in all other environments.

Response 3

#### # Request 4: Invite a collaborator with a nonexistent or unavailable role

When you invite a collaborator using a role that doesn't exist or isn't available, this endpoint returns a `400` error: `Role Not existing role not found`.

Response 4

#### # Request 5: Invite a collaborator to a nonexistent environment

When you invite a collaborator to an environment that doesn't exist, this endpoint returns a `400` error: `Environment Not existing environment not found`.

Response 5

___

## # Get list of collaborators

Get a list of all users in a workspace. This resource returns the following information for each user in your workspace:

-   User ID
-   Grant type: Where `team` indicates the user is a workspace collaborator and `federation_manager` indicates the user is a workspace moderator.
-   Role
-   External ID
-   Name
-   Email
-   Timezone
-   Last activity log: This log displays the user's most recent action within a workspace. For AHQ-enabled workspaces, it only displays the latest activity in the DEV environment. The log records events such as logging in, logging out, joining a workspace, generating a token, disconnecting a connection, and more. Refer to our activity audit log reference documentation for a complete list of activities that are captured in the log and can be returned in this request.
-   Created at

ENDPOINT ACCESS

Your API client role must be assigned the **Get collaborators** `GET /api/members` privilege to use this endpoint.

### # Sample request

#### # Response

___

## # Get collaborator details

Get details about a workspace member you specify. This resource returns the following information in the response:

-   User ID
-   Grant type: Where `team` indicates the user is a workspace collaborator and `federation_manager` indicates the user is a workspace moderator.
-   Role
-   External ID
-   Name
-   Email
-   Timezone
-   Last activity log: This displays the user's most recent action within a workspace and captures the same data as the activity audit log. For workspaces with AHQ, this only displays the last activity within the DEV environment. It can include events such as logging in, logging out, joining a workspace, generating a token, disconnecting a connection, and more. Refer to our activity audit log reference documentation for a complete list of activities that are captured in the log and can be returned in this request.
-   Created at

ENDPOINT ACCESS

Your API client role must be assigned the **Get collaborator** `GET /api/members/:id` privilege to use this endpoint.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | The ID of the user whose information you plan to retrieve. |

### # Sample request

#### # Response

___

## # Get collaborator privileges

Get the role and privileges for a user you specify. This resource includes details for system and custom roles. This resource returns an array of roles for each environment in the workspace (for example, DEV, TEST, and PROD), which includes the following information:

-   Environment type
-   User role
-   All permissions assigned to the role

ENDPOINT ACCESS

Your API client role must be assigned the **Get collaborator privileges** `GET /api/members/:id` privilege to use this endpoint.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | The ID of the user whose role and privileges you plan to retrieve. |

### # Sample request

#### # Response