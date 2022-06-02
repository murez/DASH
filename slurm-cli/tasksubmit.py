import subprocess
import time


def TaskSubmit(path: str) -> str:
    response = subprocess.getoutput("sbatch {}".format(path));
    job_id = str(response).split(' ')[-1].strip()
    print("Job ID is",job_id)
    print(str(response))
    return job_id

def GetTaskOutputByID(id: int):
    ret = subprocess.check_output("squeue -j {}".format(id), shell=True);
    with open("{}.out".format(id), 'r+') as f:
        print(f.read())

if __name__ =="__main__":
    id = TaskSubmit("/public/home/qinfr/DASH/test/test.sbatch")
    print(id)