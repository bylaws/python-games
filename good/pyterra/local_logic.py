import pygame
import local_assets as assets
from local_types import Image, GameStates, Colors, Layers, Tiles, Items
import numpy as np
class MenuState:
    def __init__(self):
        self.selected = 0
        pass

    def id(self):
        return GameStates.MENU

    def frame(self, display, inputMonitor):
      
        if (inputMonitor.isKeyPressed(pygame.K_RETURN)):
            return PlayingState(display)
        display.blit(assets.BACKGROUND_WORLD, 0, display.getHeight() - assets.BACKGROUND_WORLD.getHeight(), Layers.BACKGROUND)

        textX = int((display.getWidth() / 2) - (assets.PLAY_TEXT.getWidth() / 2))
        textY = 5
        
        display.blit(assets.PLAY_TEXT, textX, textY, Layers.FOREGROUND)

        if (inputMonitor.isKeyPressed(pygame.K_DOWN)):
            self.selected = 1

        if (inputMonitor.isKeyPressed(pygame.K_UP)):
            self.selected = 0

        if (self.selected == 0):
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY - 2, textX + assets.PLAY_TEXT.getWidth() + 2, textY - 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY - 2, textX - 2, textY + assets.PLAY_TEXT.getHeight() + 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY + assets.PLAY_TEXT.getHeight() + 2, textX + assets.PLAY_TEXT.getWidth() + 2, textY + assets.PLAY_TEXT.getHeight() + 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX + assets.PLAY_TEXT.getWidth() + 2, textY - 2, textX + assets.PLAY_TEXT.getWidth() + 2, textY + assets.PLAY_TEXT.getHeight() + 2)
       
        textX = int(display.getWidth() - (assets.QUIT_TEXT.getWidth() * 2))
        textY = int(display.getHeight() - (assets.QUIT_TEXT.getHeight() * 3))
        
        display.blit(assets.QUIT_TEXT, textX, textY, Layers.FOREGROUND)

        if (self.selected == 1):
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY - 2, textX + assets.QUIT_TEXT.getWidth() + 2, textY - 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY - 2, textX - 2, textY + assets.QUIT_TEXT.getHeight() + 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX - 2, textY + assets.QUIT_TEXT.getHeight() + 2, textX + assets.QUIT_TEXT.getWidth() + 2, textY + assets.QUIT_TEXT.getHeight() + 2)
            display.draw_line(Colors.WHITE, Layers.FOREGROUND, textX + assets.QUIT_TEXT.getWidth() + 2, textY - 2, textX + assets.QUIT_TEXT.getWidth() + 2, textY + assets.QUIT_TEXT.getHeight() + 2)
        return self

class World:
    def __init__(self, displayWidth, displayHeight):
        self.world = np.zeros((400, 2000))
        self.world[200:400, 0:2000] = Tiles.STONE
        self.world[200, 0:2000] = Tiles.GRASS
        self.world[200:400, 1000] = Tiles.STONE
        self.world[195, 1000] = Tiles.STONE
        self.world[198, 1001] = Tiles.STONE
        self.displayWidth = displayWidth
        self.xStart = 0
        self.yStart = 0
        self.displayHeight = displayHeight

    def getBlock(self, x, y):
        return self.world[y, x]

    def setBlock(self, block, x, y):
        self.world[y, x] = block

    def getVisibleImage(self, playerX, playerY, cursorX, cursorY):
        yStart = int(playerY - self.displayHeight / 10)
        yEnd = int(playerY + self.displayHeight / 10)
        xStart = int(playerX - self.displayWidth / 10)
        xEnd = int(playerX + self.displayWidth / 10)
        self.xStart = xStart
        self.yStart = yStart
        base = self.world[yStart:yEnd, xStart:xEnd]
        
        image = np.zeros((base.shape[0] * 5, base.shape[1] * 5))
        pos = 0
        pos2 = 0
        relX= 0
        relY= 0
        for row in base:
            for col in row:
                if(relX == cursorX and relY == cursorY):
                    image[pos2:pos2 + 5, pos:pos + 5] = np.where(assets.CURSOR == 0, assets.tileMap[int(col)][0:5, 0:5], assets.CURSOR)
                else:
                    image[pos2:pos2 + 5, pos:pos + 5] = assets.tileMap[int(col)][0:5, 0:5]
                pos += 5
                relX += 1
            relX =  0
            relY += 1
            pos2 += 5
            pos = 0

        return image[0:self.displayHeight, 0:self.displayWidth];

