# Kraken fork - Summary
This repository is a fork of the original Kraken workflow for computing electronic and steric features of monodentate phosphines. The following changes and improvements have been made in this fork:

- Modifications, bug fixes and error corrections of the original code
- Submission of all the ligands from the input file in the first, xTB part.
- User-definable path definition and submission script handling in the `submit_input.py` file for the first, xTB part
- User-definable path configuration via a YAML file for the second, DFT part
- Unused file removal
- YAML files added for conda venv installations
- Enanced error handling
- Documentation update
- Optmization for the clusters of the University of Basel, i.e. SciCORE for the first part and STUDIX for the second part.

The workflow is divided into two main portions, each with its own documentation:

1. **conf_search_and_xTB:**  
   - CREST conformer search and xTB calculations  

2. **conf_selection_and_DFT:**  
   - Conformer selection, DFT calculations, and property extraction  

## Usage
1. **Clone repository and create venvs**
- Firstly, clone the repository and create the environments with the help of `kraken_xtb.yml` and `kraken_dft.yaml` files.
<br><br>
2. **In part 1, `conf_search_and_xTB`**
- Modify the `submit_input.py` or the `bash_single_job.sh` file for the needs of your cluster.
<br><br>
3. **In part 2, `conf_selection_and_DFT`**
- Modify the `config.yaml` file 
- Update `conf_script.sh` and `end_script.sh` for your cluster's SLURM configuration and environment setup.
<br><br>
4. **Run the workflow steps**
- Step 1: Run CREST/xTB either through the bash script, or the `submit_input.py` file
- Step 2: Select conformers and run DFT calculations through `conf_script.sh` file
- Step 3: Extract the DFT properties. through `end_script.sh`

<br>
See the respective README files in each workflow folder for detailed instructions.

## Notes

- The code is provided "as-is." Minor edits may be required to tailor scripts for different computational systems.
<br><br><br><br>
----------
# Original readme
# kraken
Code to compute electronic and steric features to create a database of ligands and their properties.

This workflow is divided into two portions: conf_search_and_xTB and conf_selection_and_DFT. Each portion has a readme with further information.

Code is provided "as-is." Minor edits may be required to tailor scripts for different computational systems. 

https://doi.org/10.1021/jacs.1c09718
