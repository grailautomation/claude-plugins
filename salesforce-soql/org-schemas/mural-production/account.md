# Account - Mural Production

## Overview

Accounts represent companies/organizations that are customers, prospects, or partners of Mural.

## Record Types

Query to get current record types:
```sql
SELECT Id, DeveloperName, Name FROM RecordType WHERE SObjectType = 'Account'
```

## Key Custom Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Stripe_Customer_Id__c | Stripe Customer Id | Text | Primary Stripe customer ID |
| ZoomInfo_Company_ID__c | ZoomInfo Company ID | Text | ZoomInfo enrichment ID |
| Domain__c | Domain | Text | Company domain |
| ICP_Score__c | ICP Score | Number | Ideal Customer Profile score |
| Account_Tier__c | Account Tier | Picklist | Customer tier |
| Workspace_Count__c | Workspace Count | Number | Number of workspaces |
| Active_User_Count__c | Active User Count | Number | Number of active users |

## Type Values

| Value | Description |
|-------|-------------|
| Customer | Active paying customer |
| Prospect | Potential customer |
| Partner | Partner organization |
| Former Customer | Previously paying customer |

## Relationships

| Relationship Name | Related Object | Direction |
|-------------------|----------------|-----------|
| Contacts | Contact | Parent → Child |
| Opportunities | Opportunity | Parent → Child |
| Cases | Case | Parent → Child |
| Contracts | Contract | Parent → Child |
| Parent | Account | Child → Parent |
| ChildAccounts | Account | Parent → Child |

## Common Queries

### Accounts with Stripe Customer IDs

```sql
SELECT Id, Name, Stripe_Customer_Id__c, Type
FROM Account
WHERE Stripe_Customer_Id__c <> null
```

### Accounts with Active Subscriptions

```sql
SELECT Id, Name, Type FROM Account
WHERE Id IN (SELECT AccountId FROM Contract WHERE Status = 'Activated')
```

### Accounts by Tier

```sql
SELECT Account_Tier__c, COUNT(Id) FROM Account GROUP BY Account_Tier__c
```

### Account with Related Contacts and Opportunities

```sql
SELECT Id, Name, Type,
  (SELECT Id, FirstName, LastName, Email FROM Contacts LIMIT 5),
  (SELECT Id, Name, Amount, StageName FROM Opportunities WHERE IsClosed = false LIMIT 5)
FROM Account
WHERE Id = '001xxxxx'
```

## Account Matching for Stripe Sync

The Stripe sync attempts to match accounts using:
1. Existing `Stripe_Customer_Id__c` on Account
2. Email domain matching
3. ZoomInfo enrichment for company lookup
4. Website domain matching

When no match is found, a new Account is created with `Name = 'team: workspacename'` pattern.
