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
import numpy as np
import tasksubmit
import datetime

ratio = 1

def ifLock() -> bool:
    with open("database.lock","r") as f:
        if f.read() == "1":
            print("Lock!")
            return True
        else:
            return False

def Lock() -> None:
    """
    加锁
    """
    with open("database.lock","w") as f:
        f.write("1")

def UnLock() -> None:
    """
    解锁
    """
    with open("database.lock","w") as f:
        f.write("0")

def Scheduler():
    """
    This function is used to schedule jobs.
    Input: estimate time
    Output: which machine to run

    1. 找空闲的卡
    2. 对这个空闲的卡找对应的任务
    3. 运行
    朴素算法: 从显卡算力由弱到强，每一张显卡挑在自己上面跑的最快的任务
    """
    if ifLock() == True:
        return
    card = traffic.GetFreeCard() #找到卡名
    if card == None: # 出错或者没有空闲卡
        return 
    job = jobs.GetJobByCard(card) #找到对应的任务的执行文件
    # (ID, PATH, min({}))
    if job==-1:
        return # 出错或者无任务
    # tasksubmit.TaskSubmit(job) #运行任务 TODO:
    slurm_id = tasksubmit.change_node(job[1],job[0],card)
    jobs.RunJobOnCard(job[0], card, slurm_id)


def SchedulerP():
    """
    Provide SLO
    """
    if ifLock() == True:
        return
    card = traffic.GetFreeCardFromPCluster()

    if card == None: # 出错或者没有空闲卡
        return 
    job = jobs.GetClosetJob() # 临近 DDL 的任务 # (ID, PATH, min(DEADLINE))
    if job == -1:
        return # 出错或者无任务
    # TODO: 运行任务
    print(job)
    slurm_id = tasksubmit.change_node(job[1],job[0],card)
    jobs.RunJobOnPCluster(job[0], card, slurm_id)

def EstimateTime(jobID: int, path: str,NVIDIAGeForceGTX1080: int , NVIDIATITANV: int, NVIDIAGeForceRTX2080Ti: int,NVIDIATITANXp:int) -> str:
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
    Lock()
    # 先放入数据库
    if jobs.PutJobs(jobID,path,NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp, np.mean([NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp])) == False:
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
    _time = base_time + time_in_queue # Unix time
    _time = _time * ratio
    jobs.UpdateJobDDLByID(jobID, _time)
    readable_time = datetime.datetime.utcfromtimestamp(_time + 8*60*60).strftime('%Y-%m-%dT%H:%M:%SZ') # readable time

    UnLock()

    return readable_time

def EstimateTimeWithoutInsert(jobID: int, path: str,NVIDIAGeForceGTX1080: int , NVIDIATITANV: int, NVIDIAGeForceRTX2080Ti: int,NVIDIATITANXp:int) -> str:
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
    if ifLock() == True:
        return
    Lock()
    # 先放入数据库
    if jobs.PutJobs(jobID,path,NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp, np.mean([NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp])) == False:
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
    _time = base_time + time_in_queue # Unix time
    _time = _time * ratio
    jobs.UpdateJobDDLByID(jobID, _time)
    readable_time = datetime.datetime.utcfromtimestamp(_time + 8*60*60).strftime('%Y-%m-%dT%H:%M:%SZ') # readable time

    UnLock()

    return readable_time

if __name__ ==" __main__":
    pass