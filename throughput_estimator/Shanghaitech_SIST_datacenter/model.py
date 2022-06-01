from turtle import forward
import torch

class DashEstimator(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = torch.nn.GRU(input_size=6, hidden_size=20, dropout=0.5, batch_first=True)
        self.MLP = torch.nn.Sequential(
            torch.nn.Linear(36, 36),
            torch.nn.ReLU(),
            torch.nn.Linear(36, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 1))
    def forward(self, feature, metrics, length):
        packed_metrics = torch.nn.utils.rnn.pack_padded_sequence(metrics.float(), length, batch_first=True, enforce_sorted=False)
        packed_output, task_feature = self.gru(packed_metrics)
        features = torch.cat((task_feature.squeeze(0), feature.float()), dim=1)
        return self.MLP(features)

