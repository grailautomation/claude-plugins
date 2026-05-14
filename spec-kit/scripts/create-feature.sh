#!/usr/bin/env bash
set -euo pipefail

# Create a new feature branch and spec directory.
# Usage: create-feature.sh [--no-branch] <feature_description>
# Output: JSON with BRANCH_NAME, SPEC_FILE, FEATURE_NUM

NO_BRANCH="${SPEC_KIT_NO_BRANCH:-false}"
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --no-branch) NO_BRANCH=true ;;
        --help|-h)
            echo "Usage: $0 [--no-branch] <feature_description>" >&2
            exit 0
            ;;
        *) ARGS+=("$arg") ;;
    esac
done

FEATURE_DESCRIPTION="${ARGS[*]:-}"
if [[ -z "$FEATURE_DESCRIPTION" ]]; then
    echo "Usage: $0 <feature_description>" >&2
    exit 1
fi

# Determine repo root
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(pwd)"
    HAS_GIT=false
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/.specify/specs"
mkdir -p "$SPECS_DIR"

# Find highest existing feature number
HIGHEST=0
if [[ -d "$SPECS_DIR" ]]; then
    for dir in "$SPECS_DIR"/*/; do
        [[ -d "$dir" ]] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [[ "$number" -gt "$HIGHEST" ]]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
FEATURE_NUM=$(printf "%03d" "$NEXT")

# Derive branch name from description (first 3 words, kebab-case)
BRANCH_NAME=$(echo "$FEATURE_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
WORDS=$(echo "$BRANCH_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
BRANCH_NAME="${FEATURE_NUM}-${WORDS}"

# Create git branch if possible. Fail loudly on collisions or checkout errors
# unless the caller intentionally requested current-branch mode.
if [[ "$HAS_GIT" == "true" && "$NO_BRANCH" != "true" ]]; then
    if git rev-parse --verify --quiet "$BRANCH_NAME" >/dev/null; then
        echo "ERROR: Branch already exists: $BRANCH_NAME" >&2
        echo "Choose a more specific feature description or set SPECIFY_FEATURE for an existing feature." >&2
        exit 1
    fi
    git checkout -b "$BRANCH_NAME"
elif [[ "$HAS_GIT" == "true" ]]; then
    echo "[spec-kit] Current-branch mode; skipped branch creation for $BRANCH_NAME" >&2
    echo "[spec-kit] Set SPECIFY_FEATURE=$BRANCH_NAME for follow-up commands on this branch." >&2
else
    echo "[spec-kit] Warning: No git repo; skipped branch creation for $BRANCH_NAME" >&2
    echo "[spec-kit] Set SPECIFY_FEATURE=$BRANCH_NAME for follow-up commands." >&2
fi

# Create feature directory and empty spec file
FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"
mkdir -p "$REPO_ROOT/.specify/memory"
SPEC_FILE="$FEATURE_DIR/spec.md"
touch "$SPEC_FILE"

printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s","FEATURE_DIR":"%s"}\n' \
    "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM" "$FEATURE_DIR"
