# Baselines on chessvision dataset.

This folder contains code to predict chess board positions from corresponding images.

## Usage:

  - Update filenames in config.toml
  - Run with

    ```python main.py```

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
