# Mural Production Org

## Org Information

| Property | Value |
|----------|-------|
| Org ID | 00D36000000HtfeEAC |
| Instance | production |
| Alias | production |
| Username | dkreitter@mural.co |

## Key Customizations

This org has significant customizations around:

1. **Online/Stripe Sales** - Opportunities and Contracts integrated with Stripe
2. **Revenue Cloud** - CPQ-style quoting with SBQQ
3. **Customer Success** - Gainsight (JBCXM) integration
4. **Data Enrichment** - ZoomInfo, LeanData

## Object Documentation

| Object | File | Description |
|--------|------|-------------|
| Opportunity | [opportunity.md](opportunity.md) | Custom stages, Stripe fields, record types |
| Contract | [contract.md](contract.md) | Stripe subscription sync fields |
| Account | [account.md](account.md) | Enrichment and rollup fields |
| Custom Objects | [custom-objects.md](custom-objects.md) | Overview of custom objects |

## Important Notes

### Stage Names
- Use `'Won'` or `'Stripe Transact - Closed Won'` instead of `'Closed Won'`
- Always verify with: `SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName`

### Record Types
- Online opportunities use `RecordType.DeveloperName = 'Online'`
- Not to be confused with `Sales_Channel__c = 'Online'`

### Stripe Integration
- Contracts represent Stripe Subscriptions
- Use `Stripe_Customer_Id__c` and `Stripe_Subscription_Id__c` to match
- Forecast_Notes__c on Opportunity may contain Stripe Customer links

## Connected Integrations

| System | Purpose |
|--------|---------|
| Stripe | Payment processing, subscription management |
| NetSuite | ERP, financial sync |
| Workato | Integration platform |
| Gainsight | Customer success |
| ZoomInfo | Data enrichment |
| LeanData | Lead routing |
