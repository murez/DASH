#!/bin/bash
#SBATCH -J collect_daa
#SBATCH -p critical
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=all
##SBATCH --mail-user=YOU@MAIL.COM
#SBATCH -N 1
##SBATCH --nodelist=ai_gpu19
#SBATCH -t 15-00:00
#SBATCH --gres=gpu:NVIDIAGeForceGTX1080:1
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#TAG=V100
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.free,memory.used,temperature.gpu,power.draw --format=csv -lms 100 > /public/home/qinfr/DASH/test/test.log &
hostname
cat /public/home/qinfr/DASH/test/input
sleep 1m