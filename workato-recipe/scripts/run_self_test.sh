#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAX_TESTDATA_BYTES=$((256 * 1024))

cd "$ROOT"

echo "=== Testdata size check ==="
testdata_bytes="$(python - "$ROOT/testdata" <<'PY'
import sys
from pathlib import Path

root = Path(sys.argv[1])
print(sum(path.stat().st_size for path in root.glob("**/*") if path.is_file()))
PY
)"
echo "  testdata bytes: $testdata_bytes"
if (( testdata_bytes > MAX_TESTDATA_BYTES )); then
  echo "ERROR: testdata exceeds ${MAX_TESTDATA_BYTES} bytes" >&2
  exit 1
fi
echo ""

echo "=== Unit tests ==="
python -m unittest discover -s tests -p 'test_*.py'
echo ""

echo "=== Fixture fidelity ==="
for recipe in "$ROOT"/testdata/*.recipe.json; do
  recipe_name="$(basename "$recipe")"
  echo "  Checking $recipe_name"
  views_dir="$(python "$ROOT/cli.py" extract --force --recipe "$recipe")"
  if [[ "$recipe_name" == "ambiguous_multi_catch.recipe.json" ]]; then
    if python "$ROOT/cli.py" check-fidelity \
      --recipe "$recipe" \
      --summary "$views_dir/summary.json" \
      --schema "$ROOT/schemas/summary_fidelity_v2.schema.json" \
      --format text > /dev/null; then
      echo "ERROR: expected unsupported topology to fail for $recipe_name" >&2
      exit 1
    fi
  else
    python "$ROOT/cli.py" check-fidelity \
      --recipe "$recipe" \
      --summary "$views_dir/summary.json" \
      --schema "$ROOT/schemas/summary_fidelity_v2.schema.json" \
      --format text > /dev/null
  fi
done
