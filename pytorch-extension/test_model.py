import torch
import torchvision
from decorator import DashProfiler

testmodel = torchvision.models.resnet101()

with DashProfiler(testmodel, (3, 224, 224)) as testmodel:
    for i in range(10):
        testmodel.forward(torch.rand((1, 3, 224, 224)))