class Item:
    def __init__(self, item):
        self.texture = assets.itemMap[item - 1000]
        print(self.texture)

    def use(self, player, world, x, y):
        pass

class TileItem(Item):
    def __init__(self, tile):
        self.texture = assets.tileMap[tile]
        self.tile = tile

    def use(self, player, world, x, y):
        if (world.getBlock(x, y) == Tiles.AIR):
            world.setBlock(self.tile, x, y)
            return True
        return False

class Pickaxe(Item):
    def __init__(self):
        super().__init__(Items.PICKAXE)

    def use(self, player, world, x, y):
        block = world.getBlock(x, y)
        if (block == Tiles.STONE or block == Tiles.GRASS):
            for i in player.inventory.contents:
                try:
                    if(i.tile == block):
                        world.setBlock(Tiles.AIR, x, y)
                        return True
                except AttributeError:
                    continue;

            player.inventory.give(1, block)
            world.setBlock(Tiles.AIR, x, y)
        return False

class Inventory:
    def __init__(self, startingItems):
        self.contents = startingItems
        self.currentItem = 0
        self.image = Image()
        self.image.numpy = True

    def give(self, item, amount):
        if (int(item) == int(Items.PICKAXE)):
            newItem = Pickaxe()
        elif (int(item) < 1000):
            newItem = TileItem(item)
        self.contents.append(newItem)

    def frame(self, display, inputMonitor):
        display.draw_line(Colors.WHITE, Layers.FOREGROUND, 0, 0, 0, 8)
        display.draw_line(Colors.WHITE, Layers.FOREGROUND, 0, 0, 49, 0)
        display.draw_line(Colors.WHITE, Layers.FOREGROUND, 49, 8, 49, 0)
        display.draw_line(Colors.WHITE, Layers.FOREGROUND, 0, 8, 49, 8)

        array = np.ones((5, 45))

        cursor = 0
        cursor1 = 0

        for i in range(len(self.contents)):
            if (i == self.currentItem):
                display.draw_line(Colors.WHITE, Layers.FOREGROUND, 1 + (i*5) + i, 1, 1 + ((i+1)*5) + i, 1)
                display.draw_line(Colors.WHITE, Layers.FOREGROUND, 1 + (i*5) + i, 7, 1 + ((i+1)*5) + i, 7)
                display.draw_line(Colors.WHITE, Layers.FOREGROUND, 1 + (i*5) + i, 1, 1 + ((i)*5) + i, 7)
                display.draw_line(Colors.WHITE, Layers.FOREGROUND, 2 + ((i+1)*5) + i, 1, 2 + ((i+1)*5) + i, 7)
            array[0:5, (i*5)+i:((i+1)*5)+i] = self.contents[i].texture

        self.image.addTexture(array, 45, 5)
        self.image.setTextureID(0)

        display.blit(self.image, 2, 2, Layers.BACKGROUND)

        if (inputMonitor.isKeyPressed(pygame.K_1)):
            if (len(self.contents) > 0):
                self.currentItem = 0
        elif (inputMonitor.isKeyPressed(pygame.K_2)):
            if (len(self.contents) > 1):
                self.currentItem = 1
        elif (inputMonitor.isKeyPressed(pygame.K_3)):
            if (len(self.contents) > 2):
                self.currentItem = 2
        elif (inputMonitor.isKeyPressed(pygame.K_4)):
            if (len(self.contents) > 3):
                self.currentItem = 3
        elif (inputMonitor.isKeyPressed(pygame.K_5)):
            if (len(self.contents) > 4):
                self.currentItem = 4
        elif (inputMonitor.isKeyPressed(pygame.K_6)):
            if (len(self.contents) > 5):
                self.currentItem = 5
        elif (inputMonitor.isKeyPressed(pygame.K_7)):
            if (len(self.contents) > 6):
                self.currentItem = 6
        elif (inputMonitor.isKeyPressed(pygame.K_8)):
            if (len(self.contents) > 7):
                self.currentItem = 7

    def use(self, player, world, x, y):
        self.contents[self.currentItem].use(player, world, x, y)

