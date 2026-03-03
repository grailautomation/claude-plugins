GLOSSARY

-   **Manifest:** A container of different assets, including recipes, lookup tables, connections, and more.
    
-   **Package:** The build of a manifest. Contains the source code of each asset within a manifest. It includes the latest version of the asset available when the package was created.
    

### # Quick reference

| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/export\_manifests/folder\_assets | View assets in a folder. |
| POST | api/export\_manifests | Create an export manifest. |
| PUT | api/export\_manifests/:id | Update an export manifest. |
| GET | api/export\_manifests/:id | View an export manifest. |
| DELETE | /api/export\_manifests/:id | Delete an export manifest. |
| POST | /api/packages/export/:manifest\_id | Export package based on a manifest. |
| POST | /api/packages/import/:folder\_id | Import package into a folder. |
| GET | /api/packages/:id | Get package by ID. |
| GET | /api/packages/:id/download | Download a package. |

___

## # View assets in a folder

View assets in a folder. You can use this endpoint to help you create or update an export manifest.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| folder\_id | **integer**  
_optional_ | The ID of the folder containing the asset. Defaults to the root folder. |
| include\_test\_cases | **boolean**  
_optional_ | Includes test cases from the list of assets. Defaults to `false.` |
| include\_data | **boolean**  
_optional_ | Includes data from the list of assets. Defaults to `false.` |

#### # Sample request

### # Response

___

## # Create an export manifest

Create an export manifest.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_required_ | Name of the new manifest. |
| assets | **object**  
_required_ | Dependent assets. |
| id | **integer**  
_required_ | ID of the dependency. |
| type | **string**  
_required_ | Type of dependent asset. |
| checked | **boolean**  
_optional_ | Determines if the asset is included in the manifest. Defaults to `true`. |
| version | **integer**  
_optional_ | The version of the asset. Defaults to the latest version. |
| folder | **string**  
_optional_ | The folder that contains the asset. Defaults to `""`. |
| absolute\_path | **string**  
_optional_ | The absolute path of the asset. Defaults to root folder. |
| root\_folder | **boolean**  
_optional_ | Name root folder. Defaults to `false`. |
| unreachable | **boolean**  
_optional_ | Whether the asset is unreachable. Defaults to `false`. |
| zip\_name | **string**  
_optional_ | Name in the exported zip file. By default, Workato auto-generates a name with this structure: `asset_#{index}.#{type}.json`. |
| folder\_id | **integer**  
_optional_ | The ID of the folder containing the asset. Defaults to the root folder. |
| include\_test\_cases | **boolean**  
_optional_ | Whether the manifest includes test cases or not. Defaults to `false`. |
| auto\_generate\_assets | **boolean**  
_optional_ | Auto-generates assets from a folder. Defaults to `false`. |
| include\_test\_cases | **boolean**  
_optional_ | This parameter includes test cases from automatic asset generation. Defaults to `false`. |
| include\_data | **boolean**  
_optional_ | This parameter includes data from automatic asset generation. Defaults to `false`. |

#### # Sample request

### # Response

### # Auto-generate assets

If you plan for Workato to auto-generate your assets, you can pass the parameter `auto_generate_assets` into the payload of the request. You must specify the `folder_id` you plan to have auto-generated. You can also choose to include test cases and data by adding the `include_test_cases` and `include_data` parameters. Note that test cases and data are excluded by default. Additionally, you can include `auto_run` in the payload to generate the package automatically.

#### # Sample request

### # Response

#### # Possible statuses

| Status | Definition |
| --- | --- |
| `working` | Active. |
| `archived` | Deleted. |

___

## # Update an export manifest

Update an export manifest.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_string_ | The ID of the dependency. |

### # Payload

Update the properties contained in `assets[]` to replace the assets previously defined.

