#!/bin/bash

#SBATCH --output=logs/job%A%a.out   # .out file %A : jobid %a : arrayid
#SBATCH --error=logs/job%A%a.out    # error file set to the same as .out file
#SBATCH --time=20:00:00            # max time allocated
#SBATCH --partition=P100		   # partition type
#SBATCH --nodes=1                  # number of nodes
#SBATCH --gpus=1                   # number of GPU
#SBATCH --cpus-per-task=8          # number of CPU per task
#SBATCH --array=1-4%4          # array=<start>-<end>[:<step>][%<maxParallel>] end included --> https://slurm.schedmd.com/job_array.html

# Activate echo of commands
set -x

# Activate bash and virtual environment
eval "bash"
eval "$(conda shell.bash hook)"
conda activate virtual_env_name # replace with your virtual environment name

# Create logs directory if it doesn't exist as following :
# slurm_scripts
# ├── logs
# │     ├── job1.out
# │     ├── job2.out
# │     └── ....
mkdir -p ./logs

# Specify the path to the config file supposing the following structure :
# slurm_scripts
# ├── logs
# │     ├── job1.out
# │     ├── job2.out
# │     └── ....
# └── configs
#       ├── config.txt

config="./configs/config.txt"

# Acquire the parameters line from the config file
param=$(sed -n ${SLURM_ARRAY_TASK_ID}p  $config )

# cd
# commands ...

# Launch python scripts with -u for unbuffered stdin, stdout, stderr
srun python3 -u script.py $param
