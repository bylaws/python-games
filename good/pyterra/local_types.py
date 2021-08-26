from enum import Enum, IntEnum
import numpy as np

class Image:
    def __init__(self):
        self.textures = []
        self.flipped = False
        self.numpy = False
        self.currentTexture = -1

    def addTexture(self, texture, width, height):
        self.textures.append([texture, [width, height]])

    def setTextureID(self, num):
        self.currentTexture = num

    def getTexture(self):
        if (self.numpy):
            return self.textures[self.currentTexture][0]
        array = np.array(self.textures[self.currentTexture][0])

        if (self.flipped):
            return np.fliplr(array)
        else:
            return array

    def getWidth(self):
        return self.textures[self.currentTexture][1][0]

    def getHeight(self):
        return self.textures[self.currentTexture][1][1]

class Colors(IntEnum):
    TRANSPARENT = 0
    BLACK = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    BLUE = 5
    MAGENTA = 6
    CYAN = 7
    WHITE = 8
    GREY = 9
    BROWN = 10
    GOLD = 10

class Layers(IntEnum):
    BACKGROUND = 0
    MIDDLEGROUND = 1
    FOREGROUND = 2

class GameStates(Enum):
    STARTING = 0
    MENU = 1
    LOADING = 2
    PLAYING = 3

class Tiles(IntEnum):
    AIR = 0
    STONE = 1
    GRASS = 2

class Items(IntEnum):
    PICKAXE = 1000
