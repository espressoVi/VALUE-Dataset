import os
import numpy as np
from tqdm import tqdm
from utils.translate import Dataset


def main():
    dataset = Dataset()
    dataset.get_dataset()

    
if __name__ == "__main__":
    main()
