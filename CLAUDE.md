# Claude Plugins

## Content Governance

**Never commit real org IDs, email addresses, company names, or credentials to this repo.** User-specific data goes in `.local.md` files (gitignored) or `~/.claude/skills/`.

### Decision Tree

```
Does it contain PII, org IDs, credentials, or company-specific data?
├── YES → Is it contextually tied to a specific plugin?
│   ├── YES → .local.md file inside the plugin (gitignored)
│   └── NO  → User-level skill (~/.claude/skills/)
└── NO  → Is it useful to other Claude Code users?
    ├── YES → Plugin repo (public)
    └── NO  → User-level skill or doesn't need to exist
```

### The Four Tiers

| Tier | Location | What goes here | Example |
|------|----------|---------------|---------|
| 1. Public | Plugin repo | Generic, reusable content that works for any user | SOQL syntax guides, Workato SDK docs, generic agents |
| 2. User skills | `~/.claude/skills/` | Personal knowledge spanning multiple projects | Machine config, company/org context, credential refs |
| 3. Local plugin | `*.local.md` (gitignored) | User-specific data tied to a specific plugin | Org schemas, personal domain lists, custom paths |
| 4. Private | Don't publish | Plugins inherently org-specific with no generic value | Internal API connectors with no reusable patterns |

### Pre-Commit Checks

Before committing, verify no PII in tracked files:

```bash
# Check for email addresses (excluding example.com and plugin infra files)
grep -rn '@[a-z]' --include='*.md' . | grep -v '@example' | grep -v 'CLAUDE.md'
grep -rn '@[a-z]' --include='*.md' --include='*.json' . | grep -v '@example' | grep -v 'CLAUDE.md' | grep -v 'plugin.json' | grep -v 'marketplace.json'

# Check for Salesforce org IDs
grep -rn '00D[A-Za-z0-9]\{15\}' --include='*.md' . | grep -v '00D000000000000'

# Check for hardcoded user paths
grep -rn '/Users/[a-z]' --include='*.md' .
```

### Git History Note

PII from the salesforce-soql org schemas existed in git history prior to commit `fe12666`. This is a documented risk acceptance — the repo was not public at the time, and history rewriting is destructive. If the repo is ever made public, run `git filter-repo` on the affected commits first.
