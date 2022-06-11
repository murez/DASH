import argparse
import parse
import tasksubmit
import time
import monitor
import scheduler
import datetime

if __name__ == "__main__":

    # Parse arguments
    # Usage: python slurm-cli.py a.run
    # It will parse a.run and do next
    # Value of args.input is "a.run"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="input file")
    args = parser.parse_args()
    parse.parse(args.input)
    jobID = int(time.time())
    print("File: ", args.input)
    # FIXME: 开启 profile
    slurm_id = tasksubmit.job_profile(args.input, jobID)
    print("Profiling",end="")
    time.sleep(1)
    while(slurm_id in monitor.checkUserQueue()):
        # print(monitor.checkUserQueue())
        print(".",end="")
        time.sleep(1)

    #TODO: 将完成的 profile 传给 predictor
    # "/public/home/qinfr/DASH/slurm-cli/tmp/{}.log".format(jobID)

    print("\nProfiling finished.")

    est_time = []
    with open("{}.out".format(slurm_id), "r") as logfile:
        for line in logfile.readlines():
            if line.startswith("estimate_time:"):
                line = line.strip().strip("estimate_time:").strip().split(",")
                est_time = [int(i) for i in line]
                print("est_time: {}".format(est_time))
                break

    # ddl = scheduler.EstimateTime(jobID, args.input, est_time[0],est_time[1],est_time[2],est_time[3])
    try:
        ddl = scheduler.EstimateTime(jobID, args.input, est_time[0],est_time[2],est_time[2],est_time[1])
    except Exception as e:
        print(e)
        scheduler.EstimateTime(jobID, args.input, 5400,5400,5400,5400)
    print("The Time is: {}",datetime.datetime.utcfromtimestamp(int(time.time()) + 8*60*60).strftime('%Y-%m-%dT%H:%M:%SZ'))
    print("EstimateTime: {}".format(ddl))
    print("Do you like what you see?")
