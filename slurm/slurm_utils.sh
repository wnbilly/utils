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

# Parameters
SQUEUE_REFRESH_RATE=3 # Refresh rate of squeue in seconds
NB_LINES_STAIL=25 # Number of lines to show in stail

# Better sbatch to store the latest job id and a better display of the output
function run_sbatch() {
	output=$(sbatch "$1")
	echo -e "${YELLOW}$output${NC}"	
	job_id="${output//[!0-9]/}"
	export LATEST_JOB="$job_id"
}

# alias sbatch="run_sbatch" # May cause issues with sbatch command

# Easier access to the command
alias squ="squeue -u $USER -i $SQUEUE_REFRESH_RATE"

# sljob to manually set LATEST_JOB
function sljob() {
  export LATEST_JOB="$1"
}

# stail to tail the latest job or the logs of a specific job if provided
# It is supposed to be launched from slurm_scripts
function stail() {
  if [[ -z $1 ]]; then
    # If LATEST_JOB contains a job id
    if [[ -n $LATEST_JOB ]]; then
      latest_file=logs/job$LATEST_JOB.out
    # Else get the last modified file
    else
      latest_file=$(ls -t logs/job*.out | head -n 1)
    fi
    echo -e "${YELLOW}---$latest_file---${NC}"
    tail -f -n $NB_LINES_STAIL "$latest_file"
  else
    echo -e "${YELLOW}---logs/job$1.out---${NC}"
    tail -f -n $NB_LINES_STAIL "logs/job$1.out" # Requires format jobXXX.out
  fi
}

# sout to show .out of your last job
# It is supposed to be launched from slurm_scripts. I kept sout as tail only shows the last 10 lines by default
function sout() {
  if [[ -z $1 ]]; then
    # If LATEST_JOB contains a job id
    if [[ -n $LATEST_JOB ]]; then
      latest_file=logs/job$LATEST_JOB.out
    # Else get the last modified file
    else
      latest_file=$(ls -t logs/job*.out | head -n 1)
    fi
    echo -e "${YELLOW}---$latest_file---${NC}"
    cat "$latest_file"
    echo -e "${YELLOW}---$latest_file---${NC}"
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
