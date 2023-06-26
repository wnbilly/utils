# Slurm utils

# Requires slurm scripts to be in a slurm_scripts folder like following :
# slurm_scripts
# ├── logs
# │     ├── job1.out
# │     ├── job2.out
# │     └── ....

# Fancy colors for a better experience
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Better sbatch to store the latest job id and a better display of the output
function run_sbatch() {
	output=$(sbatch "$1")
	echo -e "${YELLOW}$output${NC}"	
	job_id="${output//[!0-9]/}"
	export LATEST_JOB="$job_id"
}

# alias sbatch="run_sbatch" # May cause issues with sbatch command

# sout to show .out of your last job
# It is supposed to be launched from slurm_scripts. I kept sout as tail only shows the last 10 lines by default
function sout() {
  if [[ -z $1 ]]; then
    latest_file=$(ls -t logs/job*.out | head -n 1)
    echo -e "${YELLOW}---$latest_file---${NC}"
    cat "$latest_file"
    echo -e "${YELLOW}---logs/job$1.out---${NC}"
  else
    echo -e "${YELLOW}---logs/job$1.out---${NC}"
    cat "logs/job$1.out" # Requires format jobXXX.out
    echo -e "${YELLOW}---logs/job$1.out---${NC}"
  fi
}

# ssj to use 'scontrol show job JOB_ID' with LATEST_JOB

function ssj() {
  if [ -n "$1" ]; then
    echo -e "${YELLOW}---job $1---${NC}"
    scontrol show job "$1"
    echo -e "${YELLOW}---job $1---${NC}"
  elif [ -n "$LATEST_JOB" ]; then
    echo -e "${YELLOW}---job $LATEST_JOB---${NC}"
    scontrol show job "$LATEST_JOB"
    echo -e "${YELLOW}---job $LATEST_JOB---${NC}"
  else
    echo "Please provide a job id as LATEST_JOB is null."
  fi
}

# Easier access to the command
alias squ="squeue -u $USER -i 3"

# stail to tail the latest job or the logs of a specific job if provided
# It is supposed to be launched from slurm_scripts
function stail() {
  if [[ -z $1 ]]; then
    latest_file=$(ls -t logs/job*.out | head -n 1)
    echo -e "${YELLOW}---$latest_file---${NC}"
    tail -f -n 25 "$latest_file"
  else
    echo -e "${YELLOW}---logs/job$1.out---${NC}"
    tail -f -n 25 "logs/job$1.out" # Requires format jobXXX.out
  fi
}

# Disclaimer : I chose to use the latest file for stail and showout but LATEST_JOB could be used as well like in ssj
