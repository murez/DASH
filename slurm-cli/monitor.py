import scheduler
import subprocess
import jobs
import re
import time
import datetime

def checkUserQueue() -> list:
    ret = []
    squeue = subprocess.getoutput("squeue -u $USER")
    squeues = squeue.split('\n')
    squeues = squeues[1:]
    for line in squeues:
        line=line.strip()
        line = re.sub('\s+', ' ', line)
        jobinfo = [x.strip() for x in line.split(' ')]
        ret.append(int(jobinfo[0]))
    return ret

def checkRunningQueue():
    _jobs = jobs.GetAllRunningJobs()
    for job in _jobs:
        if job[3] not in checkUserQueue():
            print("JobID {} has finished.".format(job[0]))
            if job[4] == jobs.P_CLUSTERS:
                jobs.FinishedJobPCluster(job[0])
            if job[4] == jobs.E_CLUSTERS:
                jobs.FinishedJob(job[0])
    

if __name__ == "__main__":
    waittime = 3
    while(True):
        print("The Time is: {}",datetime.datetime.utcfromtimestamp(int(time.time()) + 8*60*60).strftime('%Y-%m-%dT%H:%M:%SZ'))
        checkRunningQueue()
        time.sleep(waittime)
        scheduler.SchedulerP()
        time.sleep(waittime)
        scheduler.Scheduler()
        time.sleep(waittime)
        # scheduler.SchedulerN()
        # time.sleep(waittime)
        






