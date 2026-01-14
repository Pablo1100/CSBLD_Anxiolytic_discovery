#!/bin/bash

# Script: 9CRV_docking.sh
# Purpose: Batch docking of all ligands to 9CRV (alpha1 subunit) receptor using AutoDock Vina

# Requirements: 
#   - AutoDock Vina executable accessible in PATH, or update VINA variable below
#   - Config file (in this case 'config_9CRV.txt')
#   - Receptor and ligand PDBQT files

# Path to Vina executable (modify if Vina is not in your PATH)
VINA="vina"  # or full path like: VINA="/path/to/vina_1.2.7_mac_aarch64"

echo "Starting batch docking to 9CRV (alpha1 subunit)..."

# Check Vina executable exists
if [ ! -f "$VINA" ]; then
    echo "Error: Vina executable not found at $VINA"
    exit 1
fi

# Check config file exists
if [ ! -f "config_9CRV.txt" ]; then
    echo "Error: config_9CRV.txt not found"
    exit 1
fi

# Create output directories
mkdir -p out_9CRV logs_9CRV

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
    echo "[$count/$total] Docking $base on 9CRV..."
    "$VINA" --config config_9CRV.txt \
            --ligand "$lig" \
            --out out_9CRV/${base}_out.pdbqt \
            > logs_9CRV/${base}.log 2>&1
done

echo ""
echo "9CRV docking complete!"
echo "Results in: out_9CRV/"
echo "Logs in: logs_9CRV/"

