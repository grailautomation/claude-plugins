| Type | Resource | Description |
| --- | --- | --- |
| GET | /api/recipes/:recipe\_id/jobs | List jobs from a recipe. |
| GET | /api/recipes/:recipe\_id/jobs/:job\_handle | Returns a single job's metadata. |
| POST | /api/job/resume | Resumes a particular job based on the `resume_token` you provide. This endpoint returns HTTP status code `204`, indicating successful request processing without any content included in the response. This endpoint is leveraged by SDK Wait for resume actions. |

## # List jobs from a recipe

Returns aggregated job information as well as detailed job information for a specified recipe in Workato.

Run-time data not available

Run-time data is the data that flows through the recipe at the time of job execution. This includes the input and output data from individual steps.

This data is available through the Workato platform on the job details page.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| recipe\_id | **integer**  
_required_ | Recipe ID. |

### # Query parameters

| Name | Type | Description |
| --- | --- | --- |
| offset\_job\_id | **string**  
_optional_ | Offset job ID. |
| prev | **boolean**  
_optional_ | Defaults to `false`. When `prev=false`, this call returns jobs completed prior to the `offset_job_id`. If `prev=true`, jobs newer than the `offset_job_id` are returned. |
| status | **string**  
_optional_ | Filter by status - `succeeded`, `failed` or `pending`. |
| rerun\_only | **boolean**  
_optional_ | If `true`, returns jobs that were rerun only. |
| offset\_run\_id | **integer**  
_(deprecated)_ | Offset run ID. This parameter has been deprecated. |
| failed | **boolean**  
_(deprecated)_ | If `true`, returns failed jobs only. This parameter has been deprecated. |

#### # Sample request

### # Response

## # Get a job

Returns a single job's metadata by its job handle.

Run-time data not available

Run-time data is the data that flows through the recipe at the time of job execution. This includes the input and output data from individual steps.

This data is available through the Workato platform on the job details page.

### # URL parameters

| Name | Type | Description |
| --- | --- | --- |
| recipe\_id | **integer**  
_required_ | Recipe ID. |
| job\_handle | **string**  
_required_ | The job's unique identifier. |

#### # Sample request

### # Response

## # Resume a job

Resumes a particular job based on the `resume_token` you provide. This endpoint returns HTTP status code `204`, indicating successful request processing without any content included in the response.

This endpoint is invoked by third-party apps when using SDK Wait for resume actions.

### # Payload

| Name | Type | Description |
| --- | --- | --- |
| token | **string**  
_required_ | The `resume_token` that matches the particular job you plan to resume. |
| data | **hash**  
_optional_ | Any contextual data you plan to pass back to the job. This data is accessible by the action in the `before_resume` lambda. The payload's limit is 50MB. For payloads larger than the limit, you can send a reference and allow the action’s `execute` lambda to make a secondary request to retrieve the data. |

#### # Sample request