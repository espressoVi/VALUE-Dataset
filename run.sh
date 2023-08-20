#!/usr/bin/env sh
blender board.blend -b -P render.py -- 0 40000 > /dev/null &
blender board.blend -b -P render.py -- 40000 80000 > /dev/null &
blender board.blend -b -P render.py -- 80000 120000 > /dev/null &
blender board.blend -b -P render.py -- 120000 160000 > /dev/null &
blender board.blend -b -P render.py -- 160000 200000 > /dev/null &
blender board.blend -b -P render.py -- 200000 220000 > /dev/null &
