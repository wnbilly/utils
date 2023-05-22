#!/bin/bash

#SBATCH --output=logs/job%j.out   # .out file %j : jobid
#SBATCH --error=logs/job%j.out    # error file set to the same as .out file
#SBATCH --time=20:00:00            # max time allocated
#SBATCH --partition=P100		   # partition type
#SBATCH --nodes=1                  # number of nodes
#SBATCH --gpus=1                   # number of GPU
#SBATCH --cpus-per-task=8          # number of CPU per task

# Activate echo of commands
set -x

# Create logs directory if it doesn't exist as following :
# slurm_scripts
# ├── logs
# │     ├── job1.out
# │     ├── job2.out
# │     └── ....
mkdir -p ./logs

# Activate bash and virtual environment
eval "bash"
eval "$(conda shell.bash hook)"
conda activate virtual_env_name # replace with your virtual environment name

# cd
# commands ...

# Launch python scripts with -u for unbuffered stdin, stdout, stderr
srun python3 -u script.py --arg1 arg1 --arg2 arg2