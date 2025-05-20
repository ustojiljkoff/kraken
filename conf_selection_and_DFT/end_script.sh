#!/bin/bash

#SBATCH --job-name=end_script
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mail-type=None
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=short
#SBATCH --output=end_script.out
#SBATCH --error=end_script.err

source $HOME/miniconda3/etc/profile.d/conda.sh
module load gcc
module load gaussian #modified for studix

conda activate kraken

export OMP_NUM_THREADS=80
export MKL_NUM_THREADS=80
export OMP_STACKSIZE=5G
export KMP_STACKSIZE=5G

ulimit -s unlimited

python run_end.py $1 $2
