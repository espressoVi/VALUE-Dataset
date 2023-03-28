import bpy
import toml
import os
import sys
from contextlib import contextmanager

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
    _settings = config_dict['render_settings']
    bpy.context.scene.render.image_settings.file_format=_settings['FILE_TYPE']
    bpy.context.scene.render.filepath = os.path.join(_settings['OUTPUT_DIR'],filename)
    bpy.context.scene.render.resolution_x = _settings['RES_X']
    bpy.context.scene.render.resolution_y = _settings['RES_Y']
    with stdout_redirected():
        bpy.ops.render.render(write_still=True)
        bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    render_scene("fuckyou.jpg")
