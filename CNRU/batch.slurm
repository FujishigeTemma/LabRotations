#!/bin/bash -l
#SBATCH --partition=taniu
#SBATCH --time=3-00:00:00
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-gpu=9
#SBATCH --mem=400G
#SBATCH --output=/home/t/temma-fujishige/logs/slurm-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=temma-fujishige@oist.jp

cd /home/t/temma-fujishige/LabRotations/CNRU
rye run python src/cli.py train-decoder -c train.toml