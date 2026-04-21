#!/bin/bash
#SBATCH --job-name=grover
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=02:00:00
#SBATCH --output=output_%j.log

echo "Start job"
echo "Running on $(hostname)"
echo "Current directory: $(pwd)"

module purge
module load Anaconda/3-2023.09-0

source activate env-ml

which python
python --version

cd /mgpfs/home/mkhairiansyah/grover_project

python run_grover.py

echo "Job finished"