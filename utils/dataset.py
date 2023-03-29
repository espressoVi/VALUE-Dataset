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
        self.EMPTY = config_dict['constants']['EMPTY_DELIMITER']
        self.games = []
        self.boards = []
        self._load_games()
        self._parse_games()
        self.dataset = np.array([self._create_array(board, self.EMPTY) for board in self.boards])
        self.START = self._create_array(chess.STARTING_BOARD_FEN, self.EMPTY)
    def _load_games(self):
        datasets = [f for f in os.listdir(self.data_dir) if 'pgn' in f]
        for dataset in datasets:
            with open(os.path.join(self.data_dir, dataset)) as p:
                string_games = [io.StringIO(l) for l in p.readlines() if '1.' in l]
            for _game in tqdm(string_games, desc = "Loading games"):
                try:
                    game = chess.pgn.read_game(_game)
                except:
                    pass
                else:
                    self.games.append(game)
    def _parse_games(self):
        for game in tqdm(self.games):
            board = game.board()
            for move in game.mainline_moves():
                self.boards.append(board.fen())
                #FILTER??
                board.push(move)
    @staticmethod
    def _create_array(fen, nil):
        dims = config_dict['constants']['CHESS_BOARD_LEN']
        final = []
        rank_array = fen.split()[0].split('/')
        for i,files in enumerate(rank_array):
            new = files
            for n in re.findall(r'[1-8]',files):
                new = new.replace(n,nil*int(n))
            final.append(np.array([config_dict['constants']['fen_pieces'][i] for i in list(new)]))
        final = np.array(final)
        return final
