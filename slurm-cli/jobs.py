#-------------------------------
# This module is to store jobs
#-------------------------------


import sqlite3
import time

DATABASE_NAME = 'dash.db'

E_CLUSTERS = 0
P_CLUSTERS = 1

def InitDatabase():
    conn = sqlite3.connect(DATABASE_NAME)
    print ("数据库打开成功")

    c = conn.cursor()
    c.execute('''CREATE TABLE JOBS
        (ID INT PRIMARY KEY     NOT NULL,
        PATH           STRING NOT NULL,
        NVIDIAGeForceGTX1080     INT     NOT NULL,
        NVIDIATITANV  INT     NOT NULL,
        NVIDIAGeForceRTX2080Ti INT NOT NULL,
        NVIDIATITANXp INT NOT NULL,
        MediumTime INT NOT NULL,
        DEADLINE INT);''')
    c.execute('''CREATE TABLE E_CLUSTERS (ID INT PRIMARY KEY NOT NULL, CARDNAME STRING NOT NULL ,InUSE INT NOT NULL, LIMIT_ INT NOT NULL);''')
    c.execute('''CREATE TABLE P_CLUSTERS (ID INT PRIMARY KEY NOT NULL, CARDNAME STRING NOT NULL ,InUSE INT NOT NULL, LIMIT_ INT NOT NULL);''')
    c.execute('''CREATE TABLE RUNNING_JOBS (ID INT PRIMARY KEY NOT NULL, CARDNAME STRING NOT NULL, FINISH_TIME INT NOT NULL, SLURM_ID INT NOT NULL, TYPE INT NOT NULL);''')
    print ("数据表创建成功")
    c.execute("INSERT INTO E_CLUSTERS (ID, CARDNAME, InUSE,LIMIT_) VALUES (?,?,?,?)", (1, "NVIDIAGeForceGTX1080", 0, 2))
    c.execute("INSERT INTO E_CLUSTERS (ID, CARDNAME, InUSE,LIMIT_) VALUES (?,?,?,?)", (2, "NVIDIATITANV", 0, 1))
    c.execute("INSERT INTO E_CLUSTERS (ID, CARDNAME, InUSE,LIMIT_) VALUES (?,?,?,?)", (3, "NVIDIAGeForceRTX2080Ti", 0, 1))
    c.execute("INSERT INTO E_CLUSTERS (ID, CARDNAME, InUSE,LIMIT_) VALUES (?,?,?,?)", (4, "NVIDIATITANXp", 0, 1))
    c.execute("INSERT INTO P_CLUSTERS (ID, CARDNAME, InUSE,LIMIT_) VALUES (?,?,?,?)", (1, "NVIDIAGeForceRTX2080Ti", 0, 1))
    print ("数据表初始化数据完成")
    conn.commit()
    conn.close()

def PutJobs(id:int, path: str, NVIDIAGeForceGTX1080: int, NVIDIATITANV: int, NVIDIAGeForceRTX2080Ti: int,NVIDIATITANXp:int, MediumTime: int) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO JOBS (ID, PATH, NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp,MediumTime ) VALUES (?,?,?,?,?,?,?)", (id, path, NVIDIAGeForceGTX1080,NVIDIATITANV,NVIDIAGeForceRTX2080Ti,NVIDIATITANXp, MediumTime))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def GetJobAndTimeByIDCard(jobID: int, cardname: str) : # (ID, ESTIMATED_TIME)
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, {} FROM JOBS WHERE ID = {}".format(cardname, jobID))
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)
        return (-1,-1)
    return result[0] # (ID, ESTIMATED_TIME)

def UpdateJobDDLByID(jobID: int, deadline: int) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("UPDATE JOBS SET DEADLINE={} WHERE ID={}".format(deadline, jobID))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def GetJobByCard(cardname: str) :
    _job_id = -1
    _min = 9999999
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, PATH, min({}) FROM JOBS".format(cardname))
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)
        return -1
    if result == [(None, None, None)]:
        return -1
    return result[0] # (ID, PATH)

def DeleteJobByID(jobID: int) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM JOBS WHERE ID={}".format(jobID))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def GetInUseAndLimitByCardname(cardname: str):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT InUSE,LIMIT_ FROM E_CLUSTERS WHERE CARDNAME='{}'".format(cardname))
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("DEBUG: CARD {} is running {} jobs with max limit {}.".format(cardname, result[0][0], result[0][1]))
    except Exception as e:
        print(e)
        return (-1,-1)
    return result[0]

def GetInUseAndLimitByCardnamePCluster(cardname: str):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT InUSE,LIMIT_ FROM P_CLUSTERS WHERE CARDNAME='{}'".format(cardname))
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("DEBUG: CARD {} is running {} jobs with max limit {}.".format(cardname, result[0][0], result[0][1]))
    except Exception as e:
        print(e)
        return (-1,-1)
    return result[0]


