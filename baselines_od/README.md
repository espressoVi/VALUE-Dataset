# Baselines on chessvision dataset.

This folder contains code to predict chess board positions from corresponding images.

## Done:
  - Seperate train, test.
  - Write data-loader, related utils - torchvision.
  - Download models, and finetune.
## To-Do:
  - Figure out object detection.

## Files:

  - main.py
  - train.py            -> Training routine.
  - README.md           -> This file.
  - utils
    - dataset.py        -> Code to load and process dataset.
    - rule.py           -> Rule checking implementation.
    - metrics.py        -> Implements several multi-target metrics.
  - model
    - classifiers.py                -> Classifier models.
    - object_detectors.py           -> Object detector models.
