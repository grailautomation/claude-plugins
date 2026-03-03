The Event streams APIs allow users to publish and retrieve messages from Event topics. Each message in the topic has an ID that is used as an offset. You must store either the **message ID** or **last message timestamp** in order to use this endpoint.

You can access the OpenAPI specification for Workato Event streams APIs here (opens new window).

NEW API DOMAIN FOR WORKATO EVENT STREAMS

Workato has migrated the Event streams API to a new domain:

Legacy endpoints published on `www.workato.com/api` continue to work but are limited to 1000 requests per minute. The legacy domain supports `/consume` and `/publish` endpoints, with the same request and response formats listed on this page.

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| POST | /api/v1/topics/:topic\_id/consume | Consume messages from a topic. |
| POST | /api/v1/topics/:topic\_id/publish | Publish a message to a topic. |
| POST | /api/v1/batch/topics/:topic\_id/publish | Publish a batch of messages to a topic. |

## # Consume messages

Retrieve messages from the topic. This resource provides the option to retrieve all messages within the topic or, by including parameters in the request body, to fetch messages after a specified ID or timestamp. The response is limited to a maximum of 50 messages in each batch.

You can enable long polling mode by setting the `timeout_secs` parameter. In this mode, the API returns available messages instantly. If there are no messages, the API waits for a maximum of `timeout_secs` seconds. If a new message appears within this timeframe, it is instantly returned; otherwise, the API provides an empty list after the call times out.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| topic\_id | **integer**  
_required_ | Event topic ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| after\_message\_id | **string**  
_optional_ | Message ID. The service returns all messages after the message with the specified ID. The ID must correspond to a message that exists in the topic. |
| since\_time | **string**  
_optional_ | Timestamp in RFC 3339 format. The service returns all messages after the timestamp specified. The current time is used if the `since_time` value is a time in the future. |
| batch\_size | **integer**  
_optional_ | Maximum batch size to return. The maximum value is 50. Returns batch of 50 messages if not specified. |
| timeout\_secs | **integer**  
_optional_ | Maximum timeout for long polling. The maximum value is 60. The default value is 0. When 0, long polling is disabled. |

USING SINCE\_TIME PARAMETER

We recommend using `after_message_id` to control the topic message cursor. `since_time` should only be used only for the first request (to poll messages from a specific timestamp without polling the whole topic), or if for some reason you need to re-retrieve messages from the topic. Using `since_time`, especially in combination with batch publish and long polling doesn't guarantee message order and can lead to skipped messages.

#### # Sample request

### # Response

## # Publish message

Publish a message to a topic. The message must comply with the topic schema.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| topic\_id | **integer**  
_required_ | Event topic ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
|  | **JSON**  
_required_ | Message to publish to the topic. The message must comply with the topic schema. |

#### # Sample request

### # Response

## # Publish a batch of messages

Publish a batch of messages to a topic. The messages must comply with the topic schema.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| topic\_id | **integer**  
_required_ | Event topic ID. |

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| payloads | **Array of JSON**  
_required_ | Array of messages to publish to the topic. The messages must comply with the topic schema. The maximum array size is 100. |

#### # Sample request

### # Response