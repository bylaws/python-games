import pygame,random,time,sys,math
from enum import IntEnum
from pygame.locals import *

WIDTH = 1280
HEIGHT = 1024

RENDERWIDTH = 320
RENDERHEIGHT = 256

TEXTURE_PREFIX = "textures/"
TEXTURE_NAMES = ["tilegrass.png", "tilestone.png", "tileflower.png", "tilestone.png", "tilestump.png", "tiletechmetalborders.png", "tiletechmetal.png", "tiletechmetalbarrel.png"]

TILE_SIZE = 16

class TextureIds(IntEnum):
    GRASS = 0,
    ROCK = 1,
    FLOWER = 2,
    STONE = 3,
    STUMP = 4,
    TECH_METAL_BORDER = 5,
    TECH_METAL = 6,
    TECH_METAL_BARREL = 7


class TileMap:
    def __init__(self, array, textures):
        self.width = RENDERWIDTH + TILE_SIZE
        self.height = RENDERHEIGHT + TILE_SIZE
        self.renderTexture = pygame.Surface((self.width, self.height))
        self.textures = []
        for path in textures:
            self.textures.append(pygame.image.load(TEXTURE_PREFIX + path))
            
        self.tileArray = array

        self.scrollX = 0
        self.scrollY = 0

    def updateTexture(self, X, Y):
        self.scrollX += X
        self.scrollY += Y

        y = 0
        if (self.scrollX < 0):
            self.scrollX = 0
        
        if (self.scrollY < 0):
            self.scrollY = 0

        for i in range(self.scrollY // TILE_SIZE, (self.scrollY // TILE_SIZE) + (self.height // TILE_SIZE)):
            x = 0
            for k in range(self.scrollX // TILE_SIZE, (self.scrollX // TILE_SIZE) + (self.width // TILE_SIZE)):
                self.renderTexture.blit(self.textures[self.tileArray[i][k]], (x, y))
                x += TILE_SIZE

            y += TILE_SIZE
 
class Hotbar:
    def __init__(self, textures):
        self.width = RENDERWIDTH
        self.height = TILE_SIZE + 4
        self.renderTexture = pygame.Surface((self.width, self.height))
        self.textures = []
        for path in textures:
            self.textures.append(pygame.image.load(TEXTURE_PREFIX + path))
            
        self.selected = 0

    def updateTextures(self):
        self.renderTexture.fill((0, 0, 0))

        x = 2
        y = 2
        
        index = 0
        for tile in self.textures:
            if (index == self.selected):
                pygame.draw.rect(self.renderTexture, (255, 255, 255), (x - 2, 0, TILE_SIZE + 4, TILE_SIZE + 4))
            self.renderTexture.blit(tile, (x, y))

            x += TILE_SIZE + 4
            index += 1

def get_position():
    local = pygame.mouse.get_pos()
    renderX = int((local[0] / WIDTH) * RENDERWIDTH)
    renderY = int((local[1] / HEIGHT) * RENDERHEIGHT)
    
    index = -1

    if (renderY > (RENDERHEIGHT - (TILE_SIZE + 4))):
        index = renderX // (TILE_SIZE + 2)
    
    X = (renderX + tileMap.scrollX) // TILE_SIZE
    Y = (renderY + tileMap.scrollY) // TILE_SIZE

    return (X, Y, index + 1)


pygame.init()

title = "MAwio"
target_fps = 60
prev_time = time.time()

with open('map.txt', 'r') as fileR:
    tileMapArray = eval(fileR.readline())
#tileMapArray = [[int(TextureIds.TECH_METAL_BORDER)]*400 for i in range(400)]

tileMap = TileMap(tileMapArray, TEXTURE_NAMES)
hotbar = Hotbar(TEXTURE_NAMES)

screenTarget = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((RENDERWIDTH, RENDERHEIGHT))
 
hotbar.updateTextures()
tileMap.updateTexture(0, 0)

while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            with open('map.txt', 'w') as fileW:
                fileW.write(str(tileMapArray))

            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYUP or event.type == pygame.KEYDOWN):
            velocity = [0, 0]
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                velocity[0] += TILE_SIZE
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                velocity[0] -= TILE_SIZE
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                velocity[1] += TILE_SIZE
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                velocity[1] -= TILE_SIZE
            tileMap.updateTexture(velocity[0], velocity[1])
            pass

    if (pygame.mouse.get_pressed()[0] == True):
        local = get_position()

        if (local[2] > 0):
            hotbar.selected = local[2] - 1 if local[2] - 1 < len(hotbar.textures) else hotbar.selected
            hotbar.updateTextures()
        else:
            tileMapArray[local[1]][local[0]] = hotbar.selected
            tileMap.updateTexture(0, 0)

    screen.blit(tileMap.renderTexture, (0, 0));
    screen.blit(hotbar.renderTexture, (0, RENDERHEIGHT - (TILE_SIZE + 4)));

    screenTarget.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0,0))
        
    pygame.display.flip()

    #Timing code at the END!
    curr_time = time.time()#so now we have time after processing
    diff = curr_time - prev_time#frame took this much time to process and render
    delay = max(1.0/target_fps - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
    time.sleep(delay)
    fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
    prev_time = curr_time
    pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))


    