def RunJobOnCard(jobID: int, cardname: str, slurmId: int) -> bool:
    print("RunJobOnCard: JobID {} is running on {} with slurmId {}.".format(jobID, cardname, slurmId))
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        card = GetInUseAndLimitByCardname(cardname)
        if card[0] == -1:
            return False
        if card[0] >= card[1]:
            print("FATAL ERROR: Run jobs on card exceed max limit.")
        c.execute("UPDATE E_CLUSTERS SET InUSE={} WHERE CARDNAME='{}'".format(card[0]+1,cardname))
        job = GetJobAndTimeByIDCard(jobID, cardname) # (ID, ESTIMATED_TIME)
        c.execute("DELETE FROM JOBS WHERE ID={}".format(jobID))
        print("DELETE JOB{}".format(jobID))
        c.execute("INSERT INTO RUNNING_JOBS (ID, CARDNAME, FINISH_TIME, SLURM_ID, TYPE) VALUES (?,?,?,?,?)", (job[0], cardname, int(time.time())+job[1] ,slurmId, E_CLUSTERS))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def RunJobOnPCluster(jobID: int, cardname: str,slurmId: int) -> bool:
    print("RunJobOnPCluster: JobID {} is running on {} with slurmId {}.".format(jobID, cardname, slurmId))
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        card = GetInUseAndLimitByCardnamePCluster(cardname)
        if card[0] == -1:
            return False
        if card[0] >= card[1]:
            print("FATAL ERROR: Run jobs on card exceed max limit.")
        c.execute("UPDATE P_CLUSTERS SET InUSE={} WHERE CARDNAME='{}'".format(card[0]+1,cardname))
        job = GetJobAndTimeByIDCard(jobID, cardname) # (ID, ESTIMATED_TIME)
        c.execute("DELETE FROM JOBS WHERE ID={}".format(jobID))
        print("DELETE JOB{}".format(jobID))
        c.execute("INSERT INTO RUNNING_JOBS (ID, CARDNAME, FINISH_TIME, SLURM_ID, TYPE) VALUES (?,?,?,?,?)", (job[0], cardname, int(time.time())+job[1] ,slurmId, P_CLUSTERS))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True




def FailRunJobOnCard(jobID: int, cardID: int) -> bool:
    print("Oops, FailRunJobOnCard")

def testJobs1():
    PutJobs(1, "./test.py", 1, 1, 1, 1, 25)
    PutJobs(2, "./test.py", 1, 1, 1, 1,50)
    PutJobs(3, "./test.py", 1, 1, 1, 1, 70)
    PutJobs(4, "./test.py", 1, 1, 1, 1, 333)
    PutJobs(5, "./test.py", 1, 1, 1, 1, 40)
    PutJobs(6, "./test.py", 1, 1, 1, 1, 999)

def GetMediumTimeSumBeforeID(jobID: int) -> int: # Return times in the queue in seconds
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT SUM(MediumTime) FROM JOBS WHERE MediumTime<={}".format(GetJobAndTimeByIDCard(jobID,"MediumTime")[1]))
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)
        return -1
    if result[0][0] == None:
        return 0
    return result[0][0]

def GetMaxFinishTimeinRunningQueue() -> int: # Return max finish time in unix seconds
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT MAX(FINISH_TIME) FROM RUNNING_JOBS")
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)
        return -1
    if result[0][0] == None:
        return int(time.time())
    return result[0][0]



def GetAllCards()-> list:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, CARDNAME, InUSE, LIMIT_ FROM E_CLUSTERS")
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)   
        return [-1]
    return result

def GetAllCardsFromPCluster() -> list:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM P_CLUSTERS")
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)   
        return [-1]
    return result

def GetAllRunningJobs()->list:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, CARDNAME, FINISH_TIME, SLURM_ID, TYPE FROM RUNNING_JOBS")
        result = c.fetchall()
        conn.commit()
        conn.close()
        print("FIND:", result)
    except Exception as e:
        print(e)
        return []
    return result

def FinishedJob(jobID: int) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, CARDNAME, FINISH_TIME, SLURM_ID, TYPE FROM RUNNING_JOBS WHERE ID={}".format(jobID))
        job = c.fetchall()[0] # (ID, CARDNAME, FINISH_TIME, SLURM_ID)
        c.execute("DELETE FROM RUNNING_JOBS WHERE ID={}".format(jobID))
        card = GetInUseAndLimitByCardname(job[1])  # InUSE,LIMIT_ FROM E_CLUSTERS
        c.execute("UPDATE E_CLUSTERS SET InUSE={} WHERE CARDNAME='{}'".format(card[0]-1,job[1]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def FinishedJobPCluster(jobID: int) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, CARDNAME, FINISH_TIME, SLURM_ID FROM RUNNING_JOBS WHERE ID={}".format(jobID))
        job = c.fetchall()[0] # (ID, CARDNAME, FINISH_TIME, SLURM_ID)
        c.execute("DELETE FROM RUNNING_JOBS WHERE ID={}".format(jobID))
        card = GetInUseAndLimitByCardnamePCluster(job[1])  # InUSE,LIMIT_ FROM E_CLUSTERS
        c.execute("UPDATE P_CLUSTERS SET InUSE={} WHERE CARDNAME='{}'".format(card[0]-1,job[1]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True

def GetClosetJob() -> list:
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT ID, PATH, min(DEADLINE) FROM JOBS")
        result = c.fetchall()[0]
        print("Find", result)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return -1
    if result == (None, None, None):
        return -1
    return result


if __name__ =="__main__":
    InitDatabase()
    # testJobs1()
    # print(GetAllCards())
    # pass