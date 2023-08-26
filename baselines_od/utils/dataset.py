#!/usr/bin/env python
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import toml
import os
import json
from tqdm import tqdm

device = torch.device("cuda")
config = toml.load("config.toml")
files = config['files']

class ChessVision(Dataset):
    def __init__(self, train = True, size = 512):
        self.train = train
        self.size = size
        self.piece2num = config["constants"]["fen_pieces"]
        self.img_dir = files['train_images'] if train else files['test_images']
        self.labels = self._read_json(files['train_labels'] if train else files['test_labels'])
        self.bb = self._read_json(files['train_bb'] if train else files['test_bb'])
        self.grid = self._read_json(files['grid'])
        self.idxs = list(self.labels.keys())
        self._preprocess =  transforms.Compose([transforms.Normalize([0.539, 0.511, 0.509], [0.206, 0.177, 0.167]),
                                                transforms.Resize(size)])
    def _get_image(self, sidx):
        fname = os.path.join(self.img_dir, f"CV_{int(sidx):07d}.jpg")
        try:
            _image = torchvision.io.read_image(fname).float()
        except:
            raise ValueError(f"Couldn't open file {fname}")
        return self._preprocess(_image)
    def __len__(self):
        return len(self.idxs)
    def __getitem__(self, idx):
        if idx > len(self):
            raise StopIteration
        sidx = self.idxs[idx]
        od_labels = torch.tensor(np.array([self.piece2num[i[0]] for i in self.bb[sidx].keys()]), dtype = int)
        boxes =  torch.tensor(np.array([i for i in self.bb[sidx].values()]), dtype = int)
        label = torch.tensor(np.array(self.labels[sidx]).flatten())
        grid = torch.tensor(np.array(self.grid[sidx]), dtype = int)
        image = self._get_image(sidx)
        boxes = (boxes*(512/self.size)).int()
        targets = {'boxes':boxes, 'labels':od_labels}
        return image, targets, grid, label
    @staticmethod
    def _read_json(filename):
        with open(filename, "r") as f:
            return json.load(f)
    @staticmethod
    def collate_fn(data):
        image, targets, grid, label = zip(*data)
        image = torch.stack(image,dim=0)
        grid = torch.stack(grid, dim=0)
        label = torch.stack(label, dim=0)
        return image, list(targets), grid, label

def main():
    dataset = ChessVision(train = False)
    dataloader = DataLoader(dataset, collate_fn = dataset.collate_fn,batch_size = 3, shuffle = False)
    for _, targets, grid, label in dataloader:
        print(targets[0])
    
if __name__ == "__main__":
    main()
