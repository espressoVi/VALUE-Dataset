#!/usr/bin/env sh
blender board.blend -b -P render.py -- 0 20000 > /dev/null &
blender board.blend -b -P render.py -- 20000 40000 > /dev/null &
blender board.blend -b -P render.py -- 40000 60000 > /dev/null &
blender board.blend -b -P render.py -- 60000 80000 > /dev/null &
blender board.blend -b -P render.py -- 80000 100000 > /dev/null &
