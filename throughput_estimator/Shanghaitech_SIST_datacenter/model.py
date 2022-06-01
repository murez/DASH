import torch

class DashEstimator(torch.nn.modules):
    def __init__(self):
        super().__init__()
        self.gru = torch.nn.GRU(input_size=6, hidden_size=20, dropout=0.5, batch_first=True)
        self.