class Player:
    def __init__(self):
        self.x = 1000
        self.y = 199
        self.velocity = [0, 0]
        self.inventory = Inventory([Pickaxe(), TileItem(Tiles.STONE)])

    def frame(self, display, inputMonitor, world):
        if (inputMonitor.keyJustPressed(pygame.K_SPACE)):
            self.velocity[1] += 5

        if (inputMonitor.keyJustPressed(pygame.K_RIGHT)):
            self.velocity[0] += 1

        if (inputMonitor.keyJustPressed(pygame.K_LEFT)):
            self.velocity[0] -= 1

        if (inputMonitor.keyJustReleased(pygame.K_RIGHT)):
            if not (self.velocity[0] == 0):
                self.velocity[0] -= 1

        if (inputMonitor.keyJustReleased(pygame.K_LEFT)):
            if not (self.velocity[0] == 0):
                self.velocity[0] += 1

        self.velocity[1] -= 1
        


        if (self.velocity[1] < 0):
            for i in range(0, self.velocity[1], -1):
                if (world.getBlock(self.x, self.y + 1 - i)):
                    self.velocity[1] = i
                    break;
        elif (self.velocity[1] > 0):
            for i in range(0, self.velocity[1]):
                if (world.getBlock(self.x, self.y - 1 - i)):
                    self.velocity[1] = i - 2
                    break;
        
        for k in [-1, 0]:
            if (self.velocity[0] < 0):
                assets.PLAYER_SPRITE.flipped = True
                for i in range(0, self.velocity[0], -1):
                    if (world.getBlock(self.x - 1 - i, self.y + k)):
                        self.velocity[0] = i
                        break;
            elif (self.velocity[0] > 0):
                assets.PLAYER_SPRITE.flipped = False
                for i in range(0, self.velocity[0]):
                    if (world.getBlock(self.x + 1 + i, self.y + k)):
                        self.velocity[0] = i
                        break;
        
        self.x += self.velocity[0]
        self.y -= int(self.velocity[1])

        display.blit(assets.PLAYER_SPRITE, int(display.width / 2), int(display.height / 2 - 5), Layers.MIDDLEGROUND)
        self.inventory.frame(display, inputMonitor)

class Cursor:
    def __init__(self, displayWidth, displayHeight):
        self.displayWidth = int(displayWidth / 5)
        self.displayHeight = int(displayHeight / 5)
        self.x = 0
        self.y = 0

    def frame(self, inputMonitor):
        if (inputMonitor.isKeyPressed(pygame.K_w)):
            self.y = max(0, self.y - 1)
        if (inputMonitor.isKeyPressed(pygame.K_s)):
            self.y = min(self.displayHeight, self.y + 1)
        if (inputMonitor.isKeyPressed(pygame.K_d)):
            self.x = min(self.displayWidth, self.x + 1)
        if (inputMonitor.isKeyPressed(pygame.K_a)):
            self.x = max(0, self.x - 1)

class PlayingState:
    def __init__(self, display):
        self.selected = 0
        self.world = World(display.getWidth(), display.getHeight())
        self.player = Player()
        self.cursor = Cursor(display.width, display.height)

    def id(self):
        return GameStates.PLAYING

    def frame(self, display, inputMonitor):
        self.cursor.frame(inputMonitor)
        display.set_layer(self.world.getVisibleImage(self.player.x, self.player.y, self.cursor.x, self.cursor.y), Layers.MIDDLEGROUND)
        if (inputMonitor.isKeyPressed(pygame.K_e)):
            self.player.inventory.use(self.player, self.world, self.cursor.x + self.world.xStart, self.cursor.y + self.world.yStart)
        self.player.frame(display, inputMonitor, self.world)
        return self


