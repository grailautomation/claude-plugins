# python-quickbooks Plugin

Comprehensive reference plugin for the [python-quickbooks](https://github.com/ej2/python-quickbooks) library — QuickBooks Online API integration in Python.

## What This Plugin Provides

A single skill (`python-quickbooks`) with 13 detailed reference files covering:

- Authentication and client setup
- Querying, filtering, and pagination
- CRUD operations (get, save, delete, void, send, download_pdf)
- All QBO object types with complete field listings
- Line item types and DetailType mapping
- Batch operations
- Change Data Capture, attachments, reports, recurring transactions
- Date helpers, JSON utilities, and exception handling
- Complete working examples

## Installation

```bash
claude --plugin-dir ./python-quickbooks
```

## Prerequisites

```bash
pip install python-quickbooks
pip install intuit-oauth
```

## Usage

The skill activates automatically when you ask about QuickBooks Online API integration in Python. Examples:

- "Create a QuickBooks invoice with line items"
- "Query QBO customers by name"
- "Set up QuickBooks authentication"
- "Batch update vendors"
- "Record a payment against an invoice"
