import argparse
import parse
import tasksubmit
import time
import monitor
import scheduler

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

    # FIXME: 开启 profile
    slurm_id = tasksubmit.job_profile(args.input, jobID)
    print("Profiling",end="")
    time.sleep(1)
    while(slurm_id in monitor.checkUserQueue()):
        print(monitor.checkUserQueue())
        print(".",end="")
        time.sleep(1)

    #TODO: 将完成的 profile 传给 predictor
    # "/public/home/qinfr/DASH/slurm-cli/tmp/{}.log".format(jobID)

    print("\nProfiling finished.")
    ddl = scheduler.EstimateTime(jobID, args.input, 70,70,70,70)
    print("EstimateTime: {}".format(ddl))
    print("Do you like what you see?")
