import bpy
import toml
import os
import sys
import numpy as np
from contextlib import contextmanager
from mathutils import Vector
import json
from tqdm import tqdm

config_dict = toml.load('config.toml')

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
    def __init__(self):
        self._settings = config_dict['scene']
        bpy.context.scene.render.image_settings.file_format=self._settings['FILE_TYPE']
        bpy.context.scene.render.resolution_x = self._settings['RES_X']
        bpy.context.scene.render.resolution_y = self._settings['RES_Y']
        self.pieces = [i for i in bpy.data.objects.keys() if len(i) == 2]
        self.hide = Vector([0,0,-10]) 

    def apply_moves(self):
        for i,moves in tqdm(self._read_moves().items(), desc="Rendering"):
            self._reset()
            for name, translation in moves.items():
                bpy.data.objects[name].location = Vector(translation)
            self.render_scene(f'CV_{int(i):07d}.jpg')
        bpy.ops.wm.quit_blender()

    def render_scene(self,filename):
        bpy.context.scene.render.filepath = os.path.join(self._settings['OUTPUT_DIR'],filename)
        with stdout_redirected():
            bpy.ops.render.render(write_still=True)
    def _reset(self):
        for piece in self.pieces:
            bpy.data.objects[piece].location = self.hide
    @staticmethod
    def _read_moves():
        with open(config_dict['data']['MOVE_FILE'], 'r') as f:
            moves = json.load(f)
        return moves

if __name__ == "__main__":
    Renderer().apply_moves()
