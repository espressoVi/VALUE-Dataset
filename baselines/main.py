#!/usr/bin/env python
import torch
from utils.dataset import ChessVision
from models.model import ResNet50, ResNet101, ViT
from train import train, evaluate
import numpy as np
from utils.metrics import Metrics

def main():
    train_dataset = ChessVision(train=True)
    test_dataset = ChessVision(train=False)
    model = ViT()
    model.to(torch.device("cuda"))
    model = train(model, train_dataset, test_dataset)

if __name__ == "__main__":
    assert torch.cuda.is_available()
    main()
