import os
import re
import io
import numpy as np
from tqdm import tqdm
import toml
import chess.pgn

config_dict = toml.load('config.toml')

class BoardData:
    def __init__(self, ):
        self.data_dir = config_dict['data']['DATA_DIR']
        self.boards = []
        self._load_games()
    def _load_games(self):
        datasets = [f for f in os.listdir(self.data_dir) if 'pgn' in f]
        for dataset in datasets:
            with open(os.path.join(self.data_dir, dataset), 'r') as p:
                for line in tqdm(p, desc = "Loading games"):
                    if '1.' in line and '{' not in line:
                        game = chess.pgn.read_game(io.StringIO(line))
                        self.boards.extend(self._parse_game(game))
                    if len(self.boards) > config_dict['data']['MAX_BOARDS']:
                        break
    def _parse_game(self, game):
        result = []
        board = game.board()
        for move in game.mainline_moves():
            result.append(board.fen())
            # ----FILTER---- Add filtration code here if necessary (e.g. unique boards only)
            board.push(move)
        return result
