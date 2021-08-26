import numpy as np
import pygame
import pygame.locals
import colorama
from enum import Enum
from colorama import Fore, Style, Back
import local_assets as assets
from local_types import Image, GameStates, Colors, Layers
from local_logic import PlayingState, MenuState

inputMonitor = 0
display = 0

def naive_line(y0, x0, y1, x1):
    if abs(x1-x0) < abs(y1-y0):
        xx, yy = naive_line(x0, y0, x1, y1)
        return (yy, xx)

    if x0 > x1:
        return naive_line(y1, x1, y0, x0)

    x = np.arange(x0, x1+1, dtype=float)
    y = x * (y1-y0) / (x1-x0) + (x1*y0-x0*y1) / (x1-x0)

    return np.floor(y).astype(int), x.astype(int)

class Display:
    def __init__(self, method, width, height):
        self.width = width
        self.height = height
        self.method = method

        self.surface = np.zeros((height, width)) 

        self.layers = []
        self.layers.append(np.zeros((height, width))) # Background
        self.layers.append(np.zeros((height, width))) # Middleground
        self.layers.append(np.zeros((height, width))) # Foreground

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def blit(self, image, x, y, layer):
        imageXBound = image.getWidth()
        imageYBound = image.getHeight()

        if (x + image.getWidth() > self.width):
            imageXBound = self.width - x;
        if (y + image.getHeight() > self.height):
            imageYBound = self.height - y;

        self.layers[layer][y:min(y+image.getHeight(), y + imageYBound),x:min(x+image.getWidth(), x + imageXBound)] = image.getTexture()[0:imageYBound, 0:imageXBound]

    def set_layer(self, array, layer):
        self.layers[layer] = array

    def draw_line(self, color, layer, x0, y0, x1, y1):
        x, y = naive_line(y0, x0, y1, x1)
        self.layers[layer][x, y] = color

    def draw(self):

        self.surface = np.where(self.layers[Layers.MIDDLEGROUND] == 0, self.layers[Layers.BACKGROUND], self.layers[Layers.MIDDLEGROUND])
        self.surface = np.where(self.layers[Layers.FOREGROUND] == 0, self.surface, self.layers[Layers.FOREGROUND])
        self.layers = []
        self.layers.append(np.zeros((self.height, self.width))) # Background
        self.layers.append(np.zeros((self.height, self.width))) # Middleground
        self.layers.append(np.zeros((self.height, self.width))) # Foreground


        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')

        print("")
        for row in range(0, self.surface.shape[0] - 1, 2):
            for col, nextcol in zip(self.surface[row], self.surface[row + 1]):
                if (nextcol == 0 or nextcol == 1):
                    color = Fore.BLACK
                elif (nextcol == 2):
                    color = Fore.LIGHTRED_EX
                elif (nextcol == 3):
                    color = Fore.GREEN
                elif (nextcol == 4):
                    color = Fore.LIGHTYELLOW_EX
                elif (nextcol == 5):
                    color = Fore.BLUE
                elif (nextcol == 6):
                    color = Fore.MAGENTA
                elif (nextcol == 7):
                    color = Fore.CYAN
                elif (nextcol == 8):
                    color = Fore.WHITE
                elif (nextcol == 9):
                    color = Fore.LIGHTBLACK_EX
                elif (nextcol == 10):
                    color = Fore.RED
                elif (nextcol == 10):
                    color = Fore.YELLOW

                if (col == 0 or col == 1):
                    bgcolor = Back.BLACK
                elif (col == 2):
                    bgcolor = Back.LIGHTRED_EX
                elif (col == 3):
                    bgcolor = Back.GREEN
                elif (col == 4):
                    bgcolor = Back.LIGHTYELLOW_EX
                elif (col == 5):
                    bgcolor = Back.BLUE
                elif (col == 6):
                    bgcolor = Back.MAGENTA
                elif (col == 7):
                    bgcolor = Back.CYAN
                elif (col == 8):
                    bgcolor = Back.WHITE
                elif (nextcol == 9):
                    bgcolor = Back.LIGHTBLACK_EX
                elif (nextcol == 10):
                    bgcolor = Back.RED
                elif (nextcol == 11):
                    bgcolor = Back.YELLOW
                print(bgcolor + color + u'▄' + Style.RESET_ALL, end="")
            print()
        print()


class Input:
    def __init__(self):
        pygame.display.set_mode((1, 1))

        self.heldKeys = 0
        self.oldHeldKeys = 0

    def checkInputs(self):
        if(self.heldKeys):
           self.oldHeldKeys = self.heldKeys
        self.heldKeys = pygame.key.get_pressed()
    
    def isKeyPressed(self, key):
        return self.heldKeys[key]

    def keyJustPressed(self, key):
        return self.heldKeys[key] == True and self.oldHeldKeys[key] == False

    def keyJustReleased(self, key):
        return self.heldKeys[key] == False and self.oldHeldKeys[key] == True

class Game:
    def __init__(self):
        self.state = MenuState()

    def frame(self, display, inputMonitor):
        inputMonitor.checkInputs()

        self.state = self.state.frame(display, inputMonitor)
        
        display.draw()
        return True

def main():
    colorama.init()
    pygame.init()
    assets.loadAssets()
    inputMonitor = Input()
    display = Display(0, 180, 120);
    game = Game()

    while game.frame(display, inputMonitor):
        for event in pygame.event.get():
            pass
        pygame.time.wait(10)
        pass

main()
