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

def render_scene(filename):
    _settings = config_dict['scene']
    bpy.context.scene.render.image_settings.file_format=_settings['FILE_TYPE']
    bpy.context.scene.render.filepath = os.path.join(_settings['OUTPUT_DIR'],filename)
    bpy.context.scene.render.resolution_x = _settings['RES_X']
    bpy.context.scene.render.resolution_y = _settings['RES_Y']
    with stdout_redirected():
        bpy.ops.render.render(write_still=True)
    bpy.ops.wm.quit_blender()

def read_moves():
    with open(config_dict['data']['MOVE_FILE'], 'r') as f:
        moves = json.load(f)
    return moves

def reset_all():
    for i in bpy.data.objects.keys():
        if len(i) == 2:
            bpy.data.objects[i].location = Vector([0,0,-10]) 

def apply_moves():
    for i,moves in tqdm(enumerate(read_moves().values()),desc = "Rendering"):
        reset_all()
        for name, translation in moves.items():
            piece = bpy.data.objects[name]
            piece.location = Vector(translation)
        render_scene(f'CV_{i:07d}.jpg')

if __name__ == "__main__":
    apply_moves()


#def get_absolute():
#    side = config_dict['scene']['side_length']
#    for obj in config_dict['scene']['3d_objects']:
#        print(obj)
#        print(bpy.data.objects[obj].location/side)
#    bpy.ops.wm.quit_blender()
#
