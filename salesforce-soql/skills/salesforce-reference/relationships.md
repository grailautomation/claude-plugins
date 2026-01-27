# Salesforce Object Relationships

## Relationship Diagram

```
                    ┌─────────────┐
                    │   Account   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │   Contact   │   │ Opportunity │   │    Case     │
  └──────┬──────┘   └──────┬──────┘   └─────────────┘
         │                 │
         │                 ▼
         │          ┌─────────────┐
         │          │  Contract   │
         │          └─────────────┘
         │
         ▼
  ┌─────────────┐
  │    Lead     │ (converts to Account + Contact + Opportunity)
  └─────────────┘
```

## Relationship Types

### Lookup Relationships
- One-to-many relationship
- Child record can exist without parent
- Deleting parent does NOT delete children

### Master-Detail Relationships
- One-to-many relationship
- Child record CANNOT exist without parent
- Deleting parent DELETES all children
- Roll-up summary fields available

## Querying Relationships

### Child-to-Parent (Dot Notation)

Access parent fields using the relationship name:

```sql
-- Standard relationship (remove 'Id' from field name)
SELECT Id, Name, Account.Name, Account.Industry
FROM Contact

-- Custom relationship (replace __c with __r)
SELECT Id, Name, Custom_Lookup__r.Name
FROM Custom_Object__c
```

### Parent-to-Child (Subquery)

Access child records using a subquery:

```sql
-- Standard relationship
SELECT Id, Name,
  (SELECT Id, FirstName, LastName, Email FROM Contacts)
FROM Account

-- Custom relationship (use relationship name from schema)
SELECT Id, Name,
  (SELECT Id, Name FROM Child_Objects__r)
FROM Parent_Object__c
```

## Common Relationship Names

### Account Relationships

| Related Object | Relationship Name | Direction |
|---------------|-------------------|-----------|
| Contact | Contacts | Parent → Child |
| Opportunity | Opportunities | Parent → Child |
| Case | Cases | Parent → Child |
| Contract | Contracts | Parent → Child |
| Account (self) | ChildAccounts | Parent → Child |
| Account (self) | Parent | Child → Parent |

### Contact Relationships

| Related Object | Relationship Name | Direction |
|---------------|-------------------|-----------|
| Account | Account | Child → Parent |
| Case | Cases | Parent → Child |
| Contact (self) | ReportsTo | Child → Parent |

### Opportunity Relationships

| Related Object | Relationship Name | Direction |
|---------------|-------------------|-----------|
| Account | Account | Child → Parent |
| OpportunityLineItem | OpportunityLineItems | Parent → Child |
| OpportunityContactRole | OpportunityContactRoles | Parent → Child |

### Case Relationships

| Related Object | Relationship Name | Direction |
|---------------|-------------------|-----------|
| Account | Account | Child → Parent |
| Contact | Contact | Child → Parent |
| Case (self) | Parent | Child → Parent |
| Case (self) | Cases | Parent → Child |

## Multi-Level Relationships

You can traverse up to 5 levels in a single query:

```sql
-- 3 levels up
SELECT Id, Name, Account.Parent.Parent.Name
FROM Contact

-- Mix of parent and child
SELECT Id, Name,
  (SELECT Id, Contact.Account.Name FROM OpportunityContactRoles)
FROM Opportunity
```

## Polymorphic Relationships

Some fields can reference multiple object types:

### Task/Event WhoId and WhatId

```sql
-- Get the type of related record
SELECT Id, Subject, Who.Type, What.Type FROM Task

-- Filter by specific type using Type field
SELECT Id, Subject FROM Task WHERE Who.Type = 'Contact'
```

### Case Owner (User or Queue)

```sql
-- Owner can be User or Queue
SELECT Id, CaseNumber, Owner.Name, Owner.Type FROM Case
```
