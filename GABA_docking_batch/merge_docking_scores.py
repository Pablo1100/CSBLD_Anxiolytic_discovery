import csv

# --- Configuration ---
file_ct0 = 'docking_scores_9CT0.tsv' # Contains 9CT0_alpha2_score
file_crv = 'docking_scores_9CRV.tsv' # Contains 9CRV_alpha1_score

output_trn = 'final_scores_TRN.tsv'
output_f3  = 'final_scores_F3.tsv'

# --- Main Script ---
def merge_and_split():
    # 1. Read the first file (9CT0) into a dictionary for fast lookup
    # Dictionary structure: { 'LIGAND_NAME': -6.833 }
    scores_ct0 = {}
    print(f"Reading {file_ct0}...")
    try:
        with open(file_ct0, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # We strip whitespace just in case
                name = row['NAME'].strip()
                scores_ct0[name] = float(row['9CT0_alpha2_score'])
    except FileNotFoundError:
        print(f"Error: Could not find {file_ct0}")
        return

    # 2. Read the second file (9CRV), merge, and calculate ratio
    merged_data = []
    print(f"Reading {file_crv} and merging...")
    try:
        with open(file_crv, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                name = row['NAME'].strip()
                
                # Only process if this ligand was also found in the 9CT0 file
                if name in scores_ct0:
                    val_ct0 = scores_ct0[name]
                    val_crv = float(row['9CRV_alpha1_score'])
                    
                    # Calculate Ratio: 9CT0 / 9CRV
                    # Note: Vina scores are usually negative. 
                    # (-8.0 / -4.0) = 2.0.
                    if val_crv != 0:
                        ratio = val_ct0 / val_crv
                    else:
                        ratio = 0.0 # Handle division by zero edge case

                    merged_data.append({
                        'NAME': name,
                        '9CT0_alpha2_score': val_ct0,
                        '9CRV_alpha1_score': val_crv,
                        'docking_ratio': ratio
                    })
    except FileNotFoundError:
        print(f"Error: Could not find {file_crv}")
        return

    # 3. Sort the data by NAME
    merged_data.sort(key=lambda x: x['NAME'])

    # 4. Split into two lists based on prefix
    trn_list = [d for d in merged_data if d['NAME'].startswith('TRN_')]
    f3_list  = [d for d in merged_data if d['NAME'].startswith('F3_')]

    # 5. Helper function to write TSV
    def write_results(filename, data_list):
        if not data_list:
            print(f"Warning: No data found for {filename}")
            return
            
        with open(filename, 'w', newline='') as f:
            # Define column order
            fieldnames = ['NAME', '9CT0_alpha2_score', '9CRV_alpha1_score', 'docking_ratio']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
            
            writer.writeheader()
            for row in data_list:
                # Formatting floats to 4 decimal places for cleaner output
                formatted_row = {
                    'NAME': row['NAME'],
                    '9CT0_alpha2_score': f"{row['9CT0_alpha2_score']:.4f}",
                    '9CRV_alpha1_score': f"{row['9CRV_alpha1_score']:.4f}",
                    'docking_ratio': f"{row['docking_ratio']:.4f}"
                }
                writer.writerow(formatted_row)
        print(f"Saved {len(data_list)} rows to {filename}")

    # 6. Write the two output files
    write_results(output_trn, trn_list)
    write_results(output_f3, f3_list)

if __name__ == "__main__":
    merge_and_split()
