# Chess vision multi label classification task - dataset generation.

## Usage
  - Download a chess database from [Lichess](https://database.lichess.org/). This should be a .pgn.zst file which needs to be extracted.
  - Put chess dataset (extracted pgn file) in folder ''./data'', update the filename in config file.
  - Run the script that generates piece translations and labels.
	```python main.py```
  - This will generate data/move.json, data/labels_all.json, data/fen_all.json
  - Run render.py with the following options to generate images.

	```blender board.blend -b -P render.py -- low_num high_num > /dev/null &```
  - This renders high_num - low_num images, based on indexes assigned in the labels/move file and puts images in ''./images/''
  - Bounding boxes are also generated and placed in ''data''.
