import csv
from pathlib import Path
import subprocess
import os

def generate_and_submit_jobs(
    input_csv: str,
    job_dir: Path,
    metals: list = ["Ni", "noNi"],
    ntasks: int = 16,
    mem_per_cpu: str = "10G",
    cpus_per_task: int = 1,
    time: str = "24:00:00",
    qos: str = "1day",
    mail_type: str = "END,FAIL,TIME_LIMIT",
    email: str = "uros.stojiljkovic@unibas.ch",
    nodes: int = 1,
    conda_env: str = "kraken",
    submit: bool = True,
    partition: str = "short",
):
    """
    Generates and submits SLURM job scripts based on the provided parameters.
    Args:
        input_csv (str): Path to the input CSV file.
        job_dir (Path): Directory to save the job scripts, ideally the same directory.
        metals (list): Job types. Ni and noNi per defult.
        ntasks (int): Number of tasks for SLURM.
        mem_per_cpu (str): Memory per CPU for SLURM.
        cpus_per_task (int): CPUs per task for SLURM.
        time (str): Time limit for SLURM jobs.
        qos (str): Quality of Service for SLURM jobs.
        mail_type (str): Mail type for SLURM notifications.
        email (str): Email address for SLURM notifications.
        nodes (int): Number of nodes for SLURM jobs.
        conda_env (str): Conda environment to activate in the job script, name of your kraken env.
        submit (bool): Whether to submit the jobs immediately or not.
        partition (str): Partition name for SLURM jobs."""
    
    #job_dir.mkdir(exist_ok=True)
    if mail_type == "None":
        mail_user = ""
    elif mail_type == "END,FAIL,TIME_LIMIT":
        mail_user = f"#SBATCH --mail-user={email}"
    else:
        mail_type = "None"
        mail_user = ""

    print(f"""
Submitting jobs to the cluster with the following configuration:
========================================
Input CSV: {input_csv}
Job Directory: {job_dir}
Metals: {metals}
ntasks: {ntasks}
Memory per CPU: {mem_per_cpu}
CPUs per Task: {cpus_per_task}
Mail type: {mail_type}
Nodes: {nodes}
Time: {time}
QOS: {qos}
Email: {email}
Submit: {submit}
========================================
""")

    with open(input_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=0):
            mol_id = row["ID"]

            for metal in metals:
                job_name = f"kraken_{mol_id}_{metal}"
                job_script_path = job_dir / f"{job_name}.sh"

                script_content = f"""#!/bin/bash

#SBATCH --job-name={job_name}
#SBATCH --nodes={nodes}
#SBATCH --ntasks={ntasks}
#SBATCH --cpus-per-task={cpus_per_task}
#SBATCH --mem-per-cpu={mem_per_cpu}
#SBATCH --time={time}
#SBATCH --qos={qos}
#SBATCH --mail-type={mail_type}
{mail_user}
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate {conda_env}

start_time=$(date +%s)

/usr/bin/time -v python run_kraken.py -idx {idx} {input_csv} {metal} 1> {job_name}_output.log 2> {job_name}_resource_usage.log

end_time=$(date +%s)
runtime=$((end_time - start_time))

echo "Total runtime: $runtime seconds" >> {job_name}_resource_usage.log
echo "SLURM Job ID: $SLURM_JOB_ID" >> {job_name}_resource_usage.log
echo "SLURM Node List: $SLURM_NODELIST" >> {job_name}_resource_usage.log
echo "SLURM Tasks Per Node: $SLURM_TASKS_PER_NODE" >> {job_name}_resource_usage.log
"""

                print(f"Generating job script for {job_name}")
                with open(job_script_path, "w") as f:
                    f.write(script_content)
                job_script_path.chmod(0o755)

                if submit:
                    print(f"Submitting job {job_name}...")
                    subprocess.run(["sbatch", str(job_script_path)], check=True)

    print(f"All jobs submitted.")

# ====== USAGE ======
if __name__ == "__main__":
    generate_and_submit_jobs(
        input_csv="input.csv",
        job_dir=Path.cwd(),
    )
