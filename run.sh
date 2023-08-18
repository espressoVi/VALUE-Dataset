#!/usr/bin/env sh
blender board.blend -b -P render.py -- 0 100 > /dev/null &
