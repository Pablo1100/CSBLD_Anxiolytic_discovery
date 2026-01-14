# Molecular Docking Analysis: Filter 3 (AutoDock Vina)

## Project Information

**Course:** Computational Structural Biology and Lead Discovery  
**Institution:** Universidad Politécnica de Madrid (UPM)  
**Student:** Pablo Rodríguez López  
**Project Title:** *In Silico Identification of Novel α2-selective Positive Allosteric Modulators (PAMs) for GABA-A Receptors in Anxiety Treatment*  
**Date:** January 2026

## Overview

This directory contains all scripts, data, and results for the final filtering step (Filter 3) of the virtual screening pipeline: **molecular docking using AutoDock Vina**. The objective is to evaluate the α2-selectivity of candidate compounds by comparing their predicted binding affinities to two GABA-A receptor structures:

- **9CT0**: α2β2γ2 assembly (α2-containing receptor)
- **9CRV**: α1β2γ2 assembly (α1-containing receptor)

The docking-based selectivity metric (docking ratio = E_α1 / E_α2) is used to prioritize compounds that preferentially bind to the α2 subunit, avoiding α1-mediated sedative effects.

---

## Initial Directory Structure

At the start of this analysis, the working directory contained:

GABA_docking_batch/
|-- ligands_pdb/              # Minimized ligand structures (PDB format)
|   |-- TRN_CHEMBL*.pdb       # Training set ligands (21 compounds)
|   +-- F3_CHEMBL*.pdb        # Filter 2 survivors (13 candidates)
|-- receptors/                # Prepared receptor structures (PDBQT format)
|   |-- 9CT0_receptor.pdbqt   # alpha2-containing receptor
|   +-- 9CRV_receptor.pdbqt   # alpha1-containing receptor
|-- config_9CT0.txt           # Vina configuration for 9CT0
+-- config_9CRV.txt           # Vina configuration for 9CRV

---

## Data Preparation

### Receptor Preparation

1. **Source:** Cryo-EM structures downloaded from PDB:
   - **9CT0** (α2β2γ2): Resolution 3.19 Å
   - **9CRV** (α1β2γ2): Resolution 3.18 Å

2. **Processing in UCSF Chimera:**
   - Removed water molecules, ions, and non-essential heteroatoms
   - Applied **Dock Prep**:
     - Added hydrogens
     - Assigned charges (AMBER ff14SB for protein)
   - Saved cleaned receptors as PDB files

3. **Conversion to PDBQT:**
   - Performed a 'test docking' with alprazolam molecule, and kept the .receptor.pdbqt file and renamed it
   - Files placed in `receptors/` directory

### Ligand Preparation

1. **Source:**
   - **Training set (21 compounds):** potenially α2-selective PAMs based on experimental Ki data
   - **Filter 3 candidates (12 compounds):** Survivors from pharmacophore screening (Filter 2)

2. **Processing in UCSF Chimera:**
   - Generated 3D structures from SMILES using "Build Structure" tool
   - 3 rounds of Energy minimization:
     - Steepest descent: 3000 steps (step size 0.02 Å)
     - Conjugate gradient: 300 steps (step size 0.02 Å)
   - Saved as PDB files in `ligands_pdb/`

3. **Conversion to PDBQT:**
   - Performed using `ligand_pdb_pdbqt_conversion.sh` script (see Workflow below)

### Docking Grid Definition

**Binding site identification:**
- The benzodiazepine/PAM binding pocket is located at the **α+/γ2- interface** in the extracellular domain
- Grid center defined by the **Cα atom** of the conserved histidine residue:
  - **9CT0 (α2):** His101 (α2 subunit)
  - **9CRV (α1):** His102 (α1 subunit)

**Grid parameters (both receptors):**

Box size: 25 × 25 × 25 Å
Exhaustiveness: 16
Number of modes: 10


Coordinates specified in `config_9CT0.txt` and `config_9CRV.txt`.

---

## Workflow

### Software Requirements

- **Open Babel** (v. 3.1.0): For PDB to PDBQT conversion  
  Installation (macOS): `brew install open-babel`
  
