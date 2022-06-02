#--------------------------------------------------
# There are several jobs waiting to be scheduled
#--------------------------------------------------


# importing the sys module
import sys   
# appending the directory of mod.py
# in the sys.path list
sys.path.append('/public/home/qinfr/DASH/throughput_estimator/Shanghaitech_SIST_datacenter')   
import config
import jobs
import traffic
import tasksubmit
import numpy as np
from datetime import datetime

ratio = 1 # DEADLINE ratio


def scheduler():
    """
    This function is used to schedule jobs.
    Input: estimate time
    Output: which machine to run

    1. 找空闲的卡
    2. 对这个空闲的卡找对应的任务
    3. 运行
    朴素算法: 从显卡算力由弱到强，每一张显卡挑在自己上面跑的最快的任务
    """
    card = traffic.GetFreeCard() #找到卡名
    job = jobs.GetJobByCard(card) #找到对应的任务的执行文件
    tasksubmit.TaskSubmit(job) #运行任务

def estimate_time(jobID: int, path: str,NVIDIAGeForceGTX1080: int , NVIDIATITANV: int, NVIDIAGeForceRTX2080Ti: int,NVIDIATITANXp:int) -> str:
    """
    这个函数是运行完测试之后，放入数据库中的操作
    This function is used to estimate the time of jobs.
    Input: estimate time
    Output: which machine to run
    1. 放入数据库并排序
    2. 将正在运行的任务时间加起来
    3. 把排名在前的任务的时间加起来
    4. 乘以系数再转换成 GMT 时间

    TODO: 加锁防止 monitor 自动运行
    """
    #上锁
    with open("scheduler.lock","w") as f:
        f.write("1")
    # 先放入数据库
    if jobs.InsertJob(jobID,path,NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp, np.mean([NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp])) == False:
        print("InsertJob failed")
        return -1
    # 再获得基础时间
    base_time = jobs.GetMaxFinishTimeinRunningQueue()
    if (base_time == -1):
        print("GetMaxFinishTimeinRunningQueue failed")
        return -1
    # 在获得队列中前面的时间
    time_in_queue = jobs.GetMediumTimeSumBeforeID(jobID)
    if (time_in_queue == -1):
        print("GetMediumTimeSumBeforeID failed")
        return -1

    # 转换成 GMT 时间 并更新
    time = base_time + time_in_queue # Unix time
    time = time * a
    jobs.UpdateJobDDLByID(jobID, time)
    readable_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') # readable time

    #释放锁
    with open("scheduler.lock","w") as f:
        f.write("0")
    return readable_time
    

if __name__ ==" __main__":
    pass