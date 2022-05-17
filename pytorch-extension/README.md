
# Dash Profiler

## without profiling
the pytorch script will run as usual
```bash
(base) murez@node1:~/CS225/project/pytorch-extension$ python test_model.py 
training finished
```
## with profiling flag
The profiling flag `DASH_PROFILER_ENABLED=1` can be set to 1 to enable the profiling funciton, the result will be sent to DASH Backend.
```
(base) murez@node1:~/CS225/project/pytorch-extension$ DASH_PROFILER_ENABLED=1 python test_model.py 
7849.50M MACs, 44.55M params, 4.71s
training finished
```

## with profiling and exit flag
The program will stop as soon as the profiling process is finished.

```
(base) murez@node1:~/CS225/project/pytorch-extension$ DASH_PROFILER_ENABLED=1 DASH_PROFILER_EXIT_ENABLED=1 python test_model.py 
7849.50M MACs, 44.55M params, 5.75s
```

## change profiling times
`DASH_PROFILER_TIMES` is used to set the profiling times of a batch to get the running time of the profiler, default is `10`.