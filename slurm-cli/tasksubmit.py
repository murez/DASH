import subprocess
import time
import os

def job_profile(path: str, job_name: int):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with open(path, 'r') as f:
        contents = f.readlines()

    to_insert = 0
    for to_insert, line in enumerate(contents):
        if not line.lstrip().startswith('#'):
            break;

    if not contents[to_insert].lstrip().startswith('(timeout 1m nvidia-smi'):
        contents.insert(to_insert, '(timeout 1m nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.free,memory.used,temperature.gpu,power.draw --format=csv -lms 100 > tmp/{}.log) &\n'.format(job_name))
    with open('tmp/{}.profile.run'.format(job_name), 'w+') as f:
        f.writelines(contents)

    response = subprocess.getoutput("sbatch tmp/{}.profile.run".format(job_name));
    job_id = response.split(' ')[-1].strip()
    print("The Job to profile is",job_id)
    print(response)
    return job_id

def change_node(path: str, job_name: int, new_node: str):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with open(path, 'r') as f:
        contents = f.readlines()

    to_insert = 0
    for to_insert, line in enumerate(contents):
        if line.lstrip().startswith('#'):
            if line.lstrip().startswith('#SBATCH --nodelist='):
                to_insert -= 1
                contents.remove(to_insert)
                break;
        else:
            break;

    contents.insert(to_insert, '#SBATCH --nodelist={}\n'.format(new_node))
    with open('tmp/{}.run'.format(job_name), 'w+') as f:
        f.writelines(contents)

    response = subprocess.getoutput("sbatch tmp/{}.run".format(job_name));
    job_id = response.split(' ')[-1].strip()
    print("The Job to run",job_id)
    print(response)
    return job_id

if __name__ =="__main__":
    id_profile = job_profile("/public/home/qinfr/DASH/test/test.sbatch", 1)
    id = change_node("/public/home/qinfr/DASH/test/test.sbatch", 1, 'ai_gpu18')