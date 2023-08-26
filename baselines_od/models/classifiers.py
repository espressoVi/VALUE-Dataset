#!/usr/bin/env python
import toml
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.resnet import resnet50, ResNet50_Weights
from torchvision.models.resnet import resnet101, ResNet101_Weights
from transformers import ViTModel

config = toml.load("config.toml")

class ResNet50(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "resnet50"
        self.class_num = len(config['constants']['fen_pieces'])
        board_dim = config['constants']['CHESS_BOARD_LEN']
        self.fex = resnet50(weights = ResNet50_Weights.IMAGENET1K_V1)
        in_features = self.fex.fc.weight.shape[1]
        out_features = board_dim*board_dim*self.class_num
        self.fex.fc = nn.Identity()
        self.dropout = nn.Dropout(p=0.1)
        self.fc = nn.Linear(in_features,out_features)
        self.loss = nn.CrossEntropyLoss()
    def forward(self, images, labels = None):
        x = self.fex(images)
        x = self.dropout(x)
        x = self.fc(x).view(x.shape[0],self.class_num, -1)
        predicts = torch.argmax(torch.softmax(x, dim = 1), dim = 1)
        if not self.training:
            return predicts
        loss = self.loss(x, labels)
        return loss, predicts

class ResNet101(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "resnet101"
        self.class_num = len(config['constants']['fen_pieces'])
        board_dim = config['constants']['CHESS_BOARD_LEN']
        self.fex = resnet101(weights = ResNet101_Weights.IMAGENET1K_V1)
        in_features = self.fex.fc.weight.shape[1]
        out_features = board_dim*board_dim*self.class_num
        self.fex.fc = nn.Identity()
        self.dropout = nn.Dropout(p=0.1)
        self.fc = nn.Linear(in_features,out_features)
        self.loss = nn.CrossEntropyLoss()
    def forward(self, images, labels = None):
        x = self.fex(images)
        x = self.dropout(x)
        x = self.fc(x).view(x.shape[0],self.class_num, -1)
        predicts = torch.argmax(torch.softmax(x, dim = 1), dim = 1)
        if not self.training:
            return predicts
        loss = self.loss(x, labels)
        return loss, predicts

class ViT(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "vit_small"
        self.class_num = len(config['constants']['fen_pieces'])
        board_dim = config['constants']['CHESS_BOARD_LEN']
        self.fex = ViTModel.from_pretrained("google/vit-base-patch16-224")
        in_features = self.fex.config.hidden_size
        out_features = board_dim*board_dim*self.class_num
        self.dropout = nn.Dropout(p=0.1)
        self.fc = nn.Linear(in_features,out_features)
        self.loss = nn.CrossEntropyLoss()
    def forward(self, images, labels = None):
        x = self.fex(images)['pooler_output']
        x = self.dropout(x)
        x = self.fc(x).view(x.shape[0],self.class_num, -1)
        predicts = torch.argmax(torch.softmax(x, dim = 1), dim = 1)
        if not self.training:
            return predicts
        loss = self.loss(x, labels)
        return loss, predicts

class ViTLarge(nn.Module):
    def __init__(self):
        super().__init__()
        self.name = "vit_large"
        self.class_num = len(config['constants']['fen_pieces'])
        board_dim = config['constants']['CHESS_BOARD_LEN']
        self.fex = ViTModel.from_pretrained("google/vit-large-patch32-384")
        in_features = self.fex.config.hidden_size
        out_features = board_dim*board_dim*self.class_num
        self.dropout = nn.Dropout(p=0.1)
        self.fc = nn.Linear(in_features,out_features)
        self.loss = nn.CrossEntropyLoss()
    def forward(self, images, labels = None):
        x = self.fex(images)['pooler_output']
        x = self.dropout(x)
        x = self.fc(x).view(x.shape[0],self.class_num, -1)
        predicts = torch.argmax(torch.softmax(x, dim = 1), dim = 1)
        if not self.training:
            return predicts
        loss = self.loss(x, labels)
        return loss, predicts
