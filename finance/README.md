# Finance & Accounting Plugin

A finance and accounting plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Supports month-end close, journal entry preparation, account reconciliation, financial statement generation, variance analysis, and SOX audit support.

> **Important**: This plugin assists with finance and accounting workflows but does not provide financial, tax, or audit advice. All outputs should be reviewed by qualified financial professionals before use in financial reporting, regulatory filings, or audit documentation.

## Installation

```bash
claude plugin install finance@grail-automation
```

## Commands

| Command | Description |
|---------|-------------|
| `/finance:journal-entry` | Journal entry preparation — generate accruals, fixed asset entries, prepaids, payroll, and revenue entries with proper debits/credits and supporting detail |
| `/finance:reconciliation` | Account reconciliation — compare GL balances to subledger, bank, or third-party balances and identify reconciling items |
| `/finance:income-statement` | Income statement generation — produce P&L with period-over-period comparison and variance analysis |
| `/finance:variance-analysis` | Variance/flux analysis — decompose variances into drivers with narrative explanations and waterfall analysis |
| `/finance:sox-testing` | SOX compliance testing — generate sample selections, testing workpapers, and control assessments |

## Skills

| Skill | Description |
|-------|-------------|
| `journal-entry-prep` | JE preparation best practices, standard accrual types, supporting documentation requirements, and review workflows |
| `reconciliation` | Reconciliation methodology for GL-to-subledger, bank recs, and intercompany, with reconciling item categorization and aging |
| `financial-statements` | Income statement, balance sheet, and cash flow statement formats with GAAP presentation and flux analysis methodology |
| `variance-analysis` | Variance decomposition techniques (price/volume, rate/mix), materiality thresholds, narrative generation, and waterfall charts |
| `close-management` | Month-end close checklist, task sequencing, dependencies, status tracking, and common close activities by day |
| `audit-support` | SOX 404 control testing methodology, sample selection, documentation standards, and deficiency classification |

## Example Workflows

### Month-End Close

1. Run `/finance:journal-entry ap-accrual 2024-12` to generate AP accrual entries
2. Run `/finance:journal-entry prepaid 2024-12` to amortize prepaid expenses
3. Run `/finance:journal-entry fixed-assets 2024-12` to book depreciation
4. Run `/finance:reconciliation cash 2024-12` to reconcile bank accounts
5. Run `/finance:reconciliation accounts-receivable 2024-12` to reconcile AR subledger
6. Run `/finance:income-statement monthly 2024-12` to generate the P&L with flux analysis

### Variance Analysis

1. Run `/finance:variance-analysis revenue 2024-Q4 vs 2024-Q3` to analyze revenue variances
2. Run `/finance:variance-analysis opex 2024-12 vs budget` to investigate operating expense variances
3. Review the waterfall analysis and provide context on unexplained variances

### SOX Testing

1. Run `/finance:sox-testing revenue-recognition 2024-Q4` to generate revenue control testing workpapers
2. Run `/finance:sox-testing procure-to-pay 2024-Q4` to test procurement controls
3. Review sample selections and document test results

## Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

This plugin works best when connected to your financial data sources. Use a
maintained CLI when it safely covers the workflow, and keep MCP for remaining
systems without a safe CLI path.

### ERP / Accounting System

Connect your ERP (e.g., NetSuite, SAP) MCP server to pull trial balances, subledger data, and journal entries automatically.

### Data Warehouse

Use BigQuery through the Google Cloud SDK `bq` CLI. Other warehouses such as
Snowflake or Databricks may use their own CLIs, user/project MCP settings, or
manual exports to query financial data, run variance analysis, and pull
historical comparisons.

For noninteractive local agent workflows, validate BigQuery with a dry run
before querying financial data:

```bash
GCP_SERVICE_ACCOUNT_OP_REF='op://<vault>/<item>/<field>' \
  ruby scripts/smoke_cli_integrations.rb --only bigquery
```

The smoke script reads a Google service-account JSON key from 1Password into a
mode `0600` temp file, runs `bq` with
`CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`, and deletes the temp file. Use
`GOOGLE_APPLICATION_CREDENTIALS` for ADC/client-library code, not as the primary
way to force `bq` to use the service account.

### Spreadsheets

Connect spreadsheet tools (e.g., Google Sheets, Excel) for workpaper generation, reconciliation templates, and financial model updates.

### Analytics / BI

Connect your BI platform (e.g., Tableau, Looker) to pull dashboards, KPIs, and trend data for variance explanations.

> **Note:** Connect ERP and data warehouse tooling to pull financial data
> automatically. Without these, you can paste data or upload files for analysis.

## Configuration

Add remaining data source MCP servers only when no safe maintained CLI exists.
The connector categories that enhance this plugin are:

- `erp-accounting` — ERP or accounting system for GL, subledger, and JE data
- `data-warehouse` — Data warehouse for financial queries and historical data
- `spreadsheets` — Spreadsheet tools for workpaper generation
- `analytics-bi` — BI tools for dashboards and KPI data
- `documents` — Document storage for policies, memos, and support
- `email` — Email for sending reports and requesting approvals
- `chat` — Team communication for close status updates and questions
