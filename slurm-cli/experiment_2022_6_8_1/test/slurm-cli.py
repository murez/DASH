import argparse
import parse
import tasksubmit
import time
import monitor
import scheduler

if __name__ == "__main__":

    with open("/public/home/qinfr/DASH/test/out", "r") as f:
        for line in f.readlines():
            args = line.strip().split(",")
            jobID = int(time.time())
            # slurm_id = tasksubmit.job_profile(args.input, jobID)
            if args[1] == "NVIDIAGeForceGTX1080":
                scheduler.EstimateTime(jobID, args.input, 70,70,70,70)
    print("EstimateTime: {}".format(ddl))
    print("Do you like what you see?")
