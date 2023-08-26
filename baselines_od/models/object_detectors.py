#!/usr/bin/env python
import toml
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

config = toml.load("config.toml")

class FRCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "fasterrcnn"
        self.class_num = len(config['constants']['fen_pieces'])-1
        self.base = fasterrcnn_resnet50_fpn_v2(weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT,
                                               box_score_thresh=0.8)
        in_features = self.base.roi_heads.box_predictor.cls_score.in_features
        self.base.roi_heads.box_predictor = FastRCNNPredictor(in_features, self.class_num)
    def forward(self, images, targets=None):
        x = self.base(images, targets)
        return x
