# Relationship Query Patterns

## Child-to-Parent (Dot Notation)

Access parent record fields from a child record.

### Standard Relationships

```sql
-- Contact → Account
SELECT Id, FirstName, LastName, Account.Name, Account.Industry
FROM Contact

-- Opportunity → Account
SELECT Id, Name, Amount, Account.Name, Account.BillingCity
FROM Opportunity

-- Case → Account and Contact
SELECT Id, CaseNumber, Account.Name, Contact.Email
FROM Case
```

### Multi-Level Traversal (up to 5 levels)

```sql
-- Contact → Account → Parent Account
SELECT Id, Name, Account.Name, Account.Parent.Name
FROM Contact

-- OpportunityLineItem → Opportunity → Account
SELECT Id, Name, Opportunity.Name, Opportunity.Account.Name
FROM OpportunityLineItem
```

### Custom Relationships

```sql
-- Replace __c with __r
SELECT Id, Name, Custom_Account__r.Name
FROM Custom_Object__c

SELECT Id, Name, Related_Object__r.Field__c
FROM Another_Object__c
```

## Parent-to-Child (Subquery)

Get child records along with the parent.

### Standard Relationships

```sql
-- Account with Contacts
SELECT Id, Name,
  (SELECT Id, FirstName, LastName, Email FROM Contacts)
FROM Account

-- Account with Opportunities
SELECT Id, Name,
  (SELECT Id, Name, Amount, StageName FROM Opportunities)
FROM Account

-- Account with multiple children
SELECT Id, Name,
  (SELECT Id, FirstName, LastName FROM Contacts LIMIT 5),
  (SELECT Id, Name, Amount FROM Opportunities WHERE IsClosed = false)
FROM Account
```

### Filter Child Records

```sql
-- Only active contacts
SELECT Id, Name,
  (SELECT Id, Name, Email FROM Contacts WHERE MailingCity = 'San Francisco')
FROM Account

-- Recent opportunities
SELECT Id, Name,
  (SELECT Id, Name, Amount FROM Opportunities
   WHERE CreatedDate >= LAST_N_DAYS:30
   ORDER BY Amount DESC
   LIMIT 5)
FROM Account
```

### Order and Limit Child Records

```sql
SELECT Id, Name,
  (SELECT Id, Subject, ActivityDate FROM OpenActivities ORDER BY ActivityDate ASC LIMIT 3),
  (SELECT Id, Subject, ActivityDate FROM ActivityHistories ORDER BY ActivityDate DESC LIMIT 5)
FROM Account WHERE Id = '001xxx'
```

## Semi-Join (IN with Subquery)

Find records that have related records meeting criteria.

```sql
-- Accounts with closed won opportunities
SELECT Id, Name FROM Account
WHERE Id IN (SELECT AccountId FROM Opportunity WHERE IsWon = true)

-- Contacts at accounts in Technology industry
SELECT Id, FirstName, LastName, Email FROM Contact
WHERE AccountId IN (SELECT Id FROM Account WHERE Industry = 'Technology')

-- Leads that were converted
SELECT Id, Name, Email FROM Lead
WHERE IsConverted = true
  AND ConvertedAccountId IN (SELECT Id FROM Account WHERE Type = 'Customer')
```

## Anti-Join (NOT IN with Subquery)

Find records that don't have related records.

```sql
-- Accounts without any contacts
SELECT Id, Name FROM Account
WHERE Id NOT IN (SELECT AccountId FROM Contact WHERE AccountId <> null)

-- Accounts without open opportunities
SELECT Id, Name FROM Account
WHERE Id NOT IN (SELECT AccountId FROM Opportunity WHERE IsClosed = false)

-- Contacts not on any open cases
SELECT Id, FirstName, LastName FROM Contact
WHERE Id NOT IN (SELECT ContactId FROM Case WHERE IsClosed = false AND ContactId <> null)
```

## Polymorphic Relationships

Handle fields that can reference multiple object types.

### Task/Event WhoId and WhatId

```sql
-- Filter by related object type
SELECT Id, Subject, Who.Name FROM Task WHERE Who.Type = 'Contact'
SELECT Id, Subject, What.Name FROM Task WHERE What.Type = 'Opportunity'

-- Get type information
SELECT Id, Subject, Who.Type, What.Type FROM Task
```

### Using TYPEOF

```sql
SELECT Id, Subject,
  TYPEOF Who
    WHEN Contact THEN FirstName, LastName, Account.Name
    WHEN Lead THEN FirstName, LastName, Company
  END
FROM Task
WHERE Who.Type IN ('Contact', 'Lead')
```

## Common Patterns

### Find Orphan Records

```sql
-- Contacts without accounts
SELECT Id, Name, Email FROM Contact WHERE AccountId = null

-- Opportunities without products
SELECT Id, Name FROM Opportunity
WHERE Id NOT IN (SELECT OpportunityId FROM OpportunityLineItem)
```

### Find Duplicate Related Records

```sql
-- Accounts with multiple primary contacts
SELECT AccountId, COUNT(Id) FROM Contact
WHERE IsPrimary__c = true
GROUP BY AccountId
HAVING COUNT(Id) > 1
```

### Get Full Hierarchy

```sql
-- Account with parent chain (up to 5 levels)
SELECT Id, Name,
  Parent.Name,
  Parent.Parent.Name,
  Parent.Parent.Parent.Name
FROM Account WHERE Id = '001xxx'
```
