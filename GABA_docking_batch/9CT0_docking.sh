#!/bin/bash

# Script: 9CT0_docking.sh
# Purpose: Batch docking of all ligands to 9CT0 (alpha2 subunit) receptor using AutoDock Vina

# Requirements: 
#   - AutoDock Vina executable accessible in PATH, or update VINA variable below
#   - Config file (in this case 'config_9CT0.txt')
#   - Receptor and ligand PDBQT files

# Path to Vina executable (modify if Vina is not in your PATH)
VINA="vina"  # or full path like: VINA="/path/to/vina_1.2.7_mac_aarch64"

echo "Starting batch docking to 9CT0 (alpha2 subunit)..."

# Check Vina executable exists
if [ ! -f "$VINA" ]; then
    echo "Error: Vina executable not found at $VINA"
    exit 1
fi

# Check config file exists
if [ ! -f "config_9CT0.txt" ]; then
    echo "Error: config_9CT0.txt not found"
    exit 1
fi

# Create output directories
mkdir -p out_9CT0 logs_9CT0

# Count ligands
total=$(ls ligands_pdbqt/*.pdbqt 2>/dev/null | wc -l)
if [ "$total" -eq 0 ]; then
    echo "Error: No PDBQT ligands found in ligands_pdbqt/"
    exit 1
fi

echo "Found $total ligands to dock"
echo ""

# Counter for progress
count=0

# Dock each ligand
for lig in ligands_pdbqt/*.pdbqt; do
    base=$(basename "$lig" .pdbqt)
    count=$((count + 1))
    echo "[$count/$total] Docking $base on 9CT0..."
    "$VINA" --config config_9CT0.txt \
            --ligand "$lig" \
            --out out_9CT0/${base}_out.pdbqt \
            > logs_9CT0/${base}.log 2>&1
done

echo ""
echo "9CT0 docking complete!"
echo "Results in: out_9CT0/"
echo "Logs in: logs_9CT0/"

