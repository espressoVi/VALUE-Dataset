#!/usr/bin/env python
import os
import toml
import torch
from tqdm import tqdm
from torch.optim import AdamW
from torch.optim.lr_scheduler import ExponentialLR
from torch.utils.data import DataLoader
import numpy as np
from utils.metrics import Metrics

config = toml.load('config.toml')
device = torch.device("cuda")
        
def train(model, train_dataset, test_dataset ):
    name = model.name
    optimizer_parameters = model.parameters()
    optimizer = AdamW(optimizer_parameters,lr=config['models']['lr'], eps=1e-8, weight_decay = 1e-4)
    scheduler = ExponentialLR(optimizer, gamma = 0.1, verbose=True)
    train_dataloader = DataLoader(train_dataset, collate_fn = train_dataset.collate_fn, shuffle = True, batch_size = config['models']['batch'], )
    best_score = 0
    epochs = config['models']['epochs']
    loss_track = []
    for ep in range(1,epochs+1):
        train_loss, counter = 0.0, 1
        model.zero_grad()
        epoch_iterator = tqdm(train_dataloader, desc="Iteration", disable=False)
        for i, batch in enumerate(epoch_iterator):
            model.train()
            image = batch[0].to(device)
            targets = [{'boxes':i['boxes'].to(device), 'labels':i['labels'].to(device)} for i in batch[1]]
            losses = model(image, targets)
            losses = sum(loss for loss in losses.values())
            losses.backward()
            train_loss += losses.item()
            counter += 1
            if counter%20 == 0:
                loss_track.append(train_loss/counter)
            optimizer.step()
            optimizer.zero_grad()
            epoch_iterator.set_description(f"Epoch:{ep} | Loss {train_loss/counter:5f}")
            epoch_iterator.refresh()
        test_metrics = evaluate(model, test_dataset)
        print('Test :', test_metrics)
        scheduler.step()
    np.save(f"./logs/{name}_losses.npy", np.array(loss_track))
    torch.save(model.state_dict(), f"./logs/{name}_chkpt.pth")
    return model

def evaluate(model, dataset):
    model.eval()
    dataloader = DataLoader(dataset, collate_fn = dataset.collate_fn, batch_size = config['models']['batch'], )
    labels, outputs = [],[]
    for batch in tqdm(dataloader, desc = "Evaluating"):
        with torch.no_grad():
            out = model(batch[0].to(device))
        labels.extend(batch[3].detach().numpy())
        boxes, predictions = [],[]
        for i in out:
            boxes.append(i['boxes'].detach().cpu().numpy())
            predictions.append(i['labels'].detach().cpu().numpy())
        preds = infer(boxes, predictions, batch[2].detach().numpy())
        outputs.extend(preds)
    labels = np.array(labels, dtype = int)
    outputs = np.array(outputs, dtype = int)
    return Metrics().eval_and_show(labels, outputs)

def infer(all_boxes, all_predictions, all_grid):
    res = []
    for boxes, predictions, grid in zip(all_boxes, all_predictions, all_grid):
        grid = np.array(grid)
        board = np.zeros(64,dtype = int)
        for box, prediction in zip(boxes, predictions):
            box = np.array([(box[0]+box[2])/2, box[1]])
            ids = np.argmin(np.square(grid - box).sum(axis=1))
            board[ids] = prediction+1
        res.append(board)
    return np.array(res, dtype = int)
