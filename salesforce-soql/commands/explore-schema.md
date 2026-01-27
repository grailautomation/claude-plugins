---
description: Interactively explore the Salesforce schema - list objects, describe fields, understand relationships
allowed-tools: ["Bash", "AskUserQuestion"]
---

# Explore Salesforce Schema

Guide the user through exploring their Salesforce org's schema.

## Step 1: Identify Target Org

First, list available orgs:

```bash
sf org list
```

Ask the user which org to explore if multiple are available.

## Step 2: Determine Exploration Goal

Ask the user what they want to explore:
- List all custom objects
- Describe a specific object
- Find fields on an object
- Understand relationships between objects
- Find picklist values

## Step 3: Execute Exploration

### List All Custom Objects

```bash
sf org list metadata --metadata-type CustomObject --target-org <alias> --json
```

### List Standard Objects (Common Ones)

Standard objects don't appear in metadata list. Common ones include:
- Account, Contact, Lead, Opportunity, Case, Task, Event
- Contract, Order, Product2, Pricebook2, Quote
- Campaign, CampaignMember, User, Profile, PermissionSet

### Describe an Object

```bash
sf sobject describe --sobject <ObjectName> --target-org <alias> --json
```

### Find All Fields on an Object

```bash
sf sobject describe --sobject <ObjectName> --target-org <alias> --json 2>&1 | \
  grep -E '"name":|"label":|"type":' | paste - - - | head -50
```

### Find Relationships

```bash
sf sobject describe --sobject <ObjectName> --target-org <alias> --json 2>&1 | \
  grep -B2 -A2 '"type": "reference"'
```

### Get Record Types

```bash
sf data query --query "SELECT Id, DeveloperName, Name FROM RecordType WHERE SObjectType = '<ObjectName>'" \
  --target-org <alias> --json
```

### Get Picklist Values for a Field

```bash
sf data query --query "SELECT <FieldName>, COUNT(Id) FROM <ObjectName> GROUP BY <FieldName>" \
  --target-org <alias> --json
```

## Step 4: Document Findings

If the user wants to save this schema information for future use, suggest creating a file in `org-schemas/<org-name>/` with the object documentation.
