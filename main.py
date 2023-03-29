import os
import numpy as np
from tqdm import tqdm
import toml
import json
from utils.dataset import BoardData
from utils.translate import Move

config_dict = toml.load('config.toml')

def save_moves(boards, mover, batch_size = 1):
    moves_dict = {}
    for i,board in enumerate(boards):
        moves = mover.get_moves(board)
        moves_dict[i] = moves
    with open(config_dict['data']['MOVE_FILE'], 'w') as f:
        json.dump(moves_dict, f, indent = 4)

def main():
    dataset = BoardData()
    mover = Move(dataset.START)
    save_moves(dataset.dataset, mover)

    
if __name__ == "__main__":
    main()
