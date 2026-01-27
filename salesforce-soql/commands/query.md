---
description: Execute a SOQL query against a Salesforce org
allowed-tools: ["Bash", "Read"]
---

# Execute SOQL Query

Execute the following SOQL query: $ARGUMENTS

## Before Running

1. Use the `salesforce-reference` skill if you need to look up field names or relationships
2. Check `org-schemas/` for org-specific custom field names if targeting a known org
3. If no target org is specified, use `sf org list` to identify available orgs

## Execution Steps

1. **Validate the query syntax** using the `soql-syntax` skill if unsure
2. **Run the query** using the sf CLI:

```bash
sf data query --query "YOUR_QUERY_HERE" --target-org <alias> --json
```

3. **Handle large result sets**: If the query returns more than 10,000 records, use bulk export:

```bash
sf data export bulk --query "YOUR_QUERY" --output-file results.csv --wait 10 --target-org <alias>
```

## Output Handling

- Use `--json` for programmatic parsing
- Parse `result.records` from the JSON response
- Use `| head -N` to limit output for very large results

## Common Issues

- **Long text fields cannot be filtered**: Fields like `Description` or custom long text areas cannot use LIKE or = in WHERE clauses. Query all records and filter client-side.
- **Shell escaping**: Use `<>` instead of `!=` for null comparisons (shell may escape `!`)
- **Stage names vary**: Don't assume `Closed Won` - verify actual picklist values with a GROUP BY query first
