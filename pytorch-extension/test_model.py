import torch
import torchvision
from profiler import DashProfiler

testmodel = torchvision.models.resnet101()

with DashProfiler(testmodel, (10, 3, 224, 224)) as testmodel:
    with torch.cuda.device(0):
        testmodel.train()
        testmodel.forward(torch.rand((10, 3, 224, 224)))
        print("training finished")
