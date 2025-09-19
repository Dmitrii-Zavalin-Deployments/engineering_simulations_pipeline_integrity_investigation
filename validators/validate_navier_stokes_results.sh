#!/bin/bash
set -euo pipefail

echo "📦 Unzipping navier_stokes_output.zip to data/testing-input-output/navier_stokes_output/"
unzip -o data/testing-input-output/navier_stokes_output.zip -d data/testing-input-output/navier_stokes_output/

OUTPUT_DIR="data/testing-input-output/navier_stokes_output"
STEP_PATTERN="fluid_simulation_input_step_*.json"
LOG_FILES=("divergence_log.txt" "influence_flags_log.json" "mutation_pathways_log.json" "step_summary.txt")

# Pre-check: Ensure step files exist
echo "🔍 Checking for step snapshot files..."
STEP_COUNT=$(ls "$OUTPUT_DIR"/$STEP_PATTERN 2>/dev/null | wc -l)
if [ "$STEP_COUNT" -eq 0 ]; then
  echo "❌ No step snapshot files found in $OUTPUT_DIR. Validation aborted."
  exit 1
else
  echo "✅ Found $STEP_COUNT step snapshot file(s)."
fi

# Pre-check: Log file presence
echo "📄 Checking for expected log files..."
for log_file in "${LOG_FILES[@]}"; do
  if [ -f "$OUTPUT_DIR/$log_file" ]; then
    echo "✅ Found log file: $log_file"
  else
    echo "⚠️ Missing log file: $log_file"
  fi
done

# Set Python module path
export PYTHONPATH=$(pwd)

# Run Python validator
echo "🚀 Running validate_navier_stokes_results.py..."
python3 validators/validate_navier_stokes_results.py



