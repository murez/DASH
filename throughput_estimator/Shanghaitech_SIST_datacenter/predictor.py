import torch
import numpy as np
import ShanghaitechData
import model
from config import *
import tqdm

class DashPredictor():
    def __init__(self, path=None) -> None:
        self.model = model.DashEstimator()
        if path is not None:
            self.model.load_state_dict(torch.load(path))

    def evaluate(self,
                 from_device: str,
                 to_device: list,
                 from_batch_size: int,
                 to_batch_size: list,
                 metrics: np.array) -> np.ndarray:

        transfer_feature = []
        for i, to in enumerate(to_device):
            from_device_config = GPU_config_list[from_device]
            to_device_config = GPU_config_list[to]
            feature = np.concatenate(
                [from_device_config, to_device_config, from_batch_size, to_batch_size[i]], axis=None)
            transfer_feature.append(feature)
        transfer_feature = torch.from_numpy(np.array(transfer_feature)).float()

        batch_metrics = torch.cat([torch.from_numpy(metrics).unsqueeze(0).float()
                                   for x in range(len(to_batch_size))], dim=0)
        self.model = self.model.to('cuda')
        self.model.eval()
        with torch.no_grad():
            duration_rate = self.model(transfer_feature.to(
                'cuda'), batch_metrics.to('cuda'))
        return duration_rate.cpu().numpy()
    
    test_loss_min = np.inf

    def train(self, batchsize=64):
        cluster_dataset = ShanghaitechData.ShanghaitechClusterDataset()
        test_len = int(len(cluster_dataset) * 0.1)
        train_len = len(cluster_dataset) - test_len
        train_dataset, test_dataset = torch.utils.data.random_split(cluster_dataset, [train_len, test_len])
        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batchsize, shuffle=True)
        test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batchsize, shuffle=True)
        self.model = self.model.to('cuda')
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        loss_func = torch.nn.MSELoss()
        for epoch in range(100):
            print('epoch:', epoch)
            for step, (device_feature, metrics, length, duration_rate) in enumerate(tqdm.tqdm(train_loader)):
                device_feature = device_feature.to('cuda')
                packed_metrics = torch.nn.utils.rnn.pack_padded_sequence(
                metrics.float(), length, batch_first=True, enforce_sorted=False)
                packed_metrics = packed_metrics.to('cuda')
                
                duration_rate = duration_rate.float().to('cuda')
                optimizer.zero_grad()
                output = self.model(device_feature, packed_metrics)
                loss = loss_func(output, duration_rate).float()
                loss.backward()
                optimizer.step()
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.item())

            test_loss = 0
            test_acc = 0
            for step, (device_feature, metrics, length, duration_rate) in enumerate(test_loader):
                device_feature = device_feature.to('cuda')
                packed_metrics = torch.nn.utils.rnn.pack_padded_sequence(
                    metrics.float(), length, batch_first=True, enforce_sorted=False)
                packed_metrics = packed_metrics.to('cuda')
                duration_rate = duration_rate.float().to('cuda')
                output = self.model(device_feature, packed_metrics)
                test_loss += loss_func(output, duration_rate).item()
                test_acc += (output.detach().cpu().numpy() - duration_rate.detach().cpu().numpy()).mean()
            test_loss /= len(test_loader)
            test_acc /= len(test_loader)
            print('Test set: Average loss: {:.4f}, Accuracy: {:.2f}%'.format(test_loss, 100 - test_acc * 100))
            if test_loss < self.test_loss_min:
                self.test_loss_min = test_loss
                torch.save(self.model.state_dict(), 'model_best.pth')
                print('model saved')
            torch.save(self.model.state_dict(), 'model_{}.pth'.format(epoch))
        # torch.save(self.model.state_dict(), './model/dash_model.pth')

        # test
        
        

