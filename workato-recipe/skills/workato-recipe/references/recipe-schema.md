# Workato Recipe JSON Schema

## Top-Level Structure

```json
{
  "name": "[STR] REC 001 | Stripe-to-Salesforce Customer Sync",
  "description": "",
  "version": 24,
  "version_comment": "optional — absent from most recipes",
  "private": true,
  "concurrency": 1,
  "code": { /* root trigger block */ },
  "config": [ /* connection configs */ ]
}
```

## Root Trigger Block (`code`)

The `code` object IS the trigger block (block 0). It has `keyword: "trigger"` and contains the
recipe's block tree in its `block[]` array.

Key fields:
- `number`: 0 (always)
- `provider`: e.g., `"databricks"`, `"clock"`, `"workato_recipe_function"`
- `name`: trigger action, e.g., `"new_rows_sql_batch"`, `"scheduled_event"`, `"execute"`
- `as`: hex ID for datapill references
- `keyword`: `"trigger"`
- `input`: trigger configuration (SQL query, schedule, callable params)
- `block[]`: child blocks (the recipe body)

## Child Block Keywords (10 types)

| Keyword | Provider | Key Fields |
|---------|----------|------------|
| `action` | yes | Standard action block |
| `if` | no | Condition in `input.type`/`input.operand`/`input.conditions[]` |
| `elsif` | no | Same condition structure as `if` |
| `else` | no | No condition — fallback branch |
| `try` | no | Error boundary — followed by `catch` sibling |
| `catch` | no | Block-level `filter`, `input.max_retry_count`/`retry_interval` |
| `stop` | no | `input.stop_with_error`, `input.stop_reason` |
| `foreach` | no | Block-level `source`, `repeat_mode`, `batch_size`, `clear_scope` |
| `repeat` | no | Loop without explicit source (exit via `stop` or `while_condition`) |
| `while_condition` | no | Condition in `input` (same structure as `if`) — loop exit test |

## Block Node Structure

```json
{
  "number": 5,
  "provider": "workato_variable",
  "name": "update_variables",
  "as": "47723810",
  "keyword": "action",
  "comment": "optional human note",
  "skip": false,
  "input": { /* action-specific */ },
  "block": [ /* children */ ],

  // Bloat keys (stripped by extractor):
  "toggleCfg": {},
  "dynamicPickListSelection": {},
  "visible_config_fields": {},
  "extended_output_schema": [],
  "extended_input_schema": [],
  "uuid": "..."
}
```

## Condition Structure (if/elsif/while_condition)

Conditions live inside `input`, not as a top-level key:

```json
{
  "keyword": "if",
  "input": {
    "type": "compound",
    "operand": "and",
    "conditions": [
      {
        "operand": "blank",
        "lhs": "#{_dp('{...}')}",
        "rhs": "",
        "uuid": "..."
      }
    ]
  }
}
```

Common operands: `blank`, `present`, `equals_to`, `not_equals_to`, `contains`,
`not_contains`, `less_than`, `greater_than`, `is_true`, `is_not_true`, `match?`

## Catch Block Structure

```json
{
  "keyword": "catch",
  "as": "8f1dbe23",
  "input": {
    "max_retry_count": "3",
    "retry_interval": "10"
  },
  "filter": {
    "type": "compound",
    "operand": "and",
    "conditions": [...]
  },
  "block": []
}
```

- Retry settings are in `input`
- Error filter is a block-level `filter` key (NOT inside `input`)
- Empty `block[]` = error is suppressed silently

## Foreach Block Structure

```json
{
  "keyword": "foreach",
  "as": "02c53689",
  "source": "#{_dp('{...}')}",
  "repeat_mode": "batch",
  "batch_size": "10000",
  "clear_scope": "true",
  "input": {},
  "block": [...]
}
```

- `source`, `repeat_mode`, `batch_size`, `clear_scope` are all block-level (NOT in `input`)
- `input` is typically empty for foreach blocks

## Config (Connections)

```json
{
  "config": [
    {
      "keyword": "application",
      "provider": "salesforce",
      "skip_validation": false,
      "account_id": {
        "zip_name": "...",
        "name": "[STR] CON | Salesforce PROD (REST)",
        "folder": "..."
      }
    }
  ]
}
```

- `provider` is the identifier (not `name`, which doesn't exist on config items)
- `account_id` can be `null` (built-in providers) or an object with connection details

## Datapill Syntax

### Interpolation mode
```
"#{_dp('{\"pill_type\":\"output\",\"provider\":\"salesforce\",\"line\":\"a74dcce4\",\"path\":[\"Contract\",{\"path_element_type\":\"current_item\"},\"AccountId\"]}')}"
```

### Formula mode
```
"=_dp('{...}').method_chain()"
```

### Pill Types

| Type | Rendered As | Example |
|------|-------------|---------|
| `output` | `[block_N:provider.path]` | `[block_3:salesforce.Contract.[*].AccountId]` |
| `project_property` | `[project:name]` | `[project:house_accounts]` |
| `job_context` | `[job:path]` | `[job:started_at]` |
| `account_property` | `[account:name]` | `[account:company_name]` |
| `foreach_meta` | `[foreach_N:key]` | `[foreach_7:is_first]` |

### Path Elements

- String elements: joined with `.` (e.g., `Contract.AccountId`)
- `{"path_element_type": "current_item"}` → `[*]` (array iteration context)

### Unresolved References

When the datapill `line` (hex ID) doesn't match any block in the current recipe
(e.g., references a different recipe or callable function), rendered as `[?:provider.path]`.

## Variable Patterns

### declare_variable
- `input.variables.schema`: JSON string with variable definitions
- `input.variables.data`: initial values keyed by variable name

### declare_list
- `input.name`: list name
- `input.list_items.____source`: source datapill (quad underscore)
- `input.list_items.*`: field mappings

### update_variables
- `input.name`: `{uuid}:{as_id}:{field_name}` — last segment is the variable name
- Remaining `input` keys are the values being set

## Callable Recipe Patterns

### Trigger
Provider `workato_recipe_function`, action `execute`:
- `input.parameters_schema_json`: JSON string defining input parameters
- `input.result_schema_json`: JSON string defining return values

### Recipe Call
Provider `workato_recipe_function`, action `call_recipe`:
- `input.flow_id`: `{zip_name, name, folder}` object or numeric string
- `input.parameters`: key-value parameter map
