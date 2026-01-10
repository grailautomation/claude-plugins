---
description: Generate a complete API documentation scraper from a URL
arguments:
  - name: url
    description: The API documentation URL to analyze
    required: true
  - name: output
    description: Output directory for the generated scraper (default: current directory)
    required: false
---

# Create Scraper

Generate a complete, production-ready API documentation scraper.

## What This Command Does

Given an API documentation URL, this command:

1. **Analyzes** the documentation site structure and patterns
2. **Designs** a scraper architecture tailored to that structure
3. **Generates** a complete Python scraper package
4. **Validates** the generated code works correctly

The result is a standalone scraper like `workato_scraper/` that can run forever without AI assistance.

## Workflow

### Phase 1: Site Analysis

First, understand the target documentation structure.

**Load the doc-site-analysis skill:**
Read `${CLAUDE_PLUGIN_ROOT}/skills/doc-site-analysis/SKILL.md`

**Fetch and analyze the target URL:**
```
WebFetch {url}
```

Identify:
- Documentation framework (VuePress, Docusaurus, etc.)
- How endpoints are indexed (tables, sidebar, headings)
- How endpoint details are structured
- Where parameters, examples, descriptions are located
- Any edge cases or inconsistencies

**Document findings:**
Write analysis to `{output}/site-analysis.md`

Use the site-analyzer agent if the analysis is complex:
```
Task: Analyze the API documentation structure at {url}
Agent: site-analyzer
```

### Phase 2: Architecture Design

Design the scraper based on discovered patterns.

**Load the scraper-architecture skill:**
Read `${CLAUDE_PLUGIN_ROOT}/skills/scraper-architecture/SKILL.md`

**Study the reference implementation:**
Read `${CLAUDE_PLUGIN_ROOT}/skills/scraper-architecture/examples/workato_scraper/`

Plan:
- Package structure
- Data models needed
- Extraction strategies
- Output formats

### Phase 3: Code Generation

Generate the complete scraper package.

**Load the code-generation skill:**
Read `${CLAUDE_PLUGIN_ROOT}/skills/code-generation/SKILL.md`

**Generate all files:**

1. `{name}_scraper/__init__.py` - Package exports
2. `{name}_scraper/models.py` - Pydantic data models
3. `{name}_scraper/scraper.py` - HTTP fetching logic
4. `{name}_scraper/parser.py` - HTML parsing (the core logic)
5. `{name}_scraper/sections.py` - Section registry
6. `{name}_scraper/cli.py` - Command-line interface
7. `{name}_scraper/formatters/` - Output formatters
8. `main.py` - Entry point
9. `pyproject.toml` - Package configuration
10. `README.md` - Usage documentation

Use the code-generator agent for complex implementations:
```
Task: Generate scraper code based on site-analysis.md
Agent: code-generator
```

### Phase 4: Validation

Verify the generated scraper works.

**Run the validation script:**
```bash
${CLAUDE_PLUGIN_ROOT}/skills/code-generation/scripts/validate-scraper.sh {output}/{name}_scraper
```

Or use the validator agent:
```
Task: Validate the generated scraper at {output}/{name}_scraper
Agent: scraper-validator
```

**Check:**
- Package imports without errors
- Scraper runs successfully
- Endpoints are extracted
- Output formats are valid

### Phase 5: Iteration (if needed)

If validation finds issues:

1. Read the validation report
2. Identify the root cause
3. Fix the issue in the generated code
4. Re-run validation
5. Repeat until passing

### Phase 6: Completion

When validation passes:

1. Summarize what was created
2. Provide usage instructions
3. Note any known limitations

## Example Session

**User input:**
```
/create-scraper https://docs.workato.com/workato-api/connections.html
```

**Phase 1 output:**
```
Analyzing https://docs.workato.com/workato-api/connections.html...

Detected: VuePress framework
Index pattern: Quick reference table with Type/Resource/Description columns
Section pattern: H2 headings with explicit IDs
Found: 8 endpoints on this page

Wrote analysis to ./site-analysis.md
```

**Phase 2-3 output:**
```
Designing scraper architecture...
Using reference: workato_scraper

Generating package: workato_scraper/
  ✓ models.py (6 models)
  ✓ scraper.py (fetch with retry)
  ✓ parser.py (table + heading strategies)
  ✓ sections.py (28 sections)
  ✓ cli.py (argparse interface)
  ✓ formatters/ (JSON, Markdown, OpenAPI)
  ✓ main.py
  ✓ pyproject.toml
  ✓ README.md
```

**Phase 4 output:**
```
Validating generated scraper...
  ✓ Package structure valid
  ✓ Python syntax valid
  ✓ Package imports successfully
  ✓ Scraper runs (extracted 8 endpoints)
  ✓ JSON output valid
  ✓ OpenAPI spec valid

Validation: PASSED
```

**Phase 5 output:**
```
## Scraper Created Successfully!

Generated: workato_scraper/

### Usage:
```bash
# Install
uv venv && uv pip install -e .

# List sections
python main.py --list-sections

# Scrape connections
python main.py --section connections --verbose

# Scrape all sections
python main.py --all --verbose
```

### Output formats:
- JSON: Structured endpoint data
- Markdown: Human-readable documentation
- OpenAPI: Valid 3.0.3 specification

### Notes:
- 28 API sections configured
- 206+ endpoints across all sections
- All outputs validated successfully
```

## Key Principles

1. **Discovery-first** - Don't assume patterns; discover them
2. **Reference-informed** - Learn from workato_scraper example
3. **Validation-driven** - Test until it works
4. **Self-contained** - Generated code runs without AI

## Error Handling

**If site analysis fails:**
- Try alternative pages from the same site
- Look for API reference section
- Check if site requires authentication

**If code generation fails:**
- Simplify the extraction strategy
- Fall back to more generic patterns
- Generate skeleton with TODOs for complex parts

**If validation fails:**
- Read error messages carefully
- Fix one issue at a time
- Re-run validation after each fix
