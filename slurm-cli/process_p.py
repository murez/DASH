
with open("/public/home/qinfr/DASH/slurm-cli/out", "r") as f:
    for line in f.readlines():
        if line.startswith("RunJobOnPCluster:"):
            l = line.strip().split(" ")
            s = ""
            e = ""
            with open("/public/home/qinfr/DASH/slurm-cli/{}.out".format(l[9].strip('.')), "r") as ll:
                for line1 in ll.readlines():
                    if line1.startswith("Start Time:"):
                        s = line1.strip("Start Time:").strip()
                    if line1.startswith("End Time:"):  
                        e = line1.strip("End Time:").strip()
            est = ""
            with open("/public/home/qinfr/DASH/slurm-cli/dash_out") as ll:
                t = 0
                for line1 in ll.readlines():
                    if l[2] in line1:
                        t = t+1
                    if t==4:
                        est=line1.strip("EstimateTime: ").strip()
                        break
                    if t>0:
                        t=t+1
                    
            print("{},{},{},P,{},{},{}".format(l[9].strip('.'),l[6],l[2], s, e,est))