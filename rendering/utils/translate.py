import numpy as np
import os
import re
from tqdm import tqdm
import toml
import json
from itertools import product
from utils.ChessReader import BoardData
from collections import OrderedDict

config_dict = toml.load('config.toml')

class Move:
    def __init__(self):
        self.board_dim = config_dict['constants']['CHESS_BOARD_LEN']
        self.pieces = config_dict['constants']['fen_pieces']
        self.side_len = config_dict['scene']['side_length']
        self.z_val = config_dict['scene']['z_board']
        self.number_to_piece = {val:key for key,val in self.pieces.items()}
        self.map = self._get_abs_coordinates()
    def get_moves(self, fen_board):
        board = self._create_array(fen_board)
        piece_counter = {}
        moves = {}
        jitter = self._add_position_jitter()
        for i,j in product(np.arange(self.board_dim), np.arange(self.board_dim)):
            if board[i][j] != 0:
                piece = self.number_to_piece[board[i][j]]
                if piece in piece_counter:
                    piece_counter[piece] += 1
                else:
                    piece_counter[piece] = 0
                name = piece+str(piece_counter[piece])
                moves[name] = (self.map[i][j]+jitter[i][j]).tolist()
        moves['Camera'] = self._camera_jitter()
        return board, moves
    def _camera_jitter(self):
        x,z = np.random.uniform(0,2), max(0,np.random.normal(0.9,0.3))
        return (x,z)
    def _add_position_jitter(self):
        result = np.random.normal(0,self.side_len/16,size = (self.board_dim, self.board_dim, 3))
        result[:,:,2] = 0
        return result
    def _get_abs_coordinates(self):
        """ The origin is at the board center, i.e. A1 = (-4,-4)"""
        board_dim = self.board_dim
        result = np.zeros((board_dim, board_dim, 3))
        result[:,:,2] = self.z_val #SET Z value
        result[:,:,0] = np.repeat(np.expand_dims(np.arange(-board_dim//2+0.5,board_dim//2,1), axis = 0), board_dim, axis=0)*self.side_len
        result[:,:,1] = np.repeat(np.expand_dims(np.arange(board_dim//2-0.5,-board_dim//2,-1), axis = 1), board_dim, axis=1)*self.side_len
        return result
    @staticmethod
    def _create_array(fen_board):
        nil = config_dict['constants']['EMPTY_DELIMITER']
        piece_dict = config_dict['constants']['fen_pieces']
        final = []
        rank_array = fen_board.split()[0].split('/')
        for i,files in enumerate(rank_array):
            new = files
            for n in re.findall(r'[1-8]',files):
                new = new.replace(n,nil*int(n))
            final.append(np.array([piece_dict[i] for i in list(new)]))
        return np.array(final)

class Dataset:
    def __init__(self,):
        MAX = config_dict['data']['MAX_BOARDS']
        self.dataset = BoardData(MAX)
        self.mover = Move()
    def get_dataset(self):
        moves_dict, labels_dict, fen_dict = {},{},{}
        unique_ids = list(range(len(self.dataset)))
        np.random.shuffle(unique_ids)
        for unique_id, fen_board in tqdm(zip(unique_ids, self.dataset), total = len(self.dataset)):
            board, moves = self.mover.get_moves(fen_board)
            moves_dict[unique_id] = moves
            labels_dict[unique_id] = board.tolist()
            fen_dict[unique_id] = fen_board
            unique_id+=1
        with open(config_dict['data']['MOVE_FILE'], 'w') as f:
            json.dump(OrderedDict(sorted(moves_dict.items())), f, indent = 2)
        with open(config_dict['data']['LABEL_FILE'], 'w') as f:
            json.dump(OrderedDict(sorted(labels_dict.items())), f, indent = 2)
        with open(config_dict['data']['FEN_FILE'], 'w') as f:
            json.dump(OrderedDict(sorted(fen_dict.items())), f, indent = 2)
