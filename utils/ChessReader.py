import os
import re
import io
import numpy as np
from tqdm import tqdm
import toml
import chess.pgn

config_dict = toml.load('config.toml')

class BoardData:
    def __init__(self, MAX):
        self.dataset = config_dict['data']['DATASET']
        self.MAX = MAX
    def __len__(self):
        return self.MAX
    def __iter__(self):
        self.file = open(self.dataset, 'r')
        self.count = 0
        self.stack = []
        return self
    def __next__(self):
        if self.count > self.MAX:
            self.file.close()
            raise StopIteration
        if len(self.stack) > 0:
            return self.stack.pop()
        line = self.file.readline()
        while '1.' not in line and '{' not in line:
            line = self.file.readline()
        game = chess.pgn.read_game(io.StringIO(line))
        self.stack = self._parse_game(game)
        self.count += len(self.stack)
        return self.stack.pop()

    def _parse_game(self, game):
        result = []
        board = game.board()
        for move in game.mainline_moves():
            result.append(board.fen())
            # ----FILTER---- Add filtration code here if necessary (e.g. unique boards only)
            board.push(move)
        return result
