import numpy as np
from tqdm import tqdm
import toml
from itertools import product

config_dict = toml.load('config.toml')

class Move:
    def __init__(self, START_BOARD):
        self.start = START_BOARD
        self.board_dim = config_dict['constants']['CHESS_BOARD_LEN']
        self.pieces = config_dict['constants']['fen_pieces']
        self.number_to_piece = {val:key for key,val in self.pieces.items()}
        self.map = self._get_abs_coordinates()
        self.get_moves(self.start)

    def get_moves(self, board):
        piece_counter = {}
        moves = {}
        for i,j in product(np.arange(self.board_dim), np.arange(self.board_dim)):
            if board[i][j] != 0:
                piece = self.number_to_piece[board[i][j]]
                if piece in piece_counter:
                    piece_counter[piece] += 1
                else:
                    piece_counter[piece] = 0
                name = piece+str(piece_counter[piece])
                moves[name] = self.map[i][j].tolist()
        return moves
    def _add_position_jitter(self):
        pass
    def _add_rotation_jitter(self):
        pass
    def _get_abs_coordinates(self):
        """ The origin is at the board center, i.e. A1 = (-4,-4)"""
        side = config_dict['scene']['side_length']
        z_val = config_dict['scene']['z_board']
        board_dim = self.board_dim
        result = np.zeros((board_dim, board_dim, 3))
        result[:,:,2] = z_val #SET Z value
        result[:,:,0] = np.repeat(np.expand_dims(np.arange(-board_dim//2+0.5,board_dim//2,1), axis = 0), board_dim, axis=0)*side
        result[:,:,1] = np.repeat(np.expand_dims(np.arange(board_dim//2-0.5,-board_dim//2,-1), axis = 1), board_dim, axis=1)*side
        return result
