import subprocess
import time
import os

def job_profile(path: str, job_name: int) -> int:
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with open(path, 'r') as f:
        contents = f.readlines()

    to_insert = 0
    for to_insert, line in enumerate(contents):
        if not line.lstrip().startswith('#'):
            break;

    # if not contents[to_insert].lstrip().startswith('(timeout 1m nvidia-smi'):
    #     contents.insert(to_insert, '(timeout 1m nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.free,memory.used,temperature.gpu,power.draw --format=csv -lms 100 > tmp/{}.log) &\n'.format(job_name))

    contents.insert(to_insert,"#SBATCH --gres=gpu:NVIDIAGeForceGTX1080:1\nexport DASH_PROFILER_ENABLED=1\n")#TODO: EXPORT
    with open('tmp/{}.profile.run'.format(job_name), 'w+') as f:
        f.writelines(contents)

    response = subprocess.getoutput("sbatch tmp/{}.profile.run".format(job_name));
    job_id = response.split(' ')[-1].strip()
    print("The job to profile is ",job_id)
    print(response)
    return int(job_id)

def change_node(path: str, job_name: int, new_card: str) -> int:
    print(path, job_name, new_card)
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    with open(path, 'r') as f:
        
        contents = f.readlines()

    to_insert = 0
    for to_insert, line in enumerate(contents):
        if line.lstrip().startswith('#'):
            if line.lstrip().startswith('#SBATCH --gres=gpu:'):
                print("remove old card config: ", contents[to_insert])
                del contents[to_insert]
                break;
        else:
            break;

    contents.insert(to_insert, '#SBATCH --gres=gpu:{}:1\n'.format(new_card))
    with open('tmp/{}.run'.format(job_name), 'w+') as f:
        f.writelines(contents)

    response = subprocess.getoutput("sbatch tmp/{}.run".format(job_name))
    job_id = response.split(' ')[-1].strip()
    print("The job to run ",job_id)
    print(response)
    return int(job_id)

if __name__ =="__main__":
    id_profile = job_profile("/public/home/qinfr/DASH/test/test.sbatch", 1)
    id = change_node("/public/home/qinfr/DASH/test/test.sbatch", 1, 'ai_gpu18')