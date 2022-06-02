

def rewrite(path: str):
    flag = True
    with open(path, 'wr+') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#SBATCH'):
                continue
            else:
                flag = False
            if flag==False:
                