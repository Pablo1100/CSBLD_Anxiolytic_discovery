import os
import glob

# --- Configuration ---
log_dir = 'logs_9CT0'
output_file = 'docking_scores_9CT0.tsv'

# --- Main Script ---
def extract_scores():
    # 1. Prepare the output file and write the header
    with open(output_file, 'w') as out:
        out.write("NAME\t9CT0_alpha2_score\n")
        
        # 2. Find all .log files in the directory
        log_files = glob.glob(os.path.join(log_dir, '*.log'))
        print(f"Found {len(log_files)} log files. Processing...")

        for filepath in log_files:
            try:
                # 3. Extract NAME from the filename
                # filepath is like 'logs_9CT0/F3_CHEMBL13794.log'
                filename = os.path.basename(filepath)  # -> 'F3_CHEMBL13794.log'
                name = os.path.splitext(filename)[0]   # -> 'F3_CHEMBL13794'
                
                # 4. Parse the file to find the score
                score = "NA" # Default if not found
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        # Look for the table separator string
                        if "-----+------------+" in line:
                            # The best score is always on the very next line (i+1)
                            if i + 1 < len(lines):
                                best_mode_line = lines[i+1]
                                # Split the line by whitespace
                                # Line looks like: "   1       -6.833          0          0"
                                columns = best_mode_line.split()
                                if len(columns) >= 2:
                                    score = columns[1] # The second column is affinity
                                    break 
                
                # 5. Write the result to the TSV file
                out.write(f"{name}\t{score}\n")

            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    print(f"Done! Results saved to '{output_file}'")

if __name__ == "__main__":
    extract_scores()
