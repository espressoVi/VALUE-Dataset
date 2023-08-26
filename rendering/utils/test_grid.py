import numpy as np
import toml,json, cv2, os
from collections import OrderedDict

config = toml.load("config.toml")

class GridChecker:
    def __init__(self):
        self.grid = self._read_grid()
        for board, coords in self.grid.items():
            if os.path.exists(f"./images/CV_{int(board):07d}.jpg"):
                self.create_image(int(board), coords)
    def create_image(self, idx, coords):
        image = cv2.imread(f"./images/CV_{idx:07d}.jpg")
        for i in coords:
            image = cv2.circle(image, i, 2, (0,255,0), 2)
        outfile = f"./tests/CV_{idx:07d}.jpg"
        cv2.imwrite(outfile, image)
    def _read_grid(self):
        with open(config['data']['GRID_FILE'], 'r') as f:
            moves = json.load(f)
        return moves

def main():
    GridChecker()

if __name__ == "__main__":
    main()
