#!/usr/bin/env bash
# Validate a generated scraper package
#
# Usage: validate-scraper.sh <scraper_dir> [section]
#
# Example: validate-scraper.sh ./workato_scraper connections

set -euo pipefail

SCRAPER_DIR="${1:?Usage: validate-scraper.sh <scraper_dir> [section]}"
SECTION="${2:-}"
OUTPUT_DIR="output_validation"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success() { echo -e "${GREEN}✓${NC} $1"; }
warning() { echo -e "${YELLOW}!${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }

echo "=== Validating scraper: $SCRAPER_DIR ==="

# Derive package name from directory
PACKAGE_NAME=$(basename "$SCRAPER_DIR")

# 1. Check package structure
echo ""
echo "Checking package structure..."

required_files=(
    "__init__.py"
    "models.py"
    "parser.py"
    "scraper.py"
)

optional_files=(
    "cli.py"
    "sections.py"
    "formatters/__init__.py"
)

all_present=true
for file in "${required_files[@]}"; do
    if [[ -f "$SCRAPER_DIR/$file" ]]; then
        success "$file exists"
    else
        error "Missing required: $file"
        all_present=false
    fi
done

for file in "${optional_files[@]}"; do
    if [[ -f "$SCRAPER_DIR/$file" ]]; then
        success "$file exists"
    else
        warning "Missing optional: $file"
    fi
done

if [[ "$all_present" != "true" ]]; then
    echo ""
    error "Package structure incomplete"
    exit 1
fi

# 2. Check Python syntax
echo ""
echo "Checking Python syntax..."

syntax_ok=true
for pyfile in "$SCRAPER_DIR"/*.py "$SCRAPER_DIR"/**/*.py 2>/dev/null; do
    if [[ -f "$pyfile" ]]; then
        if python3 -m py_compile "$pyfile" 2>/dev/null; then
            success "$(basename "$pyfile") syntax OK"
        else
            error "Syntax error in $(basename "$pyfile")"
            syntax_ok=false
        fi
    fi
done

if [[ "$syntax_ok" != "true" ]]; then
    echo ""
    error "Syntax errors found"
    exit 1
fi

# 3. Check imports
echo ""
echo "Checking imports..."

cd "$(dirname "$SCRAPER_DIR")"
if python3 -c "import ${PACKAGE_NAME}" 2>/dev/null; then
    success "Package imports successfully"
else
    error "Package import failed"
    exit 1
fi

# 4. Check model definitions
echo ""
echo "Checking model definitions..."

model_check=$(python3 -c "
from ${PACKAGE_NAME}.models import APIDocumentation, Endpoint, Parameter
print('Models OK')
" 2>&1) || true

if [[ "$model_check" == "Models OK" ]]; then
    success "Core models defined"
else
    error "Missing core models"
    echo "$model_check"
    exit 1
fi

# 5. Check parser function
echo ""
echo "Checking parser..."

parser_check=$(python3 -c "
from ${PACKAGE_NAME}.parser import parse_documentation
import inspect
sig = inspect.signature(parse_documentation)
params = list(sig.parameters.keys())
if 'html' in params:
    print('Parser OK')
else:
    print('Parser missing html parameter')
" 2>&1) || true

if [[ "$parser_check" == "Parser OK" ]]; then
    success "parse_documentation function OK"
else
    error "Parser function issue"
    echo "$parser_check"
    exit 1
fi

# 6. Run scraper if section provided
if [[ -n "$SECTION" ]]; then
    echo ""
    echo "Running scraper on section: $SECTION..."

    mkdir -p "$OUTPUT_DIR"

    # Check if main.py exists
    if [[ -f "main.py" ]]; then
        if python3 main.py --section "$SECTION" --output-dir "$OUTPUT_DIR" --verbose; then
            success "Scraper ran successfully"
        else
            error "Scraper failed"
            exit 1
        fi
    else
        warning "No main.py found, skipping runtime test"
    fi

    # Validate outputs
    for ext in json yaml; do
        output_file=$(find "$OUTPUT_DIR" -name "*.$ext" | head -1)
        if [[ -n "$output_file" ]]; then
            if [[ "$ext" == "json" ]]; then
                if python3 -c "import json; json.load(open('$output_file'))"; then
                    success "JSON output valid: $(basename "$output_file")"
                else
                    error "Invalid JSON: $output_file"
                fi
            elif [[ "$ext" == "yaml" ]]; then
                if python3 -c "import yaml; yaml.safe_load(open('$output_file'))"; then
                    success "YAML output valid: $(basename "$output_file")"
                else
                    error "Invalid YAML: $output_file"
                fi
            fi
        fi
    done

    # Validate OpenAPI if spec exists
    openapi_file=$(find "$OUTPUT_DIR" -name "*openapi.yaml" | head -1)
    if [[ -n "$openapi_file" ]]; then
        if command -v npx &> /dev/null; then
            echo ""
            echo "Validating OpenAPI spec..."
            if npx @openapitools/openapi-generator-cli validate -i "$openapi_file" 2>&1 | grep -q "No validation issues"; then
                success "OpenAPI spec valid"
            else
                warning "OpenAPI validation issues found"
            fi
        else
            warning "npx not found, skipping OpenAPI validation"
        fi
    fi

    # Cleanup
    rm -rf "$OUTPUT_DIR"
fi

echo ""
echo "=== Validation complete ==="
