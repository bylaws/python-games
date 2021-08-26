import pygame, sys, random, math
from enum import IntEnum
import time
objects = {}

WIDTH = int(1280 * 1)
HEIGHT = int(1024 * 1)

TILE_SIZE = 16
TILE_COLLISION_ACCURACY = round(TILE_SIZE / 4)

RENDERWIDTH = TILE_SIZE * 20
RENDERHEIGHT = TILE_SIZE * 16

TEXTURE_PREFIX = "textures/"
TEXTURE_NAMES = ["tilegrass.png", "tilestone.png", "tileflower.png", "tilestone.png", "tilestump.png", "tiletechmetalborders.png", "tiletechmetal.png", "tiletechmetalbarrel.png"]
TILE_SOLID = [False, False, False, False, False, True, False, True]

BULLET_SPEED = 2
BULLET_IMAGE = ["bullet.png"]

PLAYER_ANIM_STAGES = 2
PLAYER_ANIM_FREQ = 4

TITLE = "TANK MEGA"
TARGET_FPS = 60

ENEMY_SPEED = 2
ENEMY_HEALTH = 60

bulletCount = 0

class TextureIds(IntEnum):
    GRASS = 0,
    ROCK = 1,
    FLOWER = 2,
    STONE = 3,
    STUMP = 4,
    TECH_METAL_BORDER = 5,
    TECH_METAL = 6,
    TECH_METAL_BARREL = 7

class ObjectIds(IntEnum):
    PLAYER = 0,
    PLAYER_GUN = 1,
    BULLET_START = 50,
    BULLET_END = 10000,
    ENEMY_START = 20000

