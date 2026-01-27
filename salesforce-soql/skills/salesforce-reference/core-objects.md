# Core Salesforce Objects

## Account

The Account object represents a company, organization, or person.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Account ID | id | Primary key |
| Name | Account Name | string | Required |
| Type | Type | picklist | Customer, Partner, Prospect, etc. |
| Industry | Industry | picklist | |
| AnnualRevenue | Annual Revenue | currency | |
| NumberOfEmployees | Employees | int | |
| Website | Website | url | |
| Phone | Phone | phone | |
| BillingStreet | Billing Street | textarea | |
| BillingCity | Billing City | string | |
| BillingState | Billing State/Province | string | |
| BillingPostalCode | Billing Zip/Postal Code | string | |
| BillingCountry | Billing Country | string | |
| ShippingStreet | Shipping Street | textarea | |
| ShippingCity | Shipping City | string | |
| OwnerId | Owner | reference | User |
| ParentId | Parent Account | reference | Account (self-reference) |

### Relationships

| Relationship | Type | Related Object |
|--------------|------|----------------|
| Contacts | Child | Contact |
| Opportunities | Child | Opportunity |
| Cases | Child | Case |
| Contracts | Child | Contract |
| Parent | Parent | Account |

---

## Contact

The Contact object represents a person associated with an Account.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Contact ID | id | Primary key |
| FirstName | First Name | string | |
| LastName | Last Name | string | Required |
| Name | Full Name | string | Computed (FirstName + LastName) |
| Email | Email | email | |
| Phone | Phone | phone | |
| MobilePhone | Mobile | phone | |
| Title | Title | string | Job title |
| Department | Department | string | |
| AccountId | Account | reference | Account |
| ReportsToId | Reports To | reference | Contact (self-reference) |
| MailingStreet | Mailing Street | textarea | |
| MailingCity | Mailing City | string | |
| MailingState | Mailing State/Province | string | |
| MailingPostalCode | Mailing Zip/Postal Code | string | |
| MailingCountry | Mailing Country | string | |
| HasOptedOutOfEmail | Email Opt Out | boolean | |
| DoNotCall | Do Not Call | boolean | |

### Relationships

| Relationship | Type | Related Object |
|--------------|------|----------------|
| Account | Parent | Account |
| Cases | Child | Case |
| Opportunities | Child | Opportunity (via OpportunityContactRole) |
| ReportsTo | Parent | Contact |

---

## Opportunity

The Opportunity object represents a sales deal or revenue event.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Opportunity ID | id | Primary key |
| Name | Opportunity Name | string | Required |
| AccountId | Account | reference | Account |
| Amount | Amount | currency | |
| CloseDate | Close Date | date | Required |
| StageName | Stage | picklist | Required |
| Probability | Probability (%) | percent | Often auto-set by Stage |
| Type | Type | picklist | New Business, Existing, etc. |
| LeadSource | Lead Source | picklist | |
| NextStep | Next Step | string | |
| Description | Description | textarea | Long text - NOT filterable |
| IsClosed | Closed | boolean | Computed |
| IsWon | Won | boolean | Computed |
| ForecastCategory | Forecast Category | picklist | |
| ForecastCategoryName | Forecast Category | string | |
| CampaignId | Campaign | reference | Campaign |
| OwnerId | Owner | reference | User |
| RecordTypeId | Record Type | reference | RecordType |

### Common Stage Values (Vary by Org)

Standard stages: Prospecting, Qualification, Needs Analysis, Value Proposition, Id. Decision Makers, Perception Analysis, Proposal/Price Quote, Negotiation/Review, Closed Won, Closed Lost

### Relationships

| Relationship | Type | Related Object |
|--------------|------|----------------|
| Account | Parent | Account |
| OpportunityLineItems | Child | OpportunityLineItem |
| OpportunityContactRoles | Child | OpportunityContactRole |

---

## Lead

The Lead object represents a prospect who has not yet been qualified.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Lead ID | id | Primary key |
| FirstName | First Name | string | |
| LastName | Last Name | string | Required |
| Name | Full Name | string | Computed |
| Email | Email | email | |
| Phone | Phone | phone | |
| MobilePhone | Mobile | phone | |
| Company | Company | string | Required |
| Title | Title | string | |
| Industry | Industry | picklist | |
| LeadSource | Lead Source | picklist | |
| Status | Status | picklist | Required |
| Rating | Rating | picklist | Hot, Warm, Cold |
| Street | Street | textarea | |
| City | City | string | |
| State | State/Province | string | |
| PostalCode | Zip/Postal Code | string | |
| Country | Country | string | |
| IsConverted | Converted | boolean | |
| ConvertedAccountId | Converted Account | reference | Account |
| ConvertedContactId | Converted Contact | reference | Contact |
| ConvertedOpportunityId | Converted Opportunity | reference | Opportunity |
| ConvertedDate | Converted Date | date | |

---

## Case

The Case object represents a customer issue or support request.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Case ID | id | Primary key |
| CaseNumber | Case Number | string | Auto-generated |
| Subject | Subject | string | |
| Description | Description | textarea | Long text - NOT filterable |
| Status | Status | picklist | |
| Priority | Priority | picklist | |
| Origin | Case Origin | picklist | Phone, Email, Web, etc. |
| Type | Type | picklist | |
| Reason | Case Reason | picklist | |
| AccountId | Account | reference | Account |
| ContactId | Contact | reference | Contact |
| OwnerId | Owner | reference | User or Queue |
| IsClosed | Closed | boolean | |
| ClosedDate | Closed Date | datetime | |

---

## Contract

The Contract object represents a business agreement (often used for subscriptions).

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Contract ID | id | Primary key |
| ContractNumber | Contract Number | string | Auto-generated |
| AccountId | Account | reference | Account |
| Status | Status | picklist | Draft, In Approval, Activated |
| StartDate | Start Date | date | |
| EndDate | End Date | date | Computed from StartDate + ContractTerm |
| ContractTerm | Contract Term (months) | int | |
| OwnerExpirationNotice | Owner Expiration Notice | picklist | |
| Description | Description | textarea | Long text - NOT filterable |
| CustomerSignedId | Customer Signed By | reference | Contact |
| CustomerSignedDate | Customer Signed Date | date | |
| CustomerSignedTitle | Customer Signed Title | string | |
| CompanySignedId | Company Signed By | reference | User |
| CompanySignedDate | Company Signed Date | date | |

### Relationships

| Relationship | Type | Related Object |
|--------------|------|----------------|
| Account | Parent | Account |
| CustomerSigned | Parent | Contact |
| CompanySigned | Parent | User |
