# FlueGenerator

## About
This project allows processing music files, extracting frequencies and calculating flutes lengths.
This project contains the Panpipe submodule which is running through Blender.

## setup
Install the required packages:
```
pip install -r requirements
```
You'll also need to install Blender to use the Panpipe submodule (it was developed using Blender 2.93.5).
If you want to use mp3 music files instead of wav music files, you'll also need to install ffmpeg.

## CLI example

Simple example to create stl file of 6 flutes with holes for the first 8 seconds some wav file:
```
python -W ignore main.py --no-sorted --amount 12 --seconds 8 --file_path data/Seven_Nation_Army.wav
```

Simple example to create stl file of 6 flutes without holes and without plots for some wav file:
```
python -W ignore main.py --no-plot --no-sorted --no-holes -a 6 -s 8 -f data/Seven_Nation_Army.wav
```

We can path the '--output', '-dimensions', and '--sorted/--no-sorted' parameters that are used in the Panpipe submodlue 
#### For information about the Panpipe submodule and its cli parameters view [panpipe/README.md](panpipe/README.md)
![Panpipes!](data/result_image.jpeg "Title")

