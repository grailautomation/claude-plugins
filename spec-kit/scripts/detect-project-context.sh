#!/usr/bin/env bash
set -euo pipefail

WRITE=false
JSON=false

for arg in "$@"; do
    case "$arg" in
        --write) WRITE=true ;;
        --json) JSON=true ;;
        --help|-h)
            cat <<'EOF'
Usage: detect-project-context.sh [--write] [--json]

Detects lightweight brownfield repository context for spec-kit workflows.
With --write, writes local-only .specify/memory/project-context.md and
ensures the path is ignored in git repositories.
With --json, emits a compact JSON object instead of Markdown.
EOF
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'" >&2
            exit 1
            ;;
    esac
done

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT=$(pwd)
    HAS_GIT=false
fi

cd "$REPO_ROOT"

detect_files() {
    local files=("$@")
    local found=()
    for file in "${files[@]}"; do
        [[ -e "$file" ]] && found+=("$file")
    done
    if [[ ${#found[@]} -eq 0 ]]; then
        echo "None detected"
    else
        join_items "${found[@]}"
    fi
}

detect_dirs() {
    local dirs=("$@")
    local found=()
    for dir in "${dirs[@]}"; do
        [[ -d "$dir" ]] && found+=("$dir")
    done
    if [[ ${#found[@]} -eq 0 ]]; then
        echo "None detected"
    else
        join_items "${found[@]}"
    fi
}

join_items() {
    local item
    local out=""
    for item in "$@"; do
        if [[ -z "$out" ]]; then
            out="$item"
        else
            out="$out, $item"
        fi
    done
    echo "$out"
}

detect_test_commands() {
    local commands=()
    [[ -f package.json ]] && commands+=("Use the package manager scripts in package.json")
    [[ -f pyproject.toml ]] && commands+=("Run the repo's Python test command from pyproject/tooling")
    [[ -f pytest.ini || -f tox.ini ]] && commands+=("pytest")
    [[ -f Cargo.toml ]] && commands+=("cargo test")
    [[ -f go.mod ]] && commands+=("go test ./...")
    [[ -f Package.swift ]] && commands+=("swift test")
    [[ -f Makefile ]] && commands+=("Inspect Makefile targets before inventing commands")
    if [[ ${#commands[@]} -eq 0 ]]; then
        echo "No standard test command detected; infer from repo docs before planning."
    else
        printf '%s\n' "${commands[@]}" | awk '!seen[$0]++' | sed 's/^/- /'
    fi
}

detect_primary_stack() {
    local stack=()
    [[ -f package.json ]] && stack+=("Node/JavaScript")
    [[ -f tsconfig.json ]] && stack+=("TypeScript")
    [[ -f pyproject.toml || -f requirements.txt ]] && stack+=("Python")
    [[ -f Cargo.toml ]] && stack+=("Rust")
    [[ -f go.mod ]] && stack+=("Go")
    [[ -f Package.swift ]] && stack+=("Swift")
    [[ -f pom.xml || -f build.gradle || -f build.gradle.kts ]] && stack+=("JVM")
    [[ -f Gemfile ]] && stack+=("Ruby")
    [[ -f composer.json ]] && stack+=("PHP")
    if [[ ${#stack[@]} -eq 0 ]]; then
        echo "Unknown from root files"
    else
        join_items "${stack[@]}"
    fi
}

GIT_BRANCH="none"
if [[ "$HAS_GIT" == "true" ]]; then
    if GIT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null); then
        :
    elif GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) && [[ "$GIT_BRANCH" != "HEAD" ]]; then
        :
    else
        GIT_BRANCH="unknown"
    fi
fi

PRIMARY_STACK=$(detect_primary_stack)
PACKAGE_FILES=$(detect_files package.json pnpm-lock.yaml yarn.lock package-lock.json bun.lockb pyproject.toml uv.lock requirements.txt Cargo.toml go.mod Package.swift pom.xml build.gradle build.gradle.kts Gemfile composer.json)
SOURCE_DIRS=$(detect_dirs src app apps packages lib backend frontend server client api ios android tests test spec docs)
CONFIG_FILES=$(detect_files README.md AGENTS.md CLAUDE.md Makefile justfile turbo.json nx.json tsconfig.json vite.config.ts next.config.js pytest.ini tox.ini ruff.toml .prettierrc .eslintrc.json)
TEST_COMMANDS=$(detect_test_commands)

DATE=$(date +%Y-%m-%d)
PROJECT_CONTEXT_PATH=".specify/memory/project-context.md"

ensure_local_context_ignored() {
    [[ "$HAS_GIT" == "true" ]] || return 0

    if git check-ignore -q "$PROJECT_CONTEXT_PATH" 2>/dev/null; then
        return 0
    fi

    local gitignore="$REPO_ROOT/.gitignore"
    if [[ -f "$gitignore" ]] && grep -Fxq "$PROJECT_CONTEXT_PATH" "$gitignore"; then
        return 0
    fi

    {
        [[ -s "$gitignore" ]] && printf '\n'
        printf '# Spec Kit local context\n'
        printf '%s\n' "$PROJECT_CONTEXT_PATH"
    } >> "$gitignore"
}

if $JSON; then
    printf '{"repoRoot":"%s","generated":"%s","hasGit":%s,"branch":"%s","primaryStack":"%s","packageFiles":"%s","sourceDirs":"%s","configFiles":"%s"}\n' \
        "$REPO_ROOT" "$DATE" "$HAS_GIT" "$GIT_BRANCH" "$PRIMARY_STACK" "$PACKAGE_FILES" "$SOURCE_DIRS" "$CONFIG_FILES"
    exit 0
fi

read -r -d '' CONTENT <<EOF || true
# Project Context

Generated: $DATE
Repository: $REPO_ROOT
Git branch: $GIT_BRANCH

## Detected Stack
$PRIMARY_STACK

## Package And Tooling Files
$PACKAGE_FILES

## Source And Test Directories
$SOURCE_DIRS

## Repo Guidance And Config Files
$CONFIG_FILES

## Likely Verification Commands
$TEST_COMMANDS

## Brownfield Rules
- Prefer existing project structure, dependencies, helpers, naming, and test style.
- Do not introduce a new framework, package manager, architectural layer, or top-level directory unless the plan explains why existing patterns are insufficient.
- Put feature work in existing analogous modules when they exist.
- If the repo has no clear convention for a choice, record the assumption in the plan before implementing.
- Keep the first implementation small enough to review in one focused pass.
EOF

if $WRITE; then
    mkdir -p "$REPO_ROOT/.specify/memory"
    ensure_local_context_ignored
    printf '%s\n' "$CONTENT" > "$REPO_ROOT/$PROJECT_CONTEXT_PATH"
fi

printf '%s\n' "$CONTENT"
