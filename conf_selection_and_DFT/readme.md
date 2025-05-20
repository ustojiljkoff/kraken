# Modified conformer selection, DFT calculation and property extraction part

## Comments on the fork
- Code revision, bug fixes and error correction 
- Path definition enabled through a yaml file, instead of in-code definition
- Removal of unnecessary files
- Currently optimized for the STUDIX cluster of the University of Basel, Department of Chemistry, but easily optimizable for other cluster.
- added `kraken_dft.yaml` file for installation of the conda venv.

## Usage
**Before running the script one needs to:**
1. **Modify the paths in the ``config.yaml`` file**
2. **Modify the bash scripts ``conf_script.sh`` and ``end_script.sh``**

**In the ``config.yaml``, one should define paths to:**
- working directories and input files for kraken
- kraken python scripts, i.e. ``tobi``, ``pint``, ``ded``
- executable files and folders of external software, such as dftd3 and Multiwfn
- Gaussian submission script

Please follow the comments in the ``config.yaml`` file for correct path definition.

**In the bash scripts ``conf_script.sh`` and ``end_script.sh`` one should:**
- Modify the `#SBATCH` section for the needs of the cluster where the scripts are run
- Modify the module loading and venv activation sections based on your needs

### Step 1. CREST conformer search and xTB calculation
- As in the original code, follow the instructions from the previous folder within this fork.
- When this part is finished, copy folders ``results_all_Ni`` and ``results_all_noNi`` in this folder (or define the path to them).

### Step 2. Conformer selection and DFT calculations
This part selects the conformers that will be considered for DFT calculations and runs DFT calculations. It takes YAML files from Step 1. as the input, along with the list of ligands that should be considered (defined in ``input.txt`` file)
#### Usage:
- When you have defined paths, or copied the results of CREST/xTB section, along with the list of ligands, run this part of the script with `sbatch conf_script.sh`
- The script should in the end make directories for the selected conformers with the output files of the DFT calculations

#### Please note:
- That for this part of the script you need to have a working Gaussian submission script (defined in `config.yaml`)
- The script takes by default ``%nprocs=16`` and ``%mem=16GB`` for the DFT calculations. If you wish to use different settings, please modify this in the ``PL_gaussian_input_200411.py`` file (see end of readme)

### Step 3. DFT property extraction
This part extracts properties of the conformers (and therefore ligands) from the DFT calculations.
#### Usage
- When the DFT calculations are finished, run this part of the script with `sbatch end_script.sh`
- The script should make the `dft_results` folder with the extracted properties

#### Please note:
- That the functionality was added that converts Gaussian output and checkpoint files (.out and .chk) to .log and .fchk files, that are needed for running the script. If your Gaussian job already gives these files, there's no need for this part in `run_end.py`. However, you can anyways run it, it will just skip them.
- That in order to run this script, you need to obtain DFTD3 and Multiwfn software from respective websites (see `config.yaml`). All other are installed in the venv.

## Note
- The memory and cpu requests are still not user definable, and should be done in the code. Currently, Gaussian jobs run with `--ntasks=1`, `--cpus-per-task-16` and `--mem-per-cpu=1100` in the bash script, as defined in the `gsub` submission script of the STUDIX cluster, or `%nproc=16` and `%mem=16GB` in the Gaussian input file in the current implementation. You can modify this in the ``PL_gaussian_input_200411.py`` file in functions `def get_link0(n)` and `def write_coms(..)`.

----------------------------
<br><br>

# Original readme

The full kraken workflow involves three steps. This folder contains scripts and information for steps 2 and 3. 
## Step 1. CREST conformer search + xTB calculations
- see folder for instructions and information

## Step 2. conformer selection + DFT calculations
- input: results (ymls) from XTB workflow portion
- recommended usage
	- edit conformer_selection.py to refer to example_ligands.txt
	- replace sub16_PL with equivalent submission script
	- add Multiwfn 3.7, dftd3, and dftd4 to Pint directory
	- submit job as `sbatch conf_script.sh` or equivalent

## Step 3. gather and condense properties 
- input: results from conformer selection + DFT calculations workflow portion
- recommended usage
	- submit job as `sbatch end_script.sh` or equivalent 

	
## Requirements
- xTB
- crest
- Gaussian
- openbabel
- python 3.6
- morfeus
- rdkit
- cython
- numpy, scipy, yaml, seaborn, time, r-uuid, r-getpass, pathlib, cclib, pyvista, vtk, sympy, tqdm, dataclasses, fire, joblib

---

note: v0 scripts contain user-specific paths. these will be condensed in a future update. path locations are listed below. 
- ded.py							              lines 13, 14
- pint_main.py						          lines 36, 63
- conf_script.sh 					          lines 28, 34
- conformer_selection.py		      	line  15
- utils.py							            lines 20, 23, 26
- run_end.py						            lines 12, 61
- end_script.sh						          lines 37, 52, 53, 58
- PL_conformer_selection_200411.py	lines 834, 836, 
