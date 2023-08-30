#!/usr/bin/env python
import torch, toml, json
from utils.dataset import ChessVision
from models.classifiers import ResNet50, ResNet101, ViT, ViTLarge, VGG, SWIN
from train import train, infer
import numpy as np

config = toml.load("config.toml")

def repr(arr):
    return "\n".join(["".join([num2piece[j] for j in i]) for i in arr.reshape(8,8)])

def Train(model, size = 512):
    model.to(torch.device("cuda"))
    train_dataset = ChessVision(train=True, size = size)
    test_dataset = ChessVision(train=False, size = size)
    model = train(model, train_dataset, test_dataset)

def main():
    assert torch.cuda.is_available()
    Train(ViT(), 224) 
    Train(VGG(), 224)
    Train(ResNet50, 512)
    Train(ResNet101(), 512)
    Train(ViTLarge(),384)
    Train(SWIN(),224)

if __name__ == "__main__":
    main()
