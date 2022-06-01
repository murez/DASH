#!/bin/bash
#SBATCH -J collect_daa
#SBATCH -p critical
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=all
##SBATCH --mail-user=YOU@MAIL.COM
#SBATCH -N 1
##SBATCH --nodelist=ai_gpu19
#SBATCH -t 15-00:00
#SBATCH --gres=gpu:NVIDIATITANXp:1
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#TAG=V100

hostname