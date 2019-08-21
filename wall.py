#!/usr/bin/python3
from os import walk, system
from PIL import Image
from random import choice
from screeninfo import get_monitors
import sys


# epsilon is the aceptable distance between the resolutions for a picture to be
# displayble for a given monitor. e.g. if epsilon = 0.1
# for a 1920X1080 monitor and a 2000x1000 image
# |(1920/1080) - (2000/1000)| = 0.2 > epsilon. thus this image would not be
# eligable for display on that monitor for that value of epsilon
epsilon = 0.2

# the feh script responsible for placing the images
script = "feh --bg-fill"

# path to your wallpaper folder
path = "/home/akil/Pictures/wallpaper/"


class picture:
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def __repr__(self):
        return f'{self.__class__}({self.path}, {self.width}, {self.height})'

    def __str__(self):
        return f'{self.path} {self.width}x{self.height}'


monitors = get_monitors()
f = []
_, _, filenames = next(walk(path))
f.extend(filenames)
images = []
for i in f:
    if i[-3:].lower() in ['png', 'jpg', 'jpeg', 'gif']:
        p = path + i
        im = Image.open(p)
        images.append(picture(p, im.width, im.height))
for m in monitors:
    validimages = [i for i in images
                   if abs(m.width / m.height - i.width / i.height) <= epsilon]
    if len(validimages) == 0:
        print(f'0 valid images for display {m}')
        sys.exit(1)
    elif len(validimages) == 1:
        print(f'1 valid images for display {m}')
    script += f' {choice(validimages).path}'
system(script)
