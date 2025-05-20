#!/bin/bash                 

#SBATCH --job-name=kraken_conf_script
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mail-type=None
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=short
#SBATCH --output=kraken_conf_script.out
#SBATCH --error=kraken_conf_script.err 

module load gaussian
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate kraken

# Run the script
python conformer_selection.py