class Directions(IntEnum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3

class TileMap:
    def __init__(self, array, textures):
        self.width = RENDERWIDTH + TILE_SIZE
        self.height = RENDERHEIGHT + TILE_SIZE
        self.renderTexture = pygame.Surface((self.width, self.height))
        self.textures = []
        for path in textures:
            self.textures.append(pygame.image.load(TEXTURE_PREFIX + path))

        self.tileArray = array

    def updateTexture(self):
        playerPos = objects[ObjectIds.PLAYER].getWorldPixelPos()

        y = 0
        scrollX = playerPos[0] + objects[ObjectIds.PLAYER].playerOffsetX
        scrollY = playerPos[1] + objects[ObjectIds.PLAYER].playerOffsetY
        print(playerPos[0], objects[ObjectIds.PLAYER].playerOffsetX)
        for i in range(scrollY // TILE_SIZE, (scrollY // TILE_SIZE) + (self.height // TILE_SIZE)):
            x = 0
            for k in range(scrollX // TILE_SIZE, (scrollX // TILE_SIZE) + (self.width // TILE_SIZE)):
                self.renderTexture.blit(self.textures[self.tileArray[i][k]], (x, y))
                x += TILE_SIZE

            y += TILE_SIZE

class GameObject:
    def isStatic(self):
        return self.static

    def setVisible(self, visible):
        self.visible = visible

    def getVelocityX(self):
        return self.velocity[0]

    def getVelocityY(self):
        return self.velocity[1]

    def getVelocity(self):
        return self.velocity

    def getPosition(self):
        return (self.rects[self.imageId].x, self.rects[self.imageId].y)

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setPosition(self, x, y):
        for i in range(len(self.rects)):
            self.rects[i].x = x
            self.rects[i].y = y

    def getRect(self):
        return self.rects[self.imageId]

    def eventHandler(self, event):
        pass

    def move(self, x = True, y = True):
        xVel = self.velocity[0] if x else 0
        yVel = self.velocity[1] if y else 0

        for i in range(len(self.rects)):
            self.rects[i] = self.rects[i].move(xVel, yVel)

    def fakeMove(self, x = True, y = True):
        xVel = self.velocity[0] if x else 0
        yVel = self.velocity[1] if y else 0

        return (self.getPosition()[0] + xVel, self.getPosition()[1] + yVel)

    def draw(self, screen):
        if (self.visible):
            rotatedImg = pygame.transform.rotate(self.images[self.imageId], self.angle)
            rotatedRect = rotatedImg.get_rect(center = self.rects[self.imageId].center)
            screen.blit(rotatedImg, rotatedRect)
        return screen

    def frameHandler(self):
        pass

    def __init__(self, image_paths, visible = False, x = 0, y = 0, static = False):
        self.visible = visible
        self.static = static
        self.velocity = [0, 0]
        self.rects = []
        self.images = []

        self.angle = 0

        for path in image_paths:
            self.images.append(pygame.image.load(TEXTURE_PREFIX + path))
            self.rects.append(pygame.image.load(TEXTURE_PREFIX + path).get_rect())

        self.imageId = 0
        self.setPosition(x, y)


class ScrollingObject(GameObject):
    def __init__(self, image_paths, visible = False, x = 0, y = 0, static = False):
        self.worldX = x
        self.worldY = y

        super().__init__(image_paths, visible, x, y, static)

    def move(self):
        playerPos = objects[ObjectIds.PLAYER].getWorldPixelPos()

        y = 0
        scrollX = playerPos[0] + objects[ObjectIds.PLAYER].playerOffsetX
        scrollY = playerPos[1] + objects[ObjectIds.PLAYER].playerOffsetY

        self.setPosition(self.worldX - scrollX, self.worldY - scrollY)

        
class EnemyObject(ScrollingObject):
    def __init__(self, image_paths, visible = False, x = 0, y = 0, static = False):
        self.health = ENEMY_HEALTH
        super().__init__(image_paths, visible, x, y, static)

        self.fancyX = self.worldX
        self.fancyY = self.worldY

    def processBullet(self, x, y):
        if (x > self.worldX and x < self.worldX + self.getRect().width and y > self.worldY and y < self.worldY + self.getRect().height):
            self.health -= 6

        if (self.health < 0):
            self.visible = False
    
    def frameHandler(self):
        global frameCounter

        playerPos = objects[ObjectIds.PLAYER].getWorldPixelRealPos()
        relativeX = playerPos[0] - self.worldX
        relativeY = playerPos[1] - self.worldY
        self.angle = -math.degrees(math.atan2(relativeY, relativeX))
        self.velocity = [math.cos(math.radians(self.angle)) * ENEMY_SPEED, (-math.sin(math.radians(self.angle))) * ENEMY_SPEED]
        self.velocity[0] += random.randint(-2, 2)
        self.velocity[1] += random.randint(-2, 2)


#        if(relativeX < self.getRect().width / 2 and relativeY < self.getRect().height):
#            print("AAAA")
        

    def move(self):
        oldValues = (self.fancyX, self.fancyY)

        self.fancyX += self.velocity[0]
        self.fancyY += self.velocity[1]
        
        self.worldX = int(self.fancyX)
        self.worldY = int(self.fancyY)

        if (self.touchingSolid((self.worldX, self.worldY))):
            self.fancyX = oldValues[0]
            self.fancyY = oldValues[1]

        super().move()

    def touchingSolid(self, position):
        lowerLeftX = position[0] + TILE_COLLISION_ACCURACY
        lowerLeftY = position[1] + self.getRect().height + TILE_COLLISION_ACCURACY
        upperLeftX = lowerLeftX
        upperLeftY = (lowerLeftY - TILE_COLLISION_ACCURACY * 2) + self.getRect().height

        lowerRightX = (lowerLeftX - TILE_COLLISION_ACCURACY * 2) + self.getRect().width
        lowerRightY = lowerLeftY
        upperRightX = (lowerRightX - TILE_COLLISION_ACCURACY * 2)
        upperRightY = upperLeftY

        points = [(lowerLeftX, lowerLeftY), (lowerRightX, lowerRightY), (upperLeftX, upperLeftY), (upperRightX, upperRightY)]

        for point in points:
            tileX = point[0] // TILE_SIZE
            tileY = point[1] // TILE_SIZE - 1

            if (TILE_SOLID[tileMapArray[tileY][tileX]]):
                return True

        return False



class BulletObject(GameObject):
    def __init__(self, x, y, worldX, worldY, velocity, angle, index):

        self.index = index

        super().__init__(BULLET_IMAGE, True, x, y, False)

        self.velocity = velocity * 10
        self.angle = angle

        self.fancyX = x
        self.fancyY = y
 
        self.worldX = worldX + x + self.getRect().width / 2
        self.worldY = worldY + y + self.getRect().height / 2
        
    def frameHandler(self):
        self.fancyX += self.velocity[0] * 3
        self.fancyY += self.velocity[1] * 3

        self.worldX += self.velocity[0] * 3
        self.worldY += self.velocity[1] * 3

        self.setPosition(self.fancyX, self.fancyY)

        enemies = []
        for key in objects:
            if (key >= int(ObjectIds.ENEMY_START)):
                enemies.append(key)

        for enemy in enemies:
            objects[enemy].processBullet(int(self.worldX), int(self.worldY))
        
        if (TILE_SOLID[tileMapArray[int(self.worldY) // TILE_SIZE][int(self.worldX) // TILE_SIZE]]):
            tileMapArray[int(self.worldY) // TILE_SIZE][int(self.worldX) // TILE_SIZE] = int(TextureIds.TECH_METAL)
            tileMap.updateTexture()
            objects.pop(self.index)

class GunObject(GameObject):
    def __init__(self, image_paths, visible = False, x = 0, y = 0, static = False):
        self.worldX = 200
        self.worldY = 200
        self.maxDeg = 360
        self.minDeg = 0
        
        self.special = False

        super().__init__(image_paths, visible, x, y, static)

    def setFOV(self, fov, direction):
        self.special = False

        rotationAngle = 0
        if (direction == Directions.UP):
            rotationAngle = -90
        elif (direction == Directions.RIGHT):
            rotationAngle = 0
        elif (direction == Directions.DOWN):
            rotationAngle = 90
        elif (direction == Directions.LEFT):
            self.minDeg = -180 + fov / 2
            self.maxDeg = 180 - fov / 2
            self.special = True

            return

        self.minDeg = rotationAngle - fov / 2
        self.maxDeg = rotationAngle + fov / 2

    def pointTowards(self, x, y):
        relativeX = x - (self.worldX + self.getPosition()[0] + self.getRect().width / 2)
        relativeY = y - (self.worldY + self.getPosition()[1] + self.getRect().height / 2)

        self.angle = math.degrees(math.atan2(relativeY, relativeX)) 




        self.angle = -self.angle
        bulletVelocity = [math.cos(math.radians(self.angle)) * 100 + self.getPosition()[0] + self.getRect().width / 2, (-math.sin(math.radians(self.angle))) * 100 +  self.getPosition()[1] + self.getRect().height / 2]
        screen.set_at((int(bulletVelocity[0]), int(bulletVelocity[1])), (255, 255, 0))

    def fire(self):
        global bulletCount
        
        if (int(ObjectIds.BULLET_START) + bulletCount >= ObjectIds.BULLET_END):
            bulletCount = 0

        bsp = (random.randint(100, 200) / 100)
        bulletVelocity = [math.cos(math.radians(self.angle)) * bsp, (-math.sin(math.radians(self.angle))) * bsp] 
        objects[int(ObjectIds.BULLET_START) + bulletCount] = BulletObject(self.getPosition()[0] + self.getRect().width / 2, self.getPosition()[1] + self.getRect().height / 2, self.worldX, self.worldY, bulletVelocity, self.angle, ObjectIds.BULLET_START + bulletCount)
        
        bulletCount += 1

class PlayerOneObject(GameObject):
    def __init__(self, image_paths, visible = False, x = 0, y = 0, static = False):
        self.worldX = 200
        self.worldY = 200

        self.tileX = 0
        self.tileY = 0

        self.playerOffsetX = 0
        self.playerOffsetY = 0

        self.direction = Directions.UP
        self.moving = 0

        super().__init__(image_paths, visible, x, y, static)

    def move(self):
        oldValues = (self.worldX, self.worldY, self.playerOffsetX, self.playerOffsetY)

        self.worldX += self.velocity[0]
        self.worldY += self.velocity[1]

        self.playerOffsetX -= self.velocity[0]
        self.playerOffsetY -= self.velocity[1]

        changePosX = True
        changePosY = True

        if (self.playerOffsetX > TILE_SIZE * 3):
            self.worldX -= (self.playerOffsetX - (TILE_SIZE * 3))
            self.playerOffsetX = TILE_SIZE * 3
            changePosX = False
        elif (self.playerOffsetX < -TILE_SIZE * 3):
            self.worldX -= (self.playerOffsetX + (TILE_SIZE * 3))
            self.playerOffsetX = -TILE_SIZE * 3
            changePosX = False


        if (self.playerOffsetY > TILE_SIZE * 3):
            self.worldY -= (self.playerOffsetY - (TILE_SIZE * 3))
            self.playerOffsetY = TILE_SIZE * 3
            changePosY = False
        elif (self.playerOffsetY < -TILE_SIZE * 3):
            self.worldY -= (self.playerOffsetY + (TILE_SIZE * 3))
            self.playerOffsetY = -TILE_SIZE * 3
            changePosY = False


        if (self.touchingSolid(self.fakeMove(changePosX, changePosY))):
            self.worldX = oldValues[0]
            self.worldY = oldValues[1]
            self.playerOffsetX = oldValues[2]
            self.playerOffsetY = oldValues[3]
            return

        super().move(changePosX, changePosY)

        if (self.worldX // TILE_SIZE != self.tileX and not changePosX):
            self.tileX = self.worldX // TILE_SIZE
            tileMap.updateTexture()
        if (self.worldY // TILE_SIZE != self.tileY and not changePosY):
            self.tileY = self.worldY // TILE_SIZE
            tileMap.updateTexture()

    def eventHandler(self, event):
        POSA = 3
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            self.velocity[0] += POSA
            self.direction = Directions.RIGHT
            self.moving += POSA
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
            self.velocity[0] -= POSA
            self.direction = Directions.LEFT
            self.moving += POSA
        elif (event.type == pygame.KEYUP and event.key == pygame.K_LEFT):
            self.velocity[0] += POSA
            self.moving -= POSA
        elif (event.type == pygame.KEYUP and event.key == pygame.K_RIGHT):
            self.velocity[0] -= POSA
            self.moving -= POSA
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
            self.velocity[1] += POSA
            self.direction = Directions.DOWN
            self.moving += POSA
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
            self.velocity[1] -= POSA
            self.direction = Directions.UP
            self.moving += POSA
        elif (event.type == pygame.KEYUP and event.key == pygame.K_UP):
            self.velocity[1] += POSA
            self.moving -= POSA
        elif (event.type == pygame.KEYUP and event.key == pygame.K_DOWN):
            self.velocity[1] -= POSA
            self.moving -= POSA
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            pygame.event.set_grab(True)
            for i in range(5):
                objects[ObjectIds.PLAYER_GUN].fire()


        
        self.imageId = PLAYER_ANIM_STAGES * self.direction
        
        objects[ObjectIds.PLAYER_GUN].setFOV(90, self.direction)

    def inView(self, x, y):
        if (x > (self.worldX + self.playerOffsetX) and x < (self.worldX + self.playerOffsetX + RENDERWIDTH) and y < (self.worldY + self.playerOffsetY) and y < (self.worldY + self.playerOffsetY + RENDERHEIGHT)):
            return True

        return False

    def getWorldPixelPos(self):
        return (self.worldX, self.worldY)

    def getWorldPos(self):
        return (
            round((self.worldX + (self.getPosition()[0] + self.getRect().width / 2) + self.playerOffsetX) / TILE_SIZE),
            round((self.worldY + (self.getPosition()[1] + self.getRect().height / 2) + self.playerOffsetY) / TILE_SIZE))
    
    def getWorldPixelRealPos(self):
        return (
            (self.worldX + (self.getPosition()[0] + self.getRect().width / 2) + self.playerOffsetX),
            (self.worldY + (self.getPosition()[1] + self.getRect().height / 2) + self.playerOffsetY))


    def touchingSolid(self, position):
        lowerLeftX = self.worldX + position[0] + self.playerOffsetX + TILE_COLLISION_ACCURACY
        lowerLeftY = self.worldY + position[1] + self.getRect().height + self.playerOffsetY + TILE_COLLISION_ACCURACY
        upperLeftX = lowerLeftX
        upperLeftY = (lowerLeftY - TILE_COLLISION_ACCURACY * 2) + self.getRect().height

        lowerRightX = (lowerLeftX - TILE_COLLISION_ACCURACY * 2) + self.getRect().width
        lowerRightY = lowerLeftY
        upperRightX = (lowerRightX - TILE_COLLISION_ACCURACY * 2)
        upperRightY = upperLeftY

        points = [(lowerLeftX, lowerLeftY), (lowerRightX, lowerRightY), (upperLeftX, upperLeftY), (upperRightX, upperRightY)]

        for point in points:
            tileX = point[0] // TILE_SIZE
            tileY = point[1] // TILE_SIZE - 1

            if (TILE_SOLID[tileMapArray[tileY][tileX]]):
                return True

        return False

    def frameHandler(self):
        global frameCounter
        if ((frameCounter % int(TARGET_FPS // PLAYER_ANIM_FREQ)) == 0 and self.moving):
            self.imageId -= ((self.imageId % PLAYER_ANIM_STAGES) * 2) - 1

        local = pygame.mouse.get_pos()
        renderX = int((local[0] / WIDTH) * RENDERWIDTH)
        renderY = int((local[1] / HEIGHT) * RENDERHEIGHT)



        objects[ObjectIds.PLAYER_GUN].worldX = self.worldX + self.playerOffsetX
        objects[ObjectIds.PLAYER_GUN].worldY = self.worldY + self.playerOffsetY
        objects[ObjectIds.PLAYER_GUN].setPosition(self.getPosition()[0], self.getPosition()[1])
        objects[ObjectIds.PLAYER_GUN].pointTowards(self.worldX + self.playerOffsetX + renderX, self.worldY +  self.playerOffsetY + renderY)

def moveKeyHandler(event, velocity):
    if (event.type == pygame.QUIT):
        sys.exit()

    return velocity

def loadGameObjects():
    for objInfo in ObjectSpawnInfo:
        tmp = objInfo[0](objInfo[2], objInfo[3], objInfo[4], objInfo[5], objInfo[6])
        objects[int(objInfo[1])] = tmp

def makeFreeList():
    x = 0
    y = 0
    out = []
    for row in tileMapArray:
        for col in row:
            if (not TILE_SOLID[col]):
                out.append([x*16, y*16])
            y += 1
        y = 0
        x += 1
    
    print(out)
    return out


def main():
    global screen
    global frameCounter
    pygame.init()
    pygame.mouse.set_visible(False)
    
    loadGameObjects()
    tileMap.updateTexture()

    screenTarget = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.Surface((RENDERWIDTH, RENDERHEIGHT))

    prev_time = time.time()
    
    enemyCount = 0
    freeTileList = makeFreeList()

    if (frameCounter == 7):
        print("hello")



    while True:
        if (frameCounter % 60 == 0):
            randomIndex = random.randint(0, len(freeTileList)-1)
            objects[ObjectIds.ENEMY_START + enemyCount] = EnemyObject(["gun.png"], True, freeTileList[randomIndex][1], freeTileList[randomIndex][0], False)
            enemyCount += 1
        tmpObj = []
        for obj in objects:
            tmpObj.append(objects[obj])

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.event.set_grab(False)

            for obj in tmpObj:
                obj.eventHandler(event)

        playerPos = objects[ObjectIds.PLAYER].getWorldPixelPos()
        screen.blit(tileMap.renderTexture.subsurface(
            (playerPos[0] + objects[ObjectIds.PLAYER].playerOffsetX) % TILE_SIZE,
            (playerPos[1] + objects[ObjectIds.PLAYER].playerOffsetY) % TILE_SIZE,
            RENDERWIDTH, RENDERHEIGHT), (0,0))

        for obj in tmpObj:
            obj.frameHandler()
            obj.move()
            screen = obj.draw(screen)

        screenTarget.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0,0))

        pygame.display.flip()


        frameCounter += 1
        frameCounter %= TARGET_FPS

        #Timing code at the END!
        curr_time = time.time()#so now we have time after processing
        diff = curr_time - prev_time#frame took this much time to process and render
        delay = max(1.0/TARGET_FPS - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
        time.sleep(delay)
        fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
        prev_time = curr_time
        pygame.display.set_caption("{0}: {1:.2f}".format(TITLE, fps))

ObjectSpawnInfo = [
#    Class               ObjectID               Sprite Image Paths    Visible X                Y                  Static
    [PlayerOneObject,    ObjectIds.PLAYER,      ["mawioup0.png", "mawioup1.png", "mawiodown0.png", "mawiodown1.png", "mawioleft0.png", "mawioleft1.png", "mawioright0.png", "mawioright1.png"],         True,   RENDERWIDTH/2-8, RENDERHEIGHT/2-16, False],
    [GunObject,          ObjectIds.PLAYER_GUN,  ["gun.png"],          True,   RENDERWIDTH/2-8, RENDERHEIGHT/2-16, False],
]

with open('map.txt', 'r') as fileR:
    tileMapArray = eval(fileR.readline())

frameCounter = 0
tileMap = TileMap(tileMapArray, TEXTURE_NAMES)

main()
