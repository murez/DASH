import os
import torch
import numpy as np
from torch.utils.data.dataset import Dataset
from config import *

class ShanghaitechClusterDataset(Dataset):
    def __init__(self, data_npy_path: str = '/home/murez/CS225/project/throughput_estimator/Shanghaitech_SIST_datacenter/transfer_data.npy') -> None:
        super().__init__()
        self.data = np.load(data_npy_path, allow_pickle=True)
        self.model_name_to_num = model_name_to_num
        self.model_num_to_name = model_num_to_name
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index):
        '''
        from gpu config, to gpu config.
        from batch size
        '''
        from_device = self.data[index]['from']
        to_device = self.data[index]['to']

        from_device_config = GPU_config_list[from_device]
        to_device_config = GPU_config_list[to_device]

        from_batch_size = self.data[index]['from_batch_size']
        to_batch_size = self.data[index]['to_batch_size']
        from_duration = self.data[index]['from_duration']
        to_duration = self.data[index]['to_duration']

        duration_rate = to_duration / from_duration

        from_metrics = self.data[index]['from_metrics']
        from_length = self.data[index]['from_length']
        
        return (from_device_config, 
                to_device_config, 
                from_batch_size, 
                to_batch_size, 
                from_metrics, 
                from_length,
                duration_rate)
                