| Name | Type | Description |
| --- | --- | --- |
| name | **string**  
_optional_ | Name of the manifest. Update this value to change the manifest name. Defaults to previous name. |
| assets | **object**  
_required_ | Dependent assets. |
| id | **integer**  
_required_ | ID of the dependency. |
| type | **string**  
_required_ | Type of dependent asset. |
| checked | **boolean**  
_optional_ | Determines if the asset is included in the manifest. Defaults to `true`. |
| version | **integer**  
_optional_ | The version of the asset. Defaults to the latest version. |
| folder | **string**  
_optional_ | The folder that contains the asset. Defaults to `""`. |
| absolute\_path | **string**  
_optional_ | The absolute path of the asset. Defaults to root folder. |
| root\_folder | **boolean**  
_optional_ | Name root folder. Defaults to `false`. |
| unreachable | **boolean**  
_optional_ | Whether the asset is unreachable. Defaults to `false`. |
| zip\_name | **string**  
_optional_ | Name in the exported zip file. By default, Workato auto-generates a name with this structure: `asset_#{index}.#{type}.json`. |
| folder\_id | **integer**  
_optional_ | The ID of the folder containing the asset. Defaults to the root folder. |
| include\_test\_cases | **boolean**  
_optional_ | Whether the manifest includes test cases or not. Defaults to `false`. |
| auto\_generate\_assets | **boolean**  
_optional_ | Auto-generates assets from a folder. Defaults to `false`. |
| include\_test\_cases | **boolean**  
_optional_ | This parameter includes test cases from automatic asset generation. Defaults to `false`. |
| include\_data | **boolean**  
_optional_ | This parameter includes data from automatic asset generation. Defaults to `false`. |

#### # Sample request

### # Response

### # Auto-generate assets

If you plan for Workato to auto-generate your assets, you can pass the parameter `auto_generate_assets` into the payload of the request. You must specify the `folder_id` you plan to have auto-generated. You can also choose to include test cases and data by adding the `include_test_cases` and `include_data` parameters. Note that test cases and data are excluded by default. Additionally, you can include `auto_run` in the payload to generate the package automatically.

#### # Sample request

### # Response

___

## # View an export manifest

View an export manifest.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **integer**  
_string_ | The ID of the dependency. |

#### # Sample request

### # Response

___

## # Delete an export manifest

Delete an export manifest.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | Export manifest ID. |

#### # Sample request

### # Response

___

## # Export a package based on a manifest

Export a package based on a manifest.

ENDPOINT PRIVILEGES ALSO PROVIDE ACCESS TO ASSETS

When you provide an API client with privileges to this endpoint, the API client is also granted the ability to view other assets like recipes, lookup tables, Event topics, and message templates by examining the resulting zip file.

This is an asynchronous request. Use GET package by ID endpoint to get details of the exported package.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | Export manifest ID. |

#### # Sample request

### # Response

___

## # Import a package into a folder

Import a package (zip file) into a folder.

ENDPOINT PRIVILEGES ALSO PROVIDE ACCESS TO ASSETS

When you provide an API client with privileges to this endpoint, it also grants the ability to create or update other assets like recipes, lookup tables, Event topics, and message templates through importing packages.

This is an asynchronous request. Use GET package by ID endpoint to get details of the imported the package.

The input (zip file) is a `application/octet-stream` payload containing package content. URL parameter **restart\_recipes** must be `true` if the running recipes need to be restarted upon import.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | Folder ID. |
| restart\_recipes | **boolean**  
_optional_ | Value must be `true` to allow the restarting of running recipes during import.  
Packages cannot be imported if there are running recipes and this parameter equals `false` or is not provided. |

#### # Sample request

### # Response

___

## # Get package by ID

Get details of an imported or exported package.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | Package ID. |

#### # Sample request

### # Response

-   This shows the response from the retrieval of a completed export manifest.

-   This shows the response from the retrieval of a failed export manifest

-   This shows the response from the retrieval of a completed import.

NOTE

For any completed import, it is important to also check each recipe's `import_result`. Learn more about the possible import\_result values.

-   This shows the response from the retrieval of a failed import.

NOTE

For any failed import, not all recipes may be returned in `recipe_status` as they may not have been updated before the import failed. Learn more about the possible import\_result values..

### # Recipe import\_result values

There are a total of six possible results:

-   `no_update_or_update_without_restart`
    
-   Indicates no restart was needed for the recipe. Either recipe could be updated without it or no update was made. **Successful import**
    
-   `not_found`
    
-   Unexpected error when recipe cannot be found. Should not often be seen. **Import has failed with no update to recipe.**
    
-   `stop_failed`
    
-   For recipes that need to be restarted, we attempt to stop the recipe. This state indicates we could not stop the recipe. **Import has failed with no update to recipe.**
    
-   `stopped`
    
-   Workato stopped the recipe but recipe was not restarted due to errors in the recipe. **Import has failed with recipe updated but not restarted**
    
-   `restart_failed`
    
-   Workato attempted to restart recipe but failed to do so. **Import has failed with recipe updated but not restarted**
    
-   `restarted`
    
-   Workato successfully restarted recipe after update. **Successful import**
    

___

## # Download package

Downloads a package.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| id | **string**  
_required_ | Package ID. |

#### # Sample request

Follow redirects in cURL

Use the `-L` flag to follow redirect paths.

### # Response

If successful, you will be redirected to the package content. Returns `404` if package not found or doesn't have content.