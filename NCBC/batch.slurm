#!/bin/bash -l
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --output=/home/t/temma-fujishige/logs/slurm-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=temma-fujishige@oist.jp

cd /home/t/temma-fujishige/LabRotations/NCBC/src
rye run python runner.py
