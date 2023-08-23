# Baselines on chessvision dataset.

This repository contains code to predict chess board positions from corresponding images.

## Authors
- [Soumadeep Saha](https://www.github.com/espressovi), Indian Statistical Institute, Kolkata, India

## Done:

## To-Do:
  - Seperate train, test.
  - Write data-loader, related utils - torchvision.
  - Download models, and finetune.

## Files:

  - main.py
  - README.md           -> This file
  - utils
    - dataset.py        -> Code to load and process dataset.
    - rule.py           -> Rule checking implementation.
    - metrics.py        -> Implements several multi-target metrics.
  - model
    - model.py           -> Code for model.
    - parts.py           -> Contains different pieces for several models.
