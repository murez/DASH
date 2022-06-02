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
            jobs.FinishedJob(job[0])
    

if __name__ == "__main__":
    while(True):
        checkRunningQueue()
        time.sleep(1)
        scheduler.SchedulerP()
        time.sleep(1)
        scheduler.Scheduler()
        time.sleep(1)
        






