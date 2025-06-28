#!/bin/bash

# Validate Navier–Stokes simulation results
set -e

echo "📦 Unzipping navier_stokes_output.zip..."
unzip -o navier_stokes_output.zip -d ./validators

echo "🚀 Running validate_fluid_simulation_input.py..."
python3 validators/validate_fluid_simulation_input.py

echo "✅ Validation completed successfully."


