# Basic Query Patterns

## Select All Fields You Need

```sql
-- Specific fields (recommended)
SELECT Id, Name, Industry, Type, AnnualRevenue FROM Account

-- Never use SELECT * - it doesn't exist in SOQL
```

## Filter by Field Values

### Text Fields

```sql
-- Exact match
SELECT Id, Name FROM Account WHERE Name = 'Acme Corporation'

-- Pattern match
SELECT Id, Name FROM Account WHERE Name LIKE 'Acme%'
SELECT Id, Name FROM Account WHERE Name LIKE '%Corp%'

-- Multiple values
SELECT Id, Name FROM Account WHERE Type IN ('Customer', 'Partner', 'Prospect')
```

### Numeric Fields

```sql
SELECT Id, Name, AnnualRevenue FROM Account WHERE AnnualRevenue > 1000000
SELECT Id, Name, Amount FROM Opportunity WHERE Amount >= 10000 AND Amount <= 100000
```

### Boolean Fields

```sql
SELECT Id, Name FROM Opportunity WHERE IsClosed = true
SELECT Id, Name FROM Contact WHERE HasOptedOutOfEmail = false
```

### Null Checks

```sql
-- Has value
SELECT Id, Name FROM Contact WHERE Email <> null

-- No value
SELECT Id, Name FROM Account WHERE Website = null
```

## Sort Results

```sql
-- Ascending (default)
SELECT Id, Name FROM Account ORDER BY Name

-- Descending
SELECT Id, Name, AnnualRevenue FROM Account ORDER BY AnnualRevenue DESC

-- Multiple fields
SELECT Id, Name FROM Contact ORDER BY LastName, FirstName

-- Handle nulls
SELECT Id, Name, CloseDate FROM Opportunity ORDER BY CloseDate DESC NULLS LAST
```

## Limit Results

```sql
-- First N records
SELECT Id, Name FROM Account ORDER BY CreatedDate DESC LIMIT 10

-- Pagination
SELECT Id, Name FROM Account ORDER BY Name LIMIT 25 OFFSET 50
```

## Combine Conditions

```sql
-- AND
SELECT Id, Name FROM Account
WHERE Industry = 'Technology' AND AnnualRevenue > 1000000

-- OR (use parentheses)
SELECT Id, Name FROM Opportunity
WHERE StageName = 'Closed Won' OR StageName = 'Closed Lost'

-- Complex
SELECT Id, Name FROM Account
WHERE (Type = 'Customer' OR Type = 'Partner')
  AND Industry = 'Technology'
  AND AnnualRevenue > 500000
```

## Find by ID

```sql
-- Single record
SELECT Id, Name FROM Account WHERE Id = '001xx000003DGbYAAW'

-- Multiple records
SELECT Id, Name FROM Account WHERE Id IN ('001xxx', '001yyy', '001zzz')
```

## Find by Owner

```sql
-- Specific owner
SELECT Id, Name FROM Account WHERE OwnerId = '005xxx'

-- Current user (use in Apex, not CLI)
-- SELECT Id, Name FROM Account WHERE OwnerId = :UserInfo.getUserId()
```

## Find by Record Type

```sql
SELECT Id, Name FROM Account WHERE RecordType.DeveloperName = 'Customer_Account'
SELECT Id, Name FROM Opportunity WHERE RecordType.Name = 'New Business'
```

## Find Recently Modified

```sql
SELECT Id, Name, LastModifiedDate FROM Account
WHERE LastModifiedDate >= LAST_N_DAYS:7
ORDER BY LastModifiedDate DESC

SELECT Id, Name FROM Lead
WHERE SystemModstamp >= 2024-01-01T00:00:00Z
```
