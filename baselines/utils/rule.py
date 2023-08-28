#!/usr/bin/env python
import numpy as np
from collections import Counter
import toml, json
from tqdm import tqdm
from itertools import combinations

config = toml.load("config.toml")

class Rules:
    def __init__(self):
        self.board_len = config["constants"]["CHESS_BOARD_LEN"]
        self.piece2num = config["constants"]["fen_pieces"]
        self.num2piece = {value:key for key, value in self.piece2num.items()}
        self.empty = lambda piece: piece == configF["constants"]["EMPTY"]
        self.black = lambda piece: piece.islower() and not self.empty(piece)
        self.white = lambda piece: piece.isupper() and not self.empty(piece)
    def check(self, arr:np.ndarray) -> bool:
        arr = self._validate(arr)
        black, white = self._split_black_white(arr)
        if not self._king_okay(black, white):
            return False
        if np.where(black > 0, 1, 0).sum() > 16 or np.where(white > 0, 1, 0).sum() > 16:
            return False
        black_counts, white_counts = self._count_pieces(black), self._count_pieces(white)
        if black_counts['p'] > 8 or white_counts['P'] > 8:
            return False
        if self._first_or_last_rank_pawn(arr):
            return False
        if black_counts['p'] == 8:  #No promotions
            if not self._check_counts(black_counts, promotion = False):
                return False
            if black_counts['b'] == 2 and not self._check_bishop(black, 'b'):
                return False
        elif black_counts['p'] < 8:
            if not self._check_counts(black_counts, promotion = True):
                return False
        if white_counts['P'] == 8:  #No promotions
            if not self._check_counts(white_counts, promotion = False):
                return False
            if white_counts['B'] == 2 and not self._check_bishop(white,'B'):
                return False
        elif white_counts['P'] < 8:
            if not self._check_counts(white_counts, promotion = True):
                return False
        return True
    def analyze(self, arr):
        arr = self._validate(arr)
        an = {"count":0,"loc":0,"ifcount":0,"ifloc":0}
        black, white = self._split_black_white(arr)
        black_counts, white_counts = self._count_pieces(black), self._count_pieces(white)
        """ Counting """
        if np.where(black == self.piece2num['k'], 1, 0).sum() != 1:
            an["count"] += 1
        if np.where(white == self.piece2num['K'], 1, 0).sum() != 1:
            an["count"] += 1
        if np.where(black > 0, 1, 0).sum() > 16:
            an["count"] += 1
        if np.where(white > 0, 1, 0).sum() > 16:
            an["count"] += 1
        if black_counts['p'] > 8:
            an["count"] += 1
        if white_counts['P'] > 8:
            an["count"] += 1
        """ Localizing """
        if self._first_or_last_rank_pawn(arr):
            _p = np.logical_or(np.where(np.append(arr[0], arr[-1]) == self.piece2num['p'], True, False), 
                           np.where(np.append(arr[0], arr[-1]) == self.piece2num['P'], True, False))
            an["loc"]+=_p.astype(int).sum()
        x = zip(*np.where(black == self.piece2num['k']))
        y = zip(*np.where(white == self.piece2num['K']))
        kings = list(x)+list(y)
        for k,K in combinations(kings,2):
            x_d, y_d = np.abs(k[0] - K[0]), np.abs(k[1] - K[1])
            if x_d < 2 and y_d < 2:
                an["loc"]+=1
        """ Conditional Counting """
        if black_counts['p'] == 8 and not self._check_counts(black_counts, promotion = False):
            an["ifcount"]+=1 
        if white_counts['P'] == 8 and not self._check_counts(white_counts, promotion = False):
            an["ifcount"]+=1 
        if black_counts['p'] < 8 and not self._check_counts(black_counts, promotion = True):
            an["ifcount"]+=1 
        if white_counts['P'] < 8 and not self._check_counts(white_counts, promotion = True):
            an["ifcount"]+=1 
        """ Conditional localizing """
        if black_counts['p'] == 8 and black_counts['b'] == 2 and not self._check_bishop(black,'b'):
            an["ifloc"]+=1
        if white_counts['P'] == 8 and white_counts['B'] == 2 and not self._check_bishop(white,'B'):
            an["ifloc"]+=1
        return an
        
    def _check_bishop(self, arr, col):
        x,y = np.where(arr == self.piece2num[col])
        res = (x+y)%2
        return res[0] != res[-1]
    def _check_counts(self, counts, promotion = False):
        if not promotion:
            return all([(counts['b'] <= 2), (counts['n'] <= 2), (counts['r'] <= 2), (counts['q'] <= 1),
                        (counts['B'] <= 2), (counts['N'] <= 2), (counts['R'] <= 2), (counts['Q'] <= 1),])
        else:
            missing_pawns = (8 - counts['p'], 8 - counts['P'])
            extra_pieces = (max(0,counts['q'] - 1) + max(0,counts['b'] -2) + max(0,counts['n'] - 2), + max(0,counts['r']-2)
                           ,max(0,counts['Q'] - 1) + max(0,counts['B'] -2) + max(0,counts['N'] - 2), + max(0,counts['R']-2))
            return all([i>=j for i,j in zip(missing_pawns, extra_pieces)])

    def _king_okay(self, black, white):
        """ Checks if both kings exist and they are not adjacent """
        i,j = np.where(black == self.piece2num['k'])
        m,n = np.where(white == self.piece2num['K'])
        if len(i) == len(j) == len(m) == len(n) == 1:
            x_d, y_d = np.abs(i[0] - m[0]), np.abs(j[0] - n[0])
            if x_d >= 2 or  y_d >= 2:
                return True
        return False
    def _first_or_last_rank_pawn(self, arr):
        _p = np.logical_or(np.where(np.append(arr[0], arr[-1]) == self.piece2num['p'], True, False), 
                           np.where(np.append(arr[0], arr[-1]) == self.piece2num['P'], True, False))
        return np.any(_p)
    def _validate(self, arr:np.ndarray) -> np.ndarray:
        assert isinstance(arr, np.ndarray)
        arr = arr.astype(int).reshape(self.board_len, self.board_len)
        assert np.amax(arr) <= 12 and np.amin(arr) >= 0
        return arr
    def _count_pieces(self, arr: np.ndarray) -> dict:
        counts = Counter(arr.flatten())
        base = {piece:0 for piece in self.piece2num.keys()}
        base.update({self.num2piece[key]:value for key, value in counts.items()})
        return base
    @staticmethod
    def _split_black_white(arr: np.ndarray) -> (np.ndarray, np.ndarray):
        white = np.where(np.where(arr <= 6, arr, 0) >= 1, arr, 0).astype(int)
        black = np.where(np.where(arr <= 12, arr, 0) >= 7, arr, 0).astype(int)
        return black, white

def main():
    rules = Rules()
    board = np.array([[10, 8, 9, 11, 12,  9, 8,10],
                     [ 7,  7,  7,  7,  7, 7, 7, 7],
                     [ 0,  0,  0,  0,  0, 0, 0, 0],
                     [ 0,  0,  0,  0,  0, 0, 0, 0],
                     [ 0,  0,  0,  0,  0, 0, 0, 0],
                     [ 0,  0,  0,  0,  0, 0, 0, 0],
                     [ 1,  1,  1,  1,  1, 1, 1, 1],
                     [ 4,  2,  3,  5,  6, 3, 2, 4],])

    isValid, error = rules.check(np.array(board))

if __name__ == "__main__":
    main()
