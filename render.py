import bpy
#import toml
import os
import sys
import numpy as np
from contextlib import contextmanager
from mathutils import Vector
import json
from time import perf_counter

config_dict = {}
config_dict['data'] = {'MOVE_FILE':'./data/move.json'} 
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
        self.camera.location.x += X/self.R
        self.camera.location.z += Z/self.R
        self.camera.location = (self.R/self.camera.location.length)*self.camera.location

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

if __name__ == "__main__":
    low, high = int(sys.argv[-2]), int(sys.argv[-1])
    Renderer(low, high).apply_moves()
