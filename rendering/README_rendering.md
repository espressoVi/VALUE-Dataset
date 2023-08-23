# Chess vision multi label classification task - DATASET CREATED.

## Done
* Generated blender 3D model chess board.
* A1 - Extract position information from 3D Scene
* B0 - PGN reading and converting to FEN (python-chess)
* B1 - FEN to numpy array (save as npy) extract label information.
* B2 - Create dataset.
* C1 - Compute absolute translations.
* C2 - Get final scene.
* C3 - Save images and corresponding label information.
* Check  if scene works in 204.
* Generated 329942 images and corresponding labels.
* Dataset generation, cleanup, etc completed.

## Usage
  - Put chess dataset (extracted) in folder data (pgn file).
  - Run the script that generates piece translations and labels.
	```python main.py```

  - This will generate data/move.json, data/labels_all.json, data/fen_all.json

  - Run render.py with the following options to generate images.
	```blender board.blend -b -P render.py -- low_num high_num > /dev/null &```
  - This renders high_num - low_num images, based on indexes assigned in the labels/move file and puts images in images/
  Also generates bounding boxes.