- **AutoDock Vina** (v. 1.2.7): Molecular docking engine  
  Download: [GitHub Releases](https://github.com/ccsb-scripps/AutoDock-Vina/releases)

- **Python 3.x**: for docking scores processing

### Steps

#### 1. Convert Ligands to PDBQT Format


./ligand_pdb_pdbqt_conversion.sh


- Converts all PDB files in ligands_pdb/ to PDBQT format

- Output: ligands_pdbqt/ directory with PDBQT files

- Assigns Gasteiger partial charges

#### 2. Dock Ligands to 9CT0 (α2 Receptor)

./9CT0_docking.sh

- Docks all ligands to 9CT0 receptor using config_9CT0.txt

- Output directories:

   - out_9CT0/: Docked poses (PDBQT format)

   - logs_9CT0/: Vina log files with binding energies

#### 3. Dock Ligands to 9CRV (α1 Receptor)

./9CRV_docking.sh

- Docks all ligands to 9CRV receptor using config_9CRV.txt

- Output directories:

   - out_9CRV/: Docked poses (PDBQT format)

   - logs_9CRV/: Vina log files with binding energies

#### 4. Extract Docking Scores

python extract_vina_scores_9CT0.py
python extract_vina_scores_9CRV.py

- Parses Vina log files to extract best binding affinity (mode 1)

- Output:

   - docking_scores_9CT0.tsv: Ligand names and 9CT0 scores

   - docking_scores_9CRV.tsv: Ligand names and 9CRV scores

5. Merge Results and Calculate Selectivity

python merge_docking_scores.py

- Merges 9CT0 and 9CRV scores for training set and Filter 2 survivors

- Calculates docking ratio = E_α1 / E_α2

   - Ratio > 1: α2-selective (desired)

   - Ratio < 1: α1-preferring (undesired)

- Output:

   - final_scores_TRN.tsv: Training set results

   - final_scores_F3.tsv: Filter 3 candidates results

#### 6. Analyze and Visualize Results

See Jupyter notebook: Docking_Analysis.ipynb

- Merges docking results with experimental data (training set)

- Plots correlation between docking ratio and experimental log2(Ki α2/α1)

- Ranks Filter 3 candidates by predicted α2-selectivity

## Final Directory Structure

After completing all steps:

GABA_docking_batch/
|-- ligands_pdb/                      # Original ligand PDB files
|   |-- TRN_CHEMBL*.pdb       
|   +-- F3_CHEMBL*.pdb        
|-- ligands_pdbqt/                    # Converted ligand PDBQT files
|   |-- TRN_CHEMBL*.pdbqt                                            
|   +-- F3_CHEMBL*.pdbqt 
|-- receptors/                        # Receptor PDBQT files
|   |-- 9CT0_receptor.pdbqt
|   +-- 9CRV_receptor.pdbqt
|-- config_9CT0.txt                   # Vina config for 9CT0
|-- config_9CRV.txt                   # Vina config for 9CRV
|-- out_9CT0/                         # 9CT0 docked poses
|-- out_9CRV/                         # 9CRV docked poses
|-- logs_9CT0/                        # 9CT0 docking logs
|-- logs_9CRV/                        # 9CRV docking logs
|-- docking_scores_9CT0.tsv           # Extracted 9CT0 scores
|-- docking_scores_9CRV.tsv           # Extracted 9CRV scores
|-- final_scores_TRN.tsv              # Training set docking results
|-- final_scores_F3.tsv               # Filter 3 candidates results
|-- ligand_pdb_pdbqt_conversion.sh    # Script: PDB to PDBQT conversion
|-- 9CT0_docking.sh                   # Script: 9CT0 batch docking
|-- 9CRV_docking.sh                   # Script: 9CRV batch docking
|-- extract_vina_scores_9CT0.py       # Script: Extract 9CT0 scores
|-- extract_vina_scores_9CRV.py       # Script: Extract 9CRV scores
|-- merge_docking_scores.py           # Script: Merge and calculate selectivity
|-- Docking_results_analysis.ipynb    # Jupyter notebook: Analysis and plots
+-- README.md                         # This file

