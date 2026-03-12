# View File Formats

All view files use **block numbers** as the primary cross-reference key.
A block number is consistent across all views — block 42 in `skeleton.md`
is the same block 42 in `mappings.md`, `conditions.md`, etc.

## summary.json

Recipe-level metadata. Read this first for orientation.

```json
{
  "name": "recipe display name",
  "version": 24,
  "version_comment": "optional — only present on ~3/142 recipes",
  "trigger": {
    "provider": "databricks",
    "action": "new_rows_sql_batch",
    "key_inputs": { "sql": "SELECT ...", "batch_size": "1" }
  },
  "connections": [
    { "provider": "salesforce", "connection": "[STR] CON | Salesforce PROD (REST)" }
  ],
  "statistics": {
    "total_blocks": 95,
    "max_depth": 12,
    "by_keyword": { "action": 44, "if": 30, "try": 5, ... },
    "by_provider": { "salesforce": 21, "workato_variable": 16, ... }
  },
  "project_properties": ["house_accounts", "public_email_domains"],
  "callable": { /* only for callable function recipes */ }
}
```

## skeleton.md

One line per block, indented by depth (2 spaces per level). Provides the
complete control flow structure at a glance.

```
0: TRIGGER databricks.new_rows_sql_batch
  1: TRY
    2: ACTION workato_variable.declare_variable
    3: ACTION salesforce.search_sobjects  — "Check for Contract with Stripe Sub ID"
    4: IF [block_2:workato_variable.determined_account_id] BLANK AND ...
      5: ACTION workato_variable.update_variables
    93: CATCH retry: 3x @ 10s
      94: ACTION workato_db_table.upsert_record
```

Format:
- `N: KEYWORD [provider.name]` — block number, keyword (uppercased), optional action
- `IF`/`ELSIF` — inline condition (truncated to ~120 chars)
- `FOREACH` — source datapill + repeat_mode/batch_size
- `CATCH` — retry settings if non-zero
- `STOP [error]` or `STOP [success]` — with rendered reason
- `[SKIPPED]` suffix for disabled blocks
- `— "comment"` suffix for blocks with human comments

## mappings.md

Field-to-value mappings per action block. Only blocks with non-empty input.

Sections separated by `---`. Each section header: `## Block N: provider.name`

Content varies by action type:
- **declare_variable**: table of variable names, types, initial values
- **declare_list**: name, source datapill, field mappings
- **update_variables**: target variable name + new value
- **call_recipe**: recipe reference + parameter mappings
- **Generic actions**: field→rendered value pairs

Datapill references are rendered: `[block_N:provider.path]` instead of raw `_dp()` JSON.

## conditions.md

Detailed condition breakdown for `if`, `elsif`, `while_condition`, and `catch` (with filter) blocks.

```markdown
## Block 4: IF

**Compound operator:** AND

1. `[block_2:workato_variable.determined_account_id]` **BLANK**
2. `[block_3:salesforce.Contract.[*].AccountId]` **PRESENT**
3. `=[project:house_accounts].match?([block_3:...AccountId])` **IS_NOT_TRUE**

→ First child: block 5 (action workato_variable.update_variables)
```

## variables.md

### Declarations section
Table: variable name, type, initial value, declaring block number.
Includes both `declare_variable` (scalar) and `declare_list` entries.

### Updates section
Grouped by variable name. Each entry: block number + rendered new value.

## errors.md

### Try/Catch pairs
- Try block number and matching catch block number
- Retry settings (count × interval)
- Catch filter conditions (if any)
- Catch actions or `[empty — error suppressed]`

### Stop blocks
- Block number with `[ERROR]` or `[SUCCESS]` status
- Rendered stop reason

## Cross-Referencing Strategy

1. Start with `skeleton.md` to identify the relevant section of the recipe
2. Note block numbers of interest
3. Look up those block numbers in the relevant detail view:
   - Data flow question → `mappings.md`
   - Branching logic → `conditions.md`
   - Variable state → `variables.md`
   - Error handling → `errors.md`
4. Rendered datapill references (e.g., `[block_3:salesforce.Contract.[*].AccountId]`)
   tell you which upstream block produces the data — trace backward through the skeleton
