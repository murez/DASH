# DASH
Deadline Aware AI Training Job Scheduler for Heterogenious cluster

## Scheduler

### Environment
The scheduler must be run at **SIST's AI Cluster**, with partition **critical**.

### How to use
1. `cd slurm-cli`
2. init the database by `python jobs.py` and see 数据库创建成功
3. `python slurm-cli.py -i <path of slurm script>`

## Monitor
Monitor should be always running

```bash
python monitor.py
```

## Evaluation
### slurm method
1. `cd slurm-cli`
2. `python eva_base.py`

### dash method
1. `cd slurm-cli`
2. `python eva_dash.py`

**Pay attention to the hard coded path in the above two files**

## FAQ
1. if I see `Lock!` when execute:
    - delete `slurm-cli/database.lock`
    - It will happen if exit in accident

## Other
Certainly, you may meet problems, including not have priviliage for AI cluster, cannot run pytorch bench mark, path missing. Should you trouble with these error, contact qinfr@@shanghaitech.edu.cn.