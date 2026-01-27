# Opportunity - Mural Production

## Overview

Opportunities in Mural track sales deals across multiple channels including direct sales and online/Stripe transactions.

## Record Types

| DeveloperName | Display Name | Description |
|---------------|--------------|-------------|
| Online | Online | Self-service Stripe transactions |
| New_Business | New Business | Direct sales new customers |
| Renewal | Renewal | Contract renewals |
| True_Up | Amendment | Contract amendments/true-ups |
| Consolidated_Business | Consolidated Business | Consolidated deals |
| Professional_Services | Professional Services | PS engagements |
| Luma_Netsuite_Opportunity | Luma Netsuite Opportunity | NetSuite integrated opportunities |

## Stage Names

**Important**: This org does NOT use standard `Closed Won`/`Closed Lost` stage names.

| StageName | Is Closed | Is Won | Notes |
|-----------|-----------|--------|-------|
| Won | Yes | Yes | Standard closed-won |
| Stripe Transact - Closed Won | Yes | Yes | Stripe online transactions |
| Lost | Yes | No | Standard closed-lost |
| Churned | Yes | No | Customer churned |
| Diagnose | No | No | Discovery stage |
| Evaluate | No | No | Evaluation stage |
| Propose | No | No | Proposal stage |
| Purchase | No | No | Pending purchase |
| Research | No | No | Research stage |
| Merged Opportunity | Yes | No | Merged into another opp |

### Query Closed Won Opportunities

```sql
SELECT Id, Name, Amount, CloseDate
FROM Opportunity
WHERE StageName = 'Won' OR StageName = 'Stripe Transact - Closed Won'
```

## Key Custom Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Forecast_Notes__c | Forecast Notes | Long Text | Contains Stripe Customer links - NOT FILTERABLE |
| Stripe_Customer_ID__c | Stripe Customer ID | Text | Direct Stripe Customer reference |
| Stripe_Subscription_Id__c | Stripe Subscription Id | Text | Direct Stripe Subscription reference |
| Sales_Channel__c | Sales Channel | Picklist | `Online`, `Sales-Assisted`, or null |

## Sales Channel Values

| Value | Description |
|-------|-------------|
| Online | Self-service/Stripe transactions |
| Sales-Assisted | Sales rep involved |
| (null) | Not specified |

## Relationships

| Field | Related Object | Relationship Name |
|-------|----------------|-------------------|
| AccountId | Account | Account |
| RecordTypeId | RecordType | RecordType |
| OwnerId | User | Owner |
| CampaignId | Campaign | Campaign |

## Common Queries

### Online Closed-Won Opportunities

```sql
SELECT Id, Name, AccountId, Account.Name, Forecast_Notes__c, CloseDate, Amount
FROM Opportunity
WHERE (StageName = 'Won' OR StageName = 'Stripe Transact - Closed Won')
  AND RecordType.DeveloperName = 'Online'
ORDER BY CloseDate DESC
```

### Opportunities by Sales Channel

```sql
SELECT Sales_Channel__c, COUNT(Id), SUM(Amount)
FROM Opportunity
WHERE (StageName = 'Won' OR StageName = 'Stripe Transact - Closed Won')
GROUP BY Sales_Channel__c
```

### Opportunities with Stripe Links

```sql
-- Note: Forecast_Notes__c cannot be filtered with LIKE
-- Query all and filter client-side for stripe.com links
SELECT Id, Name, Forecast_Notes__c, Account.Name
FROM Opportunity
WHERE RecordType.DeveloperName = 'Online'
  AND (StageName = 'Won' OR StageName = 'Stripe Transact - Closed Won')
```
