# Issue Blaster

A Claude Code plugin for analyzing GitHub issues and implementing AI-generated solution plans.

## Features

- **Solve**: Analyze GitHub issues and generate 2-4 solution plans
- **Implement**: Execute solution plans via worktrees with automated branching, commits, and merge options
- **Parallel Processing**: Solve and implement multiple issues concurrently using Task tool

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) for code search

## Installation

### Via Plugin Marketplace

```bash
# Install from marketplace (when published)
/plugin install issue-blaster@claude-plugins
```

### Manual Installation

```bash
git clone https://github.com/kreitter/issue-blaster ~/.claude-plugins/issue-blaster
```

Then add to your Claude Code settings.

## Usage

### Solve Issues

```bash
# Solve a single issue
/issue-blaster:solve 123

# Solve multiple issues in parallel
/issue-blaster:solve 1 2 3

# Specify repository explicitly
/issue-blaster:solve 123 --repo owner/repo
```

### Implement Plans

```bash
# Implement a single plan
/issue-blaster:implement 123:1

# Implement multiple plans in parallel
/issue-blaster:implement 123:1 456:2 789:1

# Implement by plan path
/issue-blaster:implement plans/issue-123/option-1-fix.md

# Or invoke the agent directly
@issue-blaster:plan-implementer 123 1
```

Each implementation creates a worktree in `.worktrees/`, makes the code changes, commits, and offers merge options (including "leave it" to defer merging).

## Output Structure

```
.worktrees/                          ← gitignored, created during implementation
└── issue-123-minimal-fix/           ← worktree per implementation
plans/                               ← gitignored, created during solving
└── issue-123/
    ├── option-1-minimal-fix.md
    ├── option-2-refactor.md
    └── option-3-new-abstraction.md
```

Each plan file contains:
- YAML frontmatter with metadata (issue number, effort, breaking changes)
- Issue summary and research findings
- Step-by-step implementation plan
- Pros/cons analysis

## Agents

| Agent | Description | Trigger Phrases |
|-------|-------------|-----------------|
| `issue-blaster` | Analyzes one issue, generates 2-4 plans | "solve issue", "analyze issue", "create plan for" |
| `plan-implementer` | Implements a chosen plan via worktree | "implement plan", "execute option", "go with option" |

## Commands

| Command | Description |
|---------|-------------|
| `/issue-blaster:solve` | Dispatch single or batch issue solving |
| `/issue-blaster:implement` | Dispatch single or parallel plan implementation |

## License

MIT
