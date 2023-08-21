import numpy as np
import toml,json, cv2, os
from collections import OrderedDict

config = toml.load("config.toml")

class BBChecker:
    def __init__(self):
        self.bb = self._read_bb()
        res = {}
        for board in self.bb.keys():
            coords = self.compute_coords(self.bb[board])
            if os.path.exists(f"./images/CV_{int(board):07d}.jpg"):
                self.create_image(int(board), coords)
            res[board] = coords
        self._write_bb(res)
    def compute_coords(self, camera):
        res = {}
        for name, lo in camera.items():
            x_min = lo[0] - config['scene']['boxes_x']//2
            x_max = lo[0] + config['scene']['boxes_x']//2
            y_min = lo[1] - config['scene']['boxes_y'][name[0].lower()]
            y_max = lo[1] + 8
            res[name] = [x_min, y_min, x_max, y_max]
        return res
    def create_image(self, idx, coords):
        image = cv2.imread(f"./images/CV_{idx:07d}.jpg")
        for name, lo in coords.items():
            image = cv2.rectangle(image, (lo[0], lo[1]), (lo[2],lo[3]), (0,255,0), 1)
        outfile = f"./tests/CV_{idx:07d}.jpg"
        cv2.imwrite(outfile, image)
    def _read_bb(self):
        with open(config['data']['BB_FILE'], 'r') as f:
            moves = json.load(f)
        return moves
    def _write_bb(self, res):
        with open(config['data']['BoBo_FILE'], 'w') as f:
            json.dump(OrderedDict(sorted(res.items())), f, indent = 2)

def main():
    BBChecker()

if __name__ == "__main__":
    main()
