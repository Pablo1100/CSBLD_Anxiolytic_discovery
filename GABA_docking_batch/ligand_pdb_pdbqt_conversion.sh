#!/bin/bash

# Script: ligand_pdb_pdbqt_conversion.sh
# Purpose: Convert all ligand PDB files to PDBQT format using Open Babel
# Requirements: Open Babel installed (brew install open-babel)

echo "Starting ligand PDB to PDBQT conversion..."

# Check if Open Babel is installed
if ! command -v obabel &> /dev/null; then
    echo "Error: Open Babel not found. Install with: brew install open-babel"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p ligands_pdbqt

# Counter for progress
count=0
total=$(ls ligands_pdb/*.pdb 2>/dev/null | wc -l)

if [ "$total" -eq 0 ]; then
    echo "Error: No PDB files found in ligands_pdb/ directory"
    exit 1
fi

echo "Found $total ligand PDB files to convert"

# Convert each PDB to PDBQT
for f in ligands_pdb/*.pdb; do
    base=$(basename "$f" .pdb)
    count=$((count + 1))
    echo "[$count/$total] Converting $base..."
    obabel "$f" -O ligands_pdbqt/${base}.pdbqt --partialcharge gasteiger
done

echo ""
echo "Conversion complete! Generated $(ls ligands_pdbqt/*.pdbqt | wc -l) PDBQT files in ligands_pdbqt/"

