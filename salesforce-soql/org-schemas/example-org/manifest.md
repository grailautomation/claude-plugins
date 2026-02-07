# Example Production Org

## Org Information

| Property | Value |
|----------|-------|
| Org ID | 00D000000000000AAA |
| Instance | production |
| Alias | production |
| Username | admin@example-corp.com |

## Key Customizations

1. **E-Commerce Integration** - Opportunities and Contracts integrated with payment provider
2. **Customer Success** - CSM platform integration

## Object Documentation

| Object | File | Description |
|--------|------|-------------|
| Opportunity | opportunity.md | Custom stages, payment fields, record types |
| Account | account.md | Enrichment and rollup fields |

## Important Notes

### Stage Names
- Verify stage names with: `SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName`

### Record Types
- Use `RecordType.DeveloperName` for reliable filtering
