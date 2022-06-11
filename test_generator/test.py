from pyexpat import model
import time
import random
import numpy as np

model = ["resnext50_32x4d",
"squeezenet1_1",
"vision_maskrcnn",
"dcgan",
"vgg16",
"resnet18",
"resnet50",
"yolov3",
"mobilenet_v2",
"mobilenet_v3_large",
"pytorch_unet",
"vision_maskrcnn",
"hf_Bert", # NLP
"densenet121",
"shufflenet_v2_x1_0",
"hf_GPT2", # NLP
"attention_is_all_you_need_pytorch", # NLP
"drq",
"timm_vision_transformer",
"timm_efficientnet",
"hf_T5"] # NLP

NVIDIAGeForceGTX1080=[]

with open("/public/home/qinfr/DASH/NVIDIAGeForceGTX1080.txt") as f:
    for line in f.readlines():
        args = line.strip().split(" ")
        NVIDIAGeForceGTX1080.append([args[0], args[1]])
        
NVIDIAGeForceRTX2080Ti = []
with open("/public/home/qinfr/DASH/NVIDIAGeForceRTX2080Ti.txt") as f:
    for line in f.readlines():
        args = line.strip().split(" ")
        NVIDIAGeForceRTX2080Ti.append([args[0], args[1]])

NVIDIATITANRTX = []
with open("/public/home/qinfr/DASH/NVIDIATITANRTX.txt") as f:
    for line in f.readlines():
        args = line.strip().split(" ")
        NVIDIATITANRTX.append([args[0], args[1]])

index = 0
for i in range(0,12):
    mu, sigma = 1100, 100 #epoch
    s = np.random.normal(mu, sigma, 12)
    mu, sigma = 5500, 400 # datasize
    s2 = np.random.normal(mu, sigma, 12)
    t = int(time.time())
    model_random_index = random.randint(0, len(model)-1)
    model_name = model[model_random_index]
    model_batch_size = []
    for i in NVIDIAGeForceGTX1080:
        if i[0] == model_name:
            model_batch_size.append(i[1])
    # print("model_name:",model_name,"model_batch_size:", model_batch_size)
    model_batch_size = model_batch_size[t % 1]
    with open("./{}.sbatch".format(t), "w") as f:
        f.write('''#!/bin/bash\n''')
        f.write('''#SBATCH -J eva_baseline\n''')
        f.write('''#SBATCH -p critical\n''')
        f.write('''#SBATCH -t 01:30:00\n''')
        f.write('''#SBATCH --cpus-per-task=4\n''')
        f.write('''#SBATCH -o ./{}.out\n'''.format(t))
        f.write('''#SBATCH -e ./{}.err\n'''.format(t))
        f.write('''set -e\n''')
        f.write('''source ~/.bashrc\n''')
        f.write('''conda activate torchbenchmark\n''')
        f.write('''cd ~/benchmark\n''')
        f.write('''proxychains4 -f ~/.proxychains_conf/node_to_login.conf python /public/home/qinfr/benchmark/test_running_profile.py  {} {} {} \n'''.format(model_name ,model_batch_size, int(s[index] *s2[index] / int(model_batch_size) / 10)))
    print("{},{}".format("NVIDIAGeForceGTX1080", t))
    index = index+1
    time.sleep(2)

index = 0
for i in range(0,24):
    mu, sigma = 1100, 100
    s = np.random.normal(mu, sigma, 24)
    mu, sigma = 5500, 400 # datasize
    s2 = np.random.normal(mu, sigma, 24)
    t = int(time.time())
    model_random_index = random.randint(0, len(model)-1)
    model_name = model[model_random_index]
    model_batch_size = []
    for i in NVIDIAGeForceRTX2080Ti:
        if i[0] == model_name:
            model_batch_size.append(i[1])
    # print("model_name:",model_name,"model_batch_size:", model_batch_size)
    model_batch_size = model_batch_size[t % 1]
    with open("./{}.sbatch".format(t), "w") as f:
        f.write('''#!/bin/bash\n''')
        f.write('''#SBATCH -J eva_baseline\n''')
        f.write('''#SBATCH -p critical\n''')
        f.write('''#SBATCH -t 01:30:00\n''')
        f.write('''#SBATCH --cpus-per-task=4\n''')
        f.write('''#SBATCH -o ./{}.out\n'''.format(t))
        f.write('''#SBATCH -e ./{}.err\n'''.format(t))
        f.write('''set -e\n''')
        f.write('''source ~/.bashrc\n''')
        f.write('''conda activate torchbenchmark\n''')
        f.write('''cd ~/benchmark\n''')
        f.write('''proxychains4 -f ~/.proxychains_conf/node_to_login.conf python /public/home/qinfr/benchmark/test_running_profile.py  {} {} {} \n'''.format(model_name ,model_batch_size, int(s[index] *s2[index] / int(model_batch_size) / 10)))
    print("{},{}".format("NVIDIAGeForceRTX2080Ti", t))
    index = index+1
    time.sleep(2)

index = 0
for i in range(0,24):
    mu, sigma = 1100, 100
    s = np.random.normal(mu, sigma, 24)
    mu, sigma = 5500, 400 # datasize
    s2 = np.random.normal(mu, sigma, 24)
    t = int(time.time())
    model_random_index = random.randint(0, len(model)-1)
    model_name = model[model_random_index]
    model_batch_size = []
    for i in NVIDIATITANRTX:
        if i[0] == model_name:
            model_batch_size.append(i[1])
    # print("model_name:",model_name,"model_batch_size:", model_batch_size)
    model_batch_size = model_batch_size[t % 1]
    with open("./{}.sbatch".format(t), "w") as f:
        f.write('''#!/bin/bash\n''')
        f.write('''#SBATCH -J eva_baseline\n''')
        f.write('''#SBATCH -p critical\n''')
        f.write('''#SBATCH -t 01:30:00\n''')
        f.write('''#SBATCH --cpus-per-task=4\n''')
        f.write('''#SBATCH -o ./{}.out\n'''.format(t))
        f.write('''#SBATCH -e ./{}.err\n'''.format(t))
        f.write('''set -e\n''')
        f.write('''source ~/.bashrc\n''')
        f.write('''conda activate torchbenchmark\n''')
        f.write('''cd ~/benchmark\n''')
        f.write('''proxychains4 -f ~/.proxychains_conf/node_to_login.conf python /public/home/qinfr/benchmark/test_running_profile.py  {} {} {} \n'''.format(model_name ,model_batch_size, int(s[index] *s2[index] / int(model_batch_size) / 10)))
    print("{},{}".format("NVIDIATITANRTX", t))
    index = index+1
    time.sleep(2)