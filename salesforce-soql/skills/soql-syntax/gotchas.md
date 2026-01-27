# SOQL Gotchas and Common Issues

## Long Text Fields Cannot Be Filtered

**Problem**: Fields of type `Long Text Area` (like `Description`, `Body`, or custom long text) cannot use `LIKE`, `=`, or any comparison in WHERE clauses.

**Error**: `field 'Description' can not be filtered in a query call`

**Solution**: Query all records and filter client-side, or use a different field.

```sql
-- This FAILS:
SELECT Id, Name FROM Case WHERE Description LIKE '%error%'

-- This WORKS (filter in code after query):
SELECT Id, Name, Description FROM Case
```

**Affected Standard Fields**:
- Account.Description
- Contact.Description
- Opportunity.Description
- Case.Description
- Lead.Description
- Task.Description
- Event.Description
- And most `__c` fields of type Long Text Area

---

## Shell Escaping with != Operator

**Problem**: When running queries via CLI, the `!` character may be escaped by the shell.

**Error**: `unexpected token: '\'`

**Solution**: Use `<>` instead of `!=`:

```sql
-- This may FAIL in CLI:
WHERE AccountId != null

-- This WORKS:
WHERE AccountId <> null
```

---

## Stage Names Vary by Org

**Problem**: Assuming standard stage names like `Closed Won` when orgs often customize them.

**Solution**: Always check actual values first:

```sql
SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName
```

Common variations:
- `Closed Won` vs `Won` vs `Closed - Won`
- `Closed Lost` vs `Lost` vs `Closed - Lost`
- Custom stages like `Stripe Transact - Closed Won`

---

## Record Type Filtering

**Problem**: Filtering by record type name vs developer name.

**Solution**: Use `DeveloperName` for stability (names can change):

```sql
-- Recommended (stable):
WHERE RecordType.DeveloperName = 'Customer_Account'

-- Less stable (can change):
WHERE RecordType.Name = 'Customer Account'
```

---

## Null vs Empty String

**Problem**: Null and empty string `''` are different in Salesforce.

**Solution**: Check for both if needed:

```sql
-- Only null
WHERE Email = null

-- Only empty string
WHERE Email = ''

-- Both
WHERE (Email = null OR Email = '')
```

---

## Date vs DateTime

**Problem**: Using wrong format for date vs datetime fields.

**Solution**: Check field type and use correct format:

```sql
-- Date field (CloseDate)
WHERE CloseDate = 2024-06-15
WHERE CloseDate >= 2024-01-01

-- DateTime field (CreatedDate)
WHERE CreatedDate >= 2024-01-01T00:00:00Z
WHERE CreatedDate < 2024-12-31T23:59:59.999Z
```

---

## Relationship Field Names

**Problem**: Using wrong relationship name in queries.

**Common Mistakes**:

```sql
-- WRONG: Using field name with Id
SELECT AccountId.Name FROM Contact

-- CORRECT: Remove 'Id' for standard relationships
SELECT Account.Name FROM Contact

-- WRONG: Using __c for custom relationship
SELECT Custom_Lookup__c.Name FROM Custom_Object__c

-- CORRECT: Replace __c with __r
SELECT Custom_Lookup__r.Name FROM Custom_Object__c
```

---

## Subquery Limitations

**Problem**: Complex subqueries fail.

**Limitations**:
- Only ONE level of nesting allowed
- Cannot reference parent query fields in subquery
- Subquery must return less than 50,000 records

```sql
-- FAILS: Nested subqueries
WHERE Id IN (SELECT AccountId FROM Opportunity
  WHERE Id IN (SELECT OpportunityId FROM OpportunityLineItem))

-- WORKS: Flatten the logic
WHERE Id IN (SELECT AccountId FROM Opportunity WHERE HasOpportunityLineItem = true)
```

---

## ORDER BY with Null Values

**Problem**: Nulls sort first by default, which may not be desired.

**Solution**: Use `NULLS LAST`:

```sql
ORDER BY CloseDate DESC NULLS LAST
ORDER BY Amount ASC NULLS FIRST
```

---

## Query Limits

| Limit | Value |
|-------|-------|
| Max records returned | 50,000 |
| Max characters in query | 100,000 |
| Max fields in SELECT | 200 |
| Max child relationships | 20 |
| Max relationship depth (up) | 5 levels |
| Max relationship depth (down) | 1 level |

**For large exports**: Use `sf data export bulk` instead of `sf data query`.

---

## Formula Fields in Queries

**Problem**: Some formula field behaviors surprise users.

**Notes**:
- Formula fields CAN be filtered in WHERE (unlike long text)
- Formula fields return calculated values, not stored values
- Cross-object formula fields may hit relationship limits

---

## Polymorphic Field Queries

**Problem**: Querying fields from polymorphic relationships (like Task.WhoId).

**Solution**: Use `TYPEOF` or filter by type:

```sql
-- Filter by type
SELECT Id, Subject FROM Task WHERE Who.Type = 'Contact'

-- Or use TYPEOF for type-specific fields
SELECT Id, Subject,
  TYPEOF Who
    WHEN Contact THEN FirstName, LastName
    WHEN Lead THEN FirstName, LastName, Company
  END
FROM Task
```
