import ptflops
import torch
import os
import time
import requests
from typing import Tuple


class DashProfiler():
    def __init__(self, train_model: torch.nn.Module, input_shape: Tuple):
        self.train_model = train_model
        self.input_shape = input_shape
    def __enter__(self):
        try:
            if os.getenv('DASH_PROFILER_ENABLED') != '1':
                return self.train_model
            if os.getenv("DASH_PROFILER_TIMES") is not None:
                self.times = int(os.getenv("DASH_PROFILER_TIMES"))
            else:
                self.times = 10
            with torch.no_grad():
                macs, prams = ptflops.get_model_complexity_info(self.train_model, self.input_shape[1:], as_strings=False, print_per_layer_stat=False)
                start_time = time.perf_counter()
                with torch.cuda.device(0):
                    for i in range(self.times):
                        self.train_model.to('cuda')
                        self.train_model.forward(torch.rand(self.input_shape).cuda())
                end_time = time.perf_counter()
                print(f"{macs/1e6:.2f}M MACs, {prams/1e6:.2f}M params, {(end_time-start_time)/self.times:.2f}s")
            if os.getenv('DASH_PROFILER_EXIT_ENABLED') == '1':
                exit()
            else:
                return self.train_model
        except Exception as e:
            print(e)
            return self.train_model
    def __exit__(self,exc_type,exc_val,exc_tb):
        pass

