Workato API allows you to work with On-prem Groups and On-prem Agents through the API.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/on\_prem\_groups | List On-prem groups. |
| POST | /api/on\_prem\_groups | Create On-prem group. |
| GET | /api/on\_prem\_groups/:id | Get On-prem group details. |
| PUT | /api/on\_prem\_groups/:id | Update On-prem group. |
| DELETE | /api/on\_prem\_groups/:id | Delete an On-prem group. |
| GET | /api/on\_prem\_groups/:id/status | Get On-prem group status. |
| GET | /api/on\_prem\_agents | List On-prem agents. |
| POST | /api/on\_prem\_agents | Create On-prem agent. |
| GET | /api/on\_prem\_agents/:id | Get On-prem agent details. |
| PUT | /api/on\_prem\_agents/:id | Update On-prem agent. |
| DELETE | /api/on\_prem\_agents/:id | List On-prem agents. |
| GET | /api/on\_prem\_agents/:id/status | Get On-prem agent status. |
| GET | /api/on\_prem\_agents/search | Search for On-prem agent. |

## # List On-prem Groups

List all On-prem groups in your workspace.

### # Response

## # Create On-prem Group

Create an On-prem group.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
 | The On-prem group name. |

#### # Sample request

### # Response

## # Get On-prem Group details

Get details about an On-prem group.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem group ID. |

### # Response

## # Update On-prem Group

Update an On-prem group.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem group ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
 | The On-prem group name. |

#### # Sample request

### # Response

## # Delete On-prem Group

Delete an On-prem group. All on-prem agents in this group will be deleted.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem group ID. |

### # Response

## # Get On-prem Group status

Get the status of an On-prem group.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem group ID. |

### # Response

## # List On-prem Agents

List all On-prem agents in your workspace.

### # Response

#### # Response schema

| Name | Description |
| --- | --- |
| name | The On-prem agent name. |
| os | The server operating system. Available OS are windows, linux, and mac |
| on\_prem\_group\_id | The On-prem group ID. |
| awaiting\_setup | True if agent is not configured. |
| enabled | True if agent is enabled. |

## # Create On-prem Agent

Create an On-prem agent.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
 | The On-prem agent name. |
| os | **string**  
 | The server operating system. |
| on\_prem\_group\_id | **integer**  
 | The On-prem group ID. See List On-prem groups. |
| awaiting\_setup | **boolean**  
_optional_ | `true` if agent should be created in awaiting setup state. Set to `false` to skip agent setup and get its status right away. |

#### # Sample request

### # Response

## # Get On-prem Agent details

Get details of an On-prem agent.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem agent ID. |

### # Response

## # Update On-prem Agent

Update an On-prem agent.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem agent ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
 | The On-prem agent name. |
| os | **string**  
 | The server operating system. |
| on\_prem\_group\_id | **integer** | The On-prem group ID. See List On-prem groups. |

#### # Sample request

### # Response

## # Delete On-prem Agent

Delete an On-prem agent.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem agent ID. |

### # Response

## # Get On-prem Agent status

Get status of an On-prem agent.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
 | On-prem agent ID. |

### # Response

## # Search for On-prem Agent by common name

Get On-prem agents that matches a common name.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| cn | **string**  
 | Common name of on-prem agent. |

### # Response