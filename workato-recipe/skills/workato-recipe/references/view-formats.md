# View File Formats

The `extract_views.py` script distills Workato recipes into two focused views to provide maximum comprehension while eliminating 90%+ of the UI/schema token bloat.

All view files use **block numbers** as the primary cross-reference key.
A block number is consistent across all views — block 42 in `summary.json` is the same block 42 in `unified_logic.md`.

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

## unified_logic.md

The complete logic of the recipe, presented as a top-down, hierarchical flow. This single file combines the control flow structure, condition statements, variable mutations, and field mappings into one cohesive document.

### Structural Example

```markdown
# Unified Logic

Block 0 (TRIGGER) is the root at depth 0. The explicit [depth=... parent=...] metadata is authoritative.

0: TRIGGER databricks.new_rows_sql_batch [depth=0 parent=root]
  [Inputs]:
    - **sql**:
      ```
      SELECT * FROM ...
      ```
1: TRY [depth=1 parent=block_0]
  2: ACTION workato_variable.declare_variable [depth=2 parent=block_1]
    -> DECLARES:
      - determined_account_id = ``
  3: ACTION salesforce.search_sobjects [depth=2 parent=block_1]
    // Check Salesforce for a Contract with the matching Stripe Subscription ID.
    [Inputs]:
      - **limit**: `150`
      - **Stripe_Subscription_Id__c**: `[block_0:databricks.rows.[*].id]`
  4: IF [depth=2 parent=block_1]
    [AND]:
      1. `[block_2:workato_variable.determined_account_id]` **BLANK**
      2. `[block_3:salesforce.Contract.[*].AccountId]` **PRESENT**
    -> True branch blocks: 5
    -> Fallthrough next block: 6
    5: ACTION workato_variable.update_variables [depth=3 parent=block_4]
      -> MUTATES [determined_account_id]:
        - determined_account_id = `[block_3:salesforce.Contract.[*].AccountId]`
  93: CATCH [depth=2 parent=block_1]
    Retry: 3x @ 10s
    94: ACTION workato_db_table.upsert_record [depth=3 parent=block_93]
```

### Format Highlights
- **Headers:** `N: KEYWORD [provider.action] [depth=D parent=P]`. Explicit depth and parent markers are authoritative.
- **Conditions (`IF`/`ELSIF`/`WHILE`/`CATCH`):** Rendered explicitly with compound operators (`[AND]:`, `[OR]:`) and numbered lists of conditions.
- **Branch Annotations:** Explicit tracking of control flow resolving `IF`/`ELSIF` blocks (e.g., `-> True branch blocks: 5`, `-> Else/ELSIF branch blocks: ...`, `-> Fallthrough next block: 6`).
- **State Mutations:** Explicit markers for variable and list modifications (e.g., `-> DECLARES:`, `-> MUTATES [target]:`).
- **Loops (`FOREACH`/`REPEAT`):** Explicitly lists `Source`, `Repeat Mode`, and `Batch Size` where applicable.
- **Datapills:** Rendered cleanly (e.g., `[block_3:salesforce.Contract.[*].AccountId]`) instead of raw `_dp()` JSON, allowing you to easily trace data lineage back to its source block.
- **Skipped Blocks:** Prefixed with `[SKIPPED]`.
- **Comments:** Developer comments are prefixed with `//`.