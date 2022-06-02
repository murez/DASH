import subprocess
import time

def job_profile(path: str, job_name: int):
    with open(path, 'r') as f:
        contents = f.readlines()

    to_insert = 0
    for line in contents:
        if not line.startswith('#'):
            break;
        else:
            to_insert += 1

    if not contents[to_insert].startswith('(timeout 1m nvidia-smi'):
        contents.insert(to_insert, '(timeout 1m nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.free,memory.used,temperature.gpu,power.draw --format=csv -lms 100 > tmp/{}.log) &\n'.format(job_name))
    with open('tmp/{}.run'.format(job_name), 'x') as f:
        f.writelines(contents)

    response = subprocess.getoutput("sbatch tmp/{}.run".format(job_name));
    job_id = str(response).split(' ')[-1].strip()
    print("The Job to profile is",job_id)
    print(str(response))
    return job_id

def GetTaskOutputByID(id: int):
    ret = subprocess.check_output("squeue -j {}".format(id), shell=True);
    with open("{}.out".format(id), 'r+') as f:
        print(f.read())

if __name__ =="__main__":
    id = job_profile("/public/home/qinfr/DASH/test/test.sbatch", 1)