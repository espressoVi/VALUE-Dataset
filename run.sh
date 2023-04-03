#!/usr/bin/env sh
blender board.blend -b -P render.py -- 0 10000 > /dev/null &
blender board.blend -b -P render.py -- 10000 20000 > /dev/null &
blender board.blend -b -P render.py -- 20000 30000 > /dev/null &
blender board.blend -b -P render.py -- 30000 40000 > /dev/null &
