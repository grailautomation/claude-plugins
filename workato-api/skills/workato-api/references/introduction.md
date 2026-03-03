## # Developer API

Workato's developer API provides access to various Workato resources, through which you can manage recipes, connections, and jobs. This allows your to automate all aspects of your Workato workspace - from deploying recipe manifests from development to production or deploying new on-prem agents within your network landscape.

## # Base URL

The Workato API is a collection of API endpoints for interacting with Workato users, recipes, and much more. Each endpoint contains the **base URL** and the **resource path** to the object.

The base URL of the API endpoint depends on the data center that you use. Here are Workato data centers:

-   US Data Center: `https://www.workato.com/api/`
-   EU Data Center: `https://app.eu.workato.com/api/`
-   JP Data Center: `https://app.jp.workato.com/api/`
-   SG Data Center: `https://app.sg.workato.com/api/`
-   AU Data Center: `https://app.au.workato.com/api/`

## # Authentication

Workato API uses API tokens to authenticate requests. You may generate an API token by creating an API client under Workspace admin and assigning it both a client role and project scopes.

Legacy API key deprecation

Prior to API clients, Workato's API used a legacy full access API key and email in **request headers** or the **query parameters** to authenticate requests. This will continue to be supported with your legacy migrated API client that represents your API key and email. We strongly recommend migrating over to API Clients for authentication to Workato APIs. Learn more

Legacy API keys will be supported until 1/1/2024 and will be deprecated thereafter. All API requests authenticated via legacy API keys will start to be rejected after this point in time.

### # Provide API tokens as a bearer token

Provide your API client's API token in the request headers as a `bearer` token.

### # Supported Formats

Workato API supports sending request body with the `application/json` content-type. All replies are also encoded in `application/json; charset=utf-8`.

## # How to generate an API token

You can generate an API token by creating an API Client under Workspace admin and under the API Clients tab. Find out more about configuring API clients and roles.

## # HTTP response codes

| Name | Description | Sample reply |
| --- | --- | --- |
| `200` | Success | `{"Success": true}` |
| `400` | Bad request | `{"message": "Bad request"}` |
| `401` | Unauthorized | `{"message": "Unauthorized"}` |
| `404` | Not found | `{"message": "Not found"}` |
| `500` | Server error | `{"message":"Server error","id":"3188c2d0-29a4-4080-908e-582e7ed82580"}` |