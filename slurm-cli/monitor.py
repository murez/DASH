import scheduler
import subprocess
import jobs
import re
import time

def checkUserQueue() -> list:
    ret = []
    squeue = subprocess.getoutput("squeue -u $USER")
    squeues = squeue.split('\n')
    squeues = squeues[1:]
    for line in squeues:
        line=line.strip()
        line = re.sub('\s+', ' ', line)
        jobinfo = [x.strip() for x in line.split(' ')]
        ret.append(jobinfo[0])
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
    waittime = 5
    while(True):
        checkRunningQueue()
        time.sleep(waittime)
        scheduler.SchedulerP()
        time.sleep(waittime)
        scheduler.Scheduler()
        time.sleep(waittime)
        






