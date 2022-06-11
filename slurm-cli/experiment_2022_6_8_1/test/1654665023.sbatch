#!/bin/bash
#SBATCH -J eva_baseline
#SBATCH -p critical
#SBATCH -t 01:30:00
#SBATCH --cpus-per-task=4
#SBATCH --output=%j.out
#SBATCH --error=%j.err
set -e
source ~/.bashrc
conda activate torchbenchmark
cd ~/benchmark
proxychains4 -f ~/.proxychains_conf/node_to_login.conf python /public/home/qinfr/benchmark/test_running_profile.py  timm_efficientnet 64 822
