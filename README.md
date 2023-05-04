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

## Notes
* Look at YOLO image models.
* Look at mask-RCNN

## Usage
1. Put chess dataset (extracted) in folder data.
2. Run the script that generates piece translations and labels.
	```python main.py```
3. Run render.py with the following options to generate images.
	```blender board.blend -b -P render.py -- low_num high_num > /dev/null &```
4. This renders high_num - low_num images, based on indexes assigned in the labels/move file.
