#!/bin/bash

# Validate Navier–Stokes simulation results
set -e

ZIP_PATH="data/testing-input-output/navier_stokes_output.zip"
DEST_DIR="."

echo "📦 Unzipping ${ZIP_PATH} to ${DEST_DIR}..."
unzip -o "$ZIP_PATH" -d "$DEST_DIR"

echo "🚀 Running validate_fluid_simulation_input.py..."
python3 validators/validate_fluid_simulation_input.py

echo "✅ Validation completed successfully."



