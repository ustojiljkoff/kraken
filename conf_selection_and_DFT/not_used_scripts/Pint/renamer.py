import os
import subprocess as sp
import yaml
from pathlib import Path
import shutil

with open("config.yaml") as f:
	config = yaml.safe_load(f)
selected_confs_dir = "/cluster/home/stojiljkovic/kraken_final/kraken/conf_selection_and_DFT/selected_conformers"

import os
import subprocess as sp
import yaml
from pathlib import Path
import shutil

with open("config.yaml") as f:
    config = yaml.safe_load(f)
selected_confs_dir = "/cluster/home/stojiljkovic/kraken_final/kraken/conf_selection_and_DFT/selected_conformers"

def out_chk_renamer():
    """
    Rename .out files to .log and convert .chk files to .fchk in all subfolders of selected_confs_dir.
    """
    start_dir = selected_confs_dir
    print(f"Current directory: {start_dir}")
    print(f"listdir: {os.listdir(start_dir)}")

    # Loop over all first-level subdirectories
    for folder in os.listdir(start_dir):
        folder_path = os.path.join(start_dir, folder)
        if not os.path.isdir(folder_path):
            print(f"Skipping {folder_path}, not a directory.")
            continue

        # Loop over all subfolders within each first-level folder
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.isdir(subfolder_path):
                print(f"Skipping {subfolder_path}, not a directory.")
                continue

            print(f"Processing subfolder: {subfolder_path}")

            # Rename .out to .log
            for file in os.listdir(subfolder_path):
                if file.endswith(".out") and "slurm" not in file:
                    base = os.path.splitext(file)[0]
                    new_name = base + ".log"
                    os.rename(os.path.join(subfolder_path, file), os.path.join(subfolder_path, new_name))
                    print(f"Renamed {file} → {new_name} in {subfolder_path}")

            # Convert .chk to .fchk
            for file in os.listdir(subfolder_path):
                if file.endswith(".chk"):
                    base = os.path.splitext(file)[0]
                    chk_file = os.path.join(subfolder_path, file)
                    fchk_file = os.path.join(subfolder_path, base + ".fchk")
                    try:
                        sp.run(["formchk", chk_file, fchk_file], check=True)
                        print(f"Converted {chk_file} → {fchk_file}")
                    except sp.CalledProcessError:
                        print(f"Error running formchk on {chk_file} in {subfolder_path}")
                    except FileNotFoundError:
                        print("Error: 'formchk' command not found. Make sure Gaussian is properly sourced.")

if __name__ == '__main__':
    out_chk_renamer()
if __name__ == '__main__':
	out_chk_renamer()