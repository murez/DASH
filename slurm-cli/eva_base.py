import argparse
import parse
import tasksubmit
import time
import monitor
import scheduler
import random

if __name__ == "__main__":
    index = 1
    with open("/public/home/qinfr/DASH/test/out", "r") as f:
        for line in f.readlines():
            args = line.strip().split(",")
            print(args)
            jobID = index
            index = index + 1
            # slurm_id = tasksubmit.job_profile(args.input, jobID)
            if args[0] == "NVIDIAGeForceGTX1080":
                scheduler.EstimateTime(jobID, "/public/home/qinfr/DASH/test/{}.sbatch".format(args[1]), random.randint(1,100),1145141919810,1145141919810,1145141919810)
            if args[0] == "NVIDIAGeForceRTX2080Ti":
                scheduler.EstimateTime(jobID, "/public/home/qinfr/DASH/test/{}.sbatch".format(args[1]),1145141919810,1145141919810,1145141919810, random.randint(1,100))
            if args[0] == "NVIDIATITANRTX":
                scheduler.EstimateTime(jobID, "/public/home/qinfr/DASH/test/{}.sbatch".format(args[1]),1145141919810,1145141919810, random.randint(1,100),1145141919810)
    # print("EstimateTime: {}".format(ddl))s
    print("Do you like what you see?")
