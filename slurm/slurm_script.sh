#!/bin/bash

#SBATCH --output=logs/job%j.out   # fichier de sortie
#SBATCH --error=logs/job%j.out    # fichier d'erreur
#SBATCH --time=20:00:00            # temps maximal d'allocation
#SBATCH --partition=A40		   # type de partition
#SBATCH --nodes=1                  # nombre de noeuds
#SBATCH --gpus=2                   # nombre de GPU
#SBATCH --cpus-per-task=8          # nombre de CPU par tâche

# Create logs directory if it doesn't exist as following :
# slurm_scripts
# ├── logs
# │     ├── job1.out
# │     ├── job2.out
# │     └── ....
mkdir -p ./logs

# Necessary to activate conda environment
bash
eval "$(conda shell.bash hook)"
conda activate datum

# cd
# export

# Activate echo of commands
set -x

# Launch python scripts with -u for unbuffered stdin, stdout, stderr
srun python3 -u script.py --arg1 arg1 --arg2 arg2