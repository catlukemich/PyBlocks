import random

import pygame
from pygame.locals import *


# Image loader functions
images = {}

def loadImage(path):
    try:
        global images
        if path in images:
            return images[path]
        else:
            img = pygame.image.load(path).convert_alpha()
            images[path] = img
            return img
    except FileNotFoundError:
        print(path + " not found")


fonts = {}

def loadFont(path, size):
    key = path + "/" + str(size)
    if key in fonts:
        return fonts[key]
    else:
        font = pygame.font.Font(path, size)
        fonts[key] = font
        return font