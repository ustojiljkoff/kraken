###################################
#                                 #
# Parse completed DFT properties. #
#                                 #
###################################

import numpy as np
import subprocess as sp
from utils import *
import yaml

def run_end(ligand: str) -> None:
	"""
	Run the end.py script for a given ligand.
	"""
	# Enter selected confs dir
	os.chdir(selected_confs_dir) #defined in utils.py

	print(f"MLD_LOGGER, fname=run_end.py, ligand={ligand}: Pre end.py.")
	try:
		# Unzip the file, if necessary
		unzip(ligand)

		# Enter ligand dir and copy new end.py script
		os.chdir(ligand)
		shutil.copyfile(f"{tobi_path}", 'end.py')

		# Run end.py
		run(['python', 'end.py'])
		print(f"MLD_LOGGER, fname=run_end.py, ligand={ligand}: Post end.py, no errors.")	

	except Exception as error:
		print(ligand)
		print(error)
		print(f"MLD_LOGGER, fname=run_end.py, ligand={ligand}: Post end.py, yes errors.")

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


	if len(sys.argv) == 2:

		# Use the only input as the ligand of choice
		ligands = sys.argv[1:]

	elif len(sys.argv) == 3:

		# Retrieve the ID of the job and number of batches
		job_id = int(sys.argv[1])
		batches = int(sys.argv[2])

		# All ligands
		all_ligands = np.asarray(sorted(set([file.split('.')[0] for file in os.listdir(selected_confs_dir) if file[0:4] == '0000'])))

		# Partition into subset
		ligands = list(np.array_split(all_ligands, batches)[job_id])

	else:
		ligands = ligands_from_file(input)

	# Run over every ligand in parallel
	#nproc = max((os.cpu_count() - 2, 1))
	#with Pool(nproc) as p:
		#p.map(run_end, ligands)

	for ligand in ligands:
		run_end(ligand)

