import bpy
from bpy_extras.object_utils import world_to_camera_view as wcv
#import toml
import os
import sys
import numpy as np
from contextlib import contextmanager
from mathutils import Vector
import json
from time import perf_counter
from collections import OrderedDict
from itertools import product

config_dict = {}
config_dict['data'] = {'MOVE_FILE':'./data/move.json', 'BB_FILE':'./data/bb_all.json', 'GRID_FILE':'./data/grid_all.json'}
config_dict['scene'] = {"OUTPUT_DIR":'./images/', "FILE_TYPE":'JPEG', "RES_X":512, "RES_Y":512, "side_length":0.106768, "z_board":0.0009}

@contextmanager
def stdout_redirected(to=os.devnull):
    fd = sys.stdout.fileno()
    def _redirect_stdout(to):
        sys.stdout.close()
        os.dup2(to.fileno(), fd)
        sys.stdout = os.fdopen(fd, 'w')
    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open(to, 'w') as file:
            _redirect_stdout(to=file)
        try:
            yield
        finally:
            _redirect_stdout(to=old_stdout)

class Renderer:
    def __init__(self, low, high):
        self._settings = config_dict['scene']
        bpy.context.scene.render.image_settings.file_format=self._settings['FILE_TYPE']
        bpy.context.scene.render.resolution_x = self._settings['RES_X']
        bpy.context.scene.render.resolution_y = self._settings['RES_Y']
        self.pieces = [i for i in bpy.data.objects.keys() if len(i) == 2]
        self.camera = bpy.data.objects['Camera']
        self.R = self.camera.location.length
        self.hide = Vector([0,0,-10]) 
        self.low = low
        self.high = high
    def apply_moves(self):
        g_start = perf_counter()
        for i,moves in self._read_moves().items():
            start = perf_counter()
            self._reset()
            self.update_camera(*moves['Camera'])
            for name, translation in moves.items():
                if name == "Camera":
                    continue
                bpy.data.objects[name].location = Vector(translation)
            self.render_scene(f'CV_{int(i):07d}.jpg')
            end = perf_counter()
            print(f"Rendering image #{int(i)-self.low} of {self.high-self.low}, took {end - start:.2f}s, Total time = {(end - g_start)/60:.1f} minutes", end="\r")
        print()
        bpy.ops.wm.quit_blender()
    def update_camera(self, X, Z):
        self.camera.location += Vector((X/self.R, 0, Z/self.R))
        self.camera.location *= (self.R/self.camera.location.length)
    def render_scene(self,filename):
        bpy.context.scene.render.filepath = os.path.join(self._settings['OUTPUT_DIR'],filename)
        with stdout_redirected():
            bpy.ops.render.render(write_still=True)
    def _reset(self):
        self.camera.location = Vector((-1.93420338, -1.87062883, 1.70655179))
        for piece in self.pieces:
            bpy.data.objects[piece].location = self.hide
    def _read_moves(self):
        with open(config_dict['data']['MOVE_FILE'], 'r') as f:
            moves = json.load(f)
        moves = {key:val for key,val in moves.items() if self.low <= int(key) < self.high}
        return moves

class BoundingBoxes(Renderer):
    def __init__(self, low, high):
        super().__init__(low, high)
        self.camera = bpy.context.scene.camera
    def update_camera(self, X, Z):
        self.camera.location += Vector((X/self.R, 0, Z/self.R))
        self.camera.location *= (self.R/self.camera.location.length)
        bpy.context.view_layer.update()
    def get_boxes(self):
        res = {}
        for i,moves in self._read_moves().items():
            self._reset()
            self.update_camera(*moves['Camera'])
            for name, translation in filter(lambda x: len(x[0]) == 2, moves.items()):
                bpy.data.objects[name].location = Vector(translation)
            res[i] = self._get_coordinates(moves)
        self._write_bb(res)
        bpy.ops.wm.quit_blender()
    def _write_bb(self, res):
        with open(config_dict['data']['BB_FILE'], "w") as f:
            json.dump(OrderedDict(sorted(res.items())), f, indent = 2)
    def _get_coordinates(self, moves):
        res = {}
        x_res, y_res = config_dict['scene']['RES_X'], config_dict['scene']['RES_Y']
        for name in filter(lambda x: len(x) == 2, moves.keys()):
            obj = bpy.data.objects[name]
            co_2d = wcv(bpy.context.scene, self.camera, obj.location)
            x_pos, y_pos = round(x_res*co_2d.x), round(y_res*co_2d.y)
            res[name] = [x_pos, y_res - y_pos]
        return res
class Grid(BoundingBoxes):
    def __init__(self, low, high):
        super().__init__(low, high)
        self.board = self._get_grid_points()
    def _get_grid_points(self):
        board_dim, side_len = 8, config_dict['scene']['side_length']
        result = np.zeros((board_dim, board_dim, 3))
        result[:,:,2] = config_dict['scene']['z_board'] #SET Z value
        result[:,:,0] = np.repeat(np.expand_dims(np.arange(-board_dim//2+0.5,board_dim//2,1), axis = 0), board_dim, axis=0)*side_len
        result[:,:,1] = np.repeat(np.expand_dims(np.arange(board_dim//2-0.5,-board_dim//2,-1), axis = 1), board_dim, axis=1)*side_len
        return result
    def get_grid(self):
        res = {}
        for i,moves in self._read_moves().items():
            self._reset()
            self.update_camera(*moves['Camera'])
            x,y = self._get_coordinates()
            res[i] = [(int(i),int(j)) for i,j in zip(x.flatten(),y.flatten())]
        self._write_grid(res)
        bpy.ops.wm.quit_blender()
    def _get_coordinates(self):
        res1, res2 = np.zeros((8,8), dtype = int), np.zeros((8,8), dtype = int)
        x_res, y_res = config_dict['scene']['RES_X'], config_dict['scene']['RES_Y']
        for i,j in product(range(8),range(8)):
            co_2d = wcv(bpy.context.scene, self.camera, Vector(self.board[i,j,:]))
            x_pos, y_pos = round(x_res*co_2d.x), round(y_res*co_2d.y)
            res1[i,j], res2[i,j] = x_pos, y_res-y_pos
        return res1,res2
    def _write_grid(self, res):
        with open(config_dict['data']['GRID_FILE'], "w") as f:
            json.dump(OrderedDict(sorted(res.items())), f, indent = 2)

if __name__ == "__main__":
    low, high = int(sys.argv[-2]), int(sys.argv[-1])
    #Renderer(low, high).apply_moves()
    #BoundingBoxes(low, high).get_boxes()
    Grid(low, high).get_grid()
