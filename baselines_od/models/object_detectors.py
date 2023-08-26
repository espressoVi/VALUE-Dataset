#!/usr/bin/env python
import toml
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights

config = toml.load("config.toml")

class FRCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "fasterrcnn"
        self.base = fasterrcnn_resnet50_fpn_v2(weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT, box_score_thresh=0.9)
