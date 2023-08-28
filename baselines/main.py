#!/usr/bin/env python
import torch, toml, json
from utils.dataset import ChessVision
from models.classifiers import ResNet50, ResNet101, ViT, ViTLarge, VGG, SWIN
from train import train, infer
import numpy as np
from utils.metrics import Metrics
from utils.rule import Rules

config = toml.load("config.toml")
num2piece = {val:key for key, val in config['constants']['fen_pieces'].items()}

def repr(arr):
    return "\n".join(["".join([num2piece[j] for j in i]) for i in arr.reshape(8,8)])

def Train(model, size = 512):
    model.to(torch.device("cuda"))
    train_dataset = ChessVision(train=True, size = size)
    test_dataset = ChessVision(train=False, size = size)
    model = train(model, train_dataset, test_dataset)

def Analyze(model, size):
    name = model.name
    print("*"*10,name,"*"*10)
    path = f"./logs/models/{name}_chkpt.pth"
    model.to(torch.device("cuda"))
    model.load_state_dict(torch.load(path))
    test_dataset = ChessVision(train=False, size = size)
    outputs, labels = infer(model, test_dataset)
    np.save(f"./logs/output_{name}.npy", outputs)
    res = {}
    for k,board in enumerate(outputs):
        valid = Rules().check(board)
        if not valid:
            res[k] = Rules().analyze(board)
    with open(f"./logs/analysis_{name}.json","w") as f:
        json.dump(res, f, indent = 2)
    print(Metrics().eval_and_show(labels, outputs))

def main():
    assert torch.cuda.is_available()
    Train(ViT(), 224) 
    Analyze(ViT(), 224)
    Train(VGG(), 224)
    Analyze(VGG(), 224)
    Train(ResNet50, 512)
    Analyze(ResNet50(), 512)
    Train(ResNet101(), 512)
    Analyze(ResNet101(), 512)
    Train(ViTLarge(),384)
    Analyze(ViTLarge(), 384)
    Train(SWIN(),224)
    Analyze(SWIN(), 224)

if __name__ == "__main__":
    main()
