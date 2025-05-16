#!/bin/bash                 

#SBATCH --job-name=kraken_single_run_Ni
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00 
#SBATCH --qos=1day
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=uros.stojiljkovic@unibas.ch
#SBATCH --output=kraken_single_run_Ni.out
#SBATCH --error=kraken_single_run_Ni.err 

###======================================================================###
#=======ADAPT THE SBATCH PART AND ENVIRONMENT PART FOR YOUR CLUSTER========#
###======================================================================###

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate kraken

###======================================================================###
#==================SET VARIABLES FOR THE CALCULATION HERE==================#
#==============NTASK SHOULD BATCH NTASK IN THE SBATCH SECTION==============#
#=====IDX IS THE ROW NUMBER OF THE LIGAND IN INPUT.CSV STARTING FROM 0=====#
#========THE JOB_TYPE CAN BE 'Ni' OR 'noNi' AS IN THE ORIGINAL CODE========#
###======================================================================###

export NTASKS=16
idx=1
job_type=noNi  # Change to 'noNi' to run the other job type


###=====================================================================###
#===============NO USER INPUT IS REQUIRED AFTER THIS LINE===============###
###=====================================================================###
base_job_name=${SLURM_JOB_NAME:-default_job}
job_name="${base_job_name}_${job_type}"

start_time=$(date +%s)

/usr/bin/time -v python run_kraken.py -idx ${idx} input.csv ${job_type} \
    1> "${job_name}_output.log" \
    2> "${job_name}_resource_usage.log"

end_time=$(date +%s)
runtime=$((end_time - start_time))

echo "Total runtime: $runtime seconds" >> "${job_name}_resource_usage.log"
echo "SLURM Job ID: $SLURM_JOB_ID" >> "${job_name}_resource_usage.log"
echo "SLURM Node List: $SLURM_NODELIST" >> "${job_name}_resource_usage.log"
echo "SLURM Tasks Per Node: $SLURM_TASKS_PER_NODE" >> "${job_name}_resource_usage.log"
