#!/usr/bin/env python
import os
import toml
import torch
from tqdm import tqdm
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
import numpy as np
from utils.metrics import Metrics

config = toml.load('config.toml')
device = torch.device("cuda")
        
def train(model, train_dataset, test_dataset ):
    name = model.name
    optimizer_parameters = model.parameters()
    optimizer = AdamW(optimizer_parameters,lr=config['models']['lr'], eps=1e-8, weight_decay = 1e-4)
    scheduler = ReduceLROnPlateau(optimizer, mode = 'max', factor = 0.1, patience = 1)
    train_dataloader = DataLoader(train_dataset, shuffle = True, batch_size = config['models']['batch'], )
    best_score = 0
    epochs = config['models']['epochs']
    loss_track = []
    for ep in range(1,epochs+1):
        train_loss, counter = 0.0, 1
        model.zero_grad()
        epoch_iterator = tqdm(train_dataloader, desc="Iteration", disable=False)
        outputs, labels = [],[]
        for i, (im,lab) in enumerate(epoch_iterator):
            model.train()
            loss, logits = model(im.to(device), lab.to(device))
            loss.backward()
            train_loss += loss.item()
            counter += 1
            if counter%20 == 0:
                loss_track.append(train_loss/counter)
            optimizer.step()
            optimizer.zero_grad()
            epoch_iterator.set_description(f"Epoch:{ep} | Loss {train_loss/counter:5f}")
            epoch_iterator.refresh()
            outputs.extend(logits.detach().cpu().numpy())
            labels.extend(lab.detach().cpu().numpy())
        outputs, labels = np.array(outputs), np.array(labels)
        f1 = Metrics().metrics['F1'](labels, outputs)
        train_metrics = Metrics().eval_and_show(labels, outputs)
        test_metrics = evaluate(model, test_dataset)
        print('Train : ', train_metrics)
        print('Test :', test_metrics)
        scheduler.step(f1)
    np.save(f"./logs/{name}_losses.npy", np.array(loss_track))
    torch.save(model.state_dict(), f"./logs/{name}_chkpt.pth")
    return model

def evaluate(model, dataset):
    model.eval()
    outputs, labels = [],[]
    dataloader = DataLoader(dataset, shuffle = False, batch_size = config['models']['batch'], )
    for im, lab in tqdm(dataloader, desc = "Evaluating"):
        with torch.no_grad():
            out = model(im.to(device), lab.to(device))
        outputs.extend(out.detach().cpu().numpy())
        labels.extend(lab.detach().cpu().numpy())
    outputs, labels = np.array(outputs), np.array(labels)
    return Metrics().eval_and_show(labels, outputs)
