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
        with torch.no_grad():
            macs, prams = ptflops.get_model_complexity_info(self.train_model, self.input_shape, as_strings=False, print_per_layer_stat=False)
            start_time = time.perf_counter()
            with torch.cuda.device(0):
                for i in range(10):
                    self.train_model.forward(torch.rand(self.input_shape).unsqueeze(0))
            end_time = time.perf_counter()
            print(f"{macs/1e6:.2f}M MACs, {prams/1e6:.2f}M params, {(end_time-start_time):.2f}s")
        return self.train_model

    def __exit__(self,exc_type,exc_val,exc_tb):
        pass

