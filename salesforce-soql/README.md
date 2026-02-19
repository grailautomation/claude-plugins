# Salesforce SOQL Plugin for Claude Code

Run SOQL queries against Salesforce orgs using the `sf` CLI directly from Claude Code.

## Features

- **Query Execution**: Run SOQL queries with `/query`
- **Schema Discovery**: Describe objects with `/describe`
- **Object Reference**: Built-in documentation for standard Salesforce objects
- **SOQL Syntax Guide**: Complete reference for SOQL clauses and functions
- **Query Patterns**: Common query patterns and examples
- **Bulk Write Operations**: Import, update, upsert, and delete records via Bulk API 2.0
- **Org-Specific Schemas**: Add custom object documentation per org

## Prerequisites

- Salesforce CLI (`sf`) installed: `npm install -g @salesforce/cli`
- At least one authenticated Salesforce org: `sf org login web`

## Quick Start

```bash
# List connected orgs
sf org list

# Run a query
/query SELECT Id, Name FROM Account LIMIT 10

# Describe an object
/describe Account
```

## Commands

| Command | Description |
|---------|-------------|
| `/query <SOQL>` | Execute a SOQL query |
| `/describe <Object>` | Get object schema and fields |
| `/explore-schema` | Interactive schema exploration |

## Skills (Auto-Invoked)

| Skill | Purpose |
|-------|---------|
| `salesforce-reference` | Object and field reference |
| `soql-syntax` | SOQL language syntax |
| `query-patterns` | Common query patterns |
| `sf-cli-execution` | CLI execution and authentication |
| `sf-bulk-operations` | Bulk API 2.0 write operations |

## Adding Org-Specific Schemas

Create a folder under `org-schemas/` for your org:

```
org-schemas/
└── my-org/
    ├── manifest.md      # Org metadata
    ├── custom-obj.md    # Custom object docs
    └── ...
```

See `org-schemas/example-org/` for an example.

## Directory Structure

```
salesforce-soql/
├── .claude-plugin/plugin.json
├── commands/
│   ├── query.md
│   ├── describe.md
│   └── explore-schema.md
├── skills/
│   ├── salesforce-reference/
│   ├── soql-syntax/
│   ├── query-patterns/
│   ├── sf-cli-execution/
│   └── sf-bulk-operations/
├── org-schemas/
│   └── example-org/
└── README.md
```
