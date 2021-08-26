# POwder POlitics

import pygame, time, sys, random, numpy, cProfile, copy, pickle, os
from numba import jit

import math
from pygame.math import Vector2
WIDTH = int(1280 * 1)
HEIGHT = int(1024 * 1)

TILE_SIZE = 16
TITLE="PoPo"

disprint = print
# Comment to enable loggin
def disprint(*args, **kwargs):
    pass

RENDERWIDTH = 255 + 32
RENDERHEIGHT = TILE_SIZE * 18 - 1

TARGET_FPS = 600
PARTICLE_AREA = Vector2(255, 255) # Map dimensions
PARTICLE_FACE_AREA = 1
GRAVITY = Vector2(0, 0.1)
FONT = 0
EXPLOSION_STRENGTH = 15
EXPLOSION_RADIUS = 9
EXPLOSION_ACTIVATION_RADIUS = 1
EXPLOSION_HEAT = 70
COLD_WALL_STRENGTH = 5
AIR_DENSITY_DEF = 1.0

@jit(nopython=True)
def doParticleCalcsQuick(velocityY, dragCoeff, airDensity, gravityY, velocityX, positionX, positionY):
    drag = ((velocityY * velocityY) / 2) * dragCoeff * airDensity * PARTICLE_FACE_AREA

    if (velocityY > 0):
        drag = -(velocityY / 4)

    accelerationY = -(gravityY - drag)
    accelerationX = 0
    if (velocityX < 0):
        accelerationX = (velocityX * velocityX) * 0.1 * dragCoeff
    else:
        accelerationX = (velocityX * velocityX) * 0.1 * -dragCoeff
    
    if ((((accelerationX + velocityX) > 0) and (velocityX <= 0)) or (((accelerationX + velocityX) < 0) and (velocityX >= 0))):
        velocityX = 0
        accelerationX = 0

    velocityX += accelerationX
    velocityY += accelerationY

    if (velocityY > 7):
        velocityY = 7
    
    positionX += velocityX
    positionY += velocityY

    return positionX, positionY, velocityX, velocityY

def setWorld(worldArray, position, value):
    try:
        worldArray[int(position.x)][len(worldArray) - int(position.y) - 1] = value
    except:
        pass


def setWorldRad(worldArray, position, value, radius):
    radius -= 1


    try:
        if (radius == 0):
            if (issubclass(type(value), Particle)):
                worldArray[int(position.x)][len(worldArray) - int(position.y) - 1] = copy.deepcopy(value)
            else:
                worldArray[int(position.x)][len(worldArray) - int(position.y) - 1] = value

            return

        for x in range(-radius, radius, 1):
            for y in range(-radius, radius, 1):
                if (issubclass(type(value), Particle)):
                    p = copy.deepcopy(value)
                    p.position.x += x
                    p.position.y += y

                    worldArray[int(position.x) + x][len(worldArray) - int(position.y) - 1 - y] = p
                else:
                    worldArray[int(position.x) + x][len(worldArray) - int(position.y) - 1 - y] = value
    except:
        pass


def setWorldVelRad(worldArray, position, velocity, radius):
    radius -= 1


    try:
        if (radius == 0):
            if (issubclass(type(worldArray[int(position.x)][len(worldArray) - int(position.y) - 1]), Particle)):
                worldArray[int(position.x)][len(worldArray) - int(position.y) - 1].velocity = velocity

            return

        for x in range(-radius, radius, 1):
            for y in range(-radius, radius, 1):
                if (issubclass(type(worldArray[int(position.x + x)][len(worldArray) - int(position.y) - y - 1]), Particle)):
                    worldArray[int(position.x + x)][len(worldArray) - int(position.y) - y - 1].velocity = velocity

    except:
        pass
def getWorld(worldArray, position):
    try:
        return worldArray[int(position.x)][len(worldArray) - int(position.y) - 1]
    except:
        pass

class BorderReflection:
    pass

class BorderVoid:
    pass

class BorderSolid:
    pass
class Configuration:
    def __init__(self, tool, particle, toolSize, borderTop, borderSides):
        self.tool = tool
        self.particle = particle
        self.toolSize = toolSize
        self.borderTop = borderTop
        self.borderSides = borderSides

class DataHolder:
    def __init__(self, initial):
        self.data = initial
        self.owners = []

    def write(self, data):
        self.data = data

    def read(self):
        return self.data


class Window:
    def __init__(self, position, extent, config):
        self.extent = extent
        self.position = position
        self.config = config
        self.renderTexture = pygame.Surface(extent)
        disprint(extent, position)

    def draw(self):
        pass;

    
class Padding:
    def __init__(self, padding):
        self.padding = padding

class Tile:
    def __init__(self, extent, padding, image):
        self.extent = extent
        self.padding = padding
        self.image = image
        self.textureNormal = pygame.Surface(extent)
        self.textureNormal.fill((0,0,0))
        self.makeVariants()
        self.clicked = False

    def makeVariants(self):
        self.textureHighlight = self.textureNormal.copy()
        self.textureHighlight.fill((100, 100, 100, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def action(self):
        print("action!")

    def mouse(self, enable):
        action = False

        if (self.clicked and not enable):
            action = True

        self.clicked = enable

        if (action):
            self.action()

        return action

        return False

class TileTogglable(Tile):
    def __init__(self, extent, padding, image, state = False):
        super().__init__(extent, padding, image)

        self.state = state
        self.draw()


    def draw(self):
        size = 8
        width = 1

        self.textureNormal.fill((0, 0, 0))
        self.textureNormal.blit(self.image, (self.padding.x * 8, self.extent.y / 2 - self.image.get_height() / 2))

        if (self.state):
            pygame.draw.rect(self.textureNormal, (255, 255, 255), (int(self.extent.x - self.padding.x - size), int(self.extent.y / 2 - size / 2), size, size))
        else:
            pygame.draw.rect(self.textureNormal, (255, 255, 255), (int(self.extent.x - self.padding.x - size), int(self.extent.y / 2 - size / 2), size, size), width = width)

        self.makeVariants()


    def action(self):
        self.state = not self.state
        self.draw()
        self.makeVariants()

class TileTogglableGrouped(Tile):
    def __init__(self, extent, padding, image, dataHolder, myActiveData, state = False):
        super().__init__(extent, padding, image)

        self.myActiveData = myActiveData
        self.dataHolder = dataHolder

        if (state):
            self.action()
        else:
            self.state = False
            self.draw()

        self.dataHolder.owners.append(self)


    def draw(self):
        radius = 4
        width = 1

        self.textureNormal.fill((0, 0, 0))
        self.textureNormal.blit(self.image, (self.padding.x * 8, self.extent.y / 2 - self.image.get_height() / 2))


        if (self.state):
            pygame.draw.circle(self.textureNormal, (255, 255, 255), (int(self.extent.x - self.padding.x - radius), int(self.extent.y / 2)), radius)
        else:
            pygame.draw.circle(self.textureNormal, (255, 255, 255), (int(self.extent.x - self.padding.x - radius), int(self.extent.y / 2)), radius, width = width)

        self.makeVariants()

    def unselect(self):
        self.state = False
        self.draw()

    def select(self):
        self.state = True
        self.draw()
        self.dataHolder.write(self.myActiveData)

    def action(self):
        for tile in self.dataHolder.owners:
            if (tile != self):
                tile.unselect()

        self.select()

class ControlWindow(Window):
    def __init__(self, position, extent, config):
        super().__init__(position, extent, config)
        self.renderTexture.fill((50,255,50))
        
        self.tiles = []

        height = 20
        width = 30

        self.tiles.append(Padding(Vector2(32, height)))
        self.tiles.append(TileTogglableGrouped(Vector2(width, height), Vector2(1, 3), pygame.image.load("void_top.png"), self.config.borderTop, BorderVoid, state = True))
        self.tiles.append(TileTogglableGrouped(Vector2(width, height), Vector2(1, 3), pygame.image.load("solid_top.png"), self.config.borderTop, BorderSolid))
        self.tiles.append(Padding(Vector2(32, height)))
        self.tiles.append(TileTogglableGrouped(Vector2(width, height), Vector2(1, 3), pygame.image.load("reflect_sides.png"), self.config.borderSides, BorderReflection, state = True))
        self.tiles.append(TileTogglableGrouped(Vector2(width, height), Vector2(1, 3), pygame.image.load("void_sides.png"), self.config.borderSides, BorderVoid))

    def draw(self):
        pos = list(pygame.mouse.get_pos())
        pos[0] /= WIDTH
        pos[0] *= RENDERWIDTH
        pos[1] /= HEIGHT
        pos[1] *= RENDERHEIGHT
        pos[0] -= self.position[0]
        pos[1] -= self.position[1]
        mousePos = Vector2(pos[0], pos[1])

        
        progX = 0
        for tile in self.tiles:
            if (isinstance(tile, Padding)):
                progX += tile.padding.x
                continue;
            progX += tile.padding.x

            # if occuluded by mouse
            texture = tile.textureNormal
            if (mousePos.x >= progX and mousePos.x < progX + tile.extent.x and mousePos.y >= tile.padding.y and mousePos.y < tile.extent.y + tile.padding.y):
                texture = tile.textureHighlight

                if (pygame.mouse.get_pressed()[0]):
                    tile.mouse(True)
                else:
                    tile.mouse(False)


            self.renderTexture.blit(texture, (progX, tile.padding.y))
            progX += tile.extent.x
            progX += tile.padding.x

       
class StatsWindow(Window):
    def __init__(self, position, extent, config):
        super().__init__(position, extent, config)
        self.renderTexture.fill((50,255,50))
        
        self.tiles = []

        height = 11

        self.tiles.append(Padding(Vector2(32, 2)))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("point.png"), self.config.tool, PointTool, state = True))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("force.png"), self.config.tool, ForceTool))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("line.png"), self.config.tool, LineTool))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("temp.png"), self.config.tool, TempTool))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("spark.png"), self.config.tool, SparkTool))

        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("spark.png"), self.config.tool, CopiPeTool))
        self.tiles.append(Padding(Vector2(32, 5)))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("dust.png"), self.config.particle, DustParticle, state = True))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("water.png"), self.config.particle, WaterParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("wall.png"), self.config.particle, WallParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("heavy.png"), self.config.particle, HeavyParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("forcefield.png"), self.config.particle, C4Particle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("cooler.png"), self.config.particle, CoolerWallParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("heater.png"), self.config.particle, HeaterWallParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("wire.png"), self.config.particle, WireParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("wire.png"), self.config.particle, InstWireParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("not.png"), self.config.particle, NotGateParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("xor.png"), self.config.particle, XorGateParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("and.png"), self.config.particle, AndGateParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("or.png"), self.config.particle, OrGateParticle))
        self.tiles.append(TileTogglableGrouped(Vector2(30, height), Vector2(1, 1), pygame.image.load("or.png"), self.config.particle, JunctionParticle))
        
    def draw(self):
        pos = list(pygame.mouse.get_pos())
        pos[0] /= WIDTH
        pos[0] *= RENDERWIDTH
        pos[1] /= HEIGHT
        pos[1] *= RENDERHEIGHT
        mousePos = Vector2(pos[0], pos[1])

        
        progY = 0
        for tile in self.tiles:
            if (isinstance(tile, Padding)):
                progY += tile.padding.y
                continue;
            progY += tile.padding.y

            # if occuluded by mouse
            texture = tile.textureNormal
            if (mousePos.y >= progY and mousePos.y < progY + tile.extent.y and mousePos.x >= tile.padding.x and mousePos.x < tile.extent.x + tile.padding.x):
                texture = tile.textureHighlight

                if (pygame.mouse.get_pressed()[0]):
                    tile.mouse(True)
                else:
                    tile.mouse(False)


            self.renderTexture.blit(texture, (tile.padding.x, progY))
            progY += tile.extent.y
            progY += tile.padding.y



class Tool:
    def __init__(self, worldArray, config):
        self.worldArray = worldArray
        self.config = config

    def handle(self, mousepos):
        pass

    def update(self):
        pass

    def draw(self, renderArray, mousePos):
        pass

    def deselect(self):
        pass

class PointTool(Tool):
    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

        self.addingType = None
        self.addingColour = 0xffffff
        
    def draw(self, renderArray, mousePos):
        if (self.addingType != self.config.particle.read()):
            self.addingType = self.config.particle.read()
            self.addingColour = self.addingType(Vector2(0, 0), Vector2(0, 0), 0).colour

        if (mousePos.x < 0 or mousePos.y < 0):
            return

        if (mousePos.x > 255 or mousePos.y > 255):
            return  
        setWorldRad(renderArray, mousePos, self.addingColour, self.config.toolSize)
        
    def handle(self, mousePos):
        if (self.addingType != self.config.particle.read()):
            self.addingType = self.config.particle.read()
            self.addingColour = self.addingType(Vector2(0, 0), Vector2(0, 0), 0).colour

        if (pygame.mouse.get_pressed()[0]):
            setWorldRad(self.worldArray, mousePos, self.config.particle.read()(Vector2(mousePos), Vector2(0, 0), AIR_DENSITY_DEF), self.config.toolSize)
        elif (pygame.mouse.get_pressed()[2]):
            setWorldRad(self.worldArray, mousePos, 0, self.config.toolSize)
        

class TempTool(Tool):
    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

    def handle(self, mousePos):
        piece = getWorld(self.worldArray, mousePos)
        if (not piece):
            return

        try:
            if (pygame.mouse.get_pressed()[0]):
                piece.temp += abs(piece.temp) * 0.4 + 1 * 2**self.config.toolSize
            elif (pygame.mouse.get_pressed()[2]):
                piece.temp -= abs(piece.temp) * 0.4 - 1 * 2**self.config.toolSize
        except:
            pass
        

class SparkTool(Tool):
    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

    def handle(self, mousePos):
        piece = getWorld(self.worldArray, mousePos)
        if (not piece):
            return

        try:
            if (pygame.mouse.get_pressed()[0]):
                piece.setCharge(Vector2(0,0), self.worldArray, expire = 2)

            if (pygame.mouse.get_pressed()[1]):
                piece.setCharge(Vector2(0,0), self.worldArray)

            if (pygame.mouse.get_pressed()[2]):
                piece.setCharge(Vector2(0,0), self.worldArray, disable = True)
        except:
            pass
        
def drawLine(renderArray, start, end, value, radius, valueCallback = None, modifyCallback = setWorldRad):
    if (start == end):
        return;

    lineEndPos = end

    lineStartPos = None
    if (lineEndPos.y < start.y):
        lineStartPos = lineEndPos
        lineEndPos = start
    else:
        lineStartPos = start


    yLen = lineEndPos.y - lineStartPos.y
    xLen = lineEndPos.x - lineStartPos.x
    
    if (abs(xLen) >= abs(yLen)):
        coeff = -(yLen/xLen)

        if (lineEndPos.x < lineStartPos.x):
            for i in range(int(lineStartPos.x), int(lineEndPos.x), -1):
                pos = Vector2(i, coeff * (lineEndPos.x - i) + lineEndPos.y)
                if (valueCallback != None):
                    value = valueCallback(pos)
                modifyCallback(renderArray, pos, value, radius)
        if (lineEndPos.x > lineStartPos.x):
            for i in range(int(lineStartPos.x), int(lineEndPos.x), 1):
                pos = Vector2(i, coeff * (lineStartPos.x - i) + lineStartPos.y)
                if (valueCallback != None):
                    value = valueCallback(pos)
                modifyCallback(renderArray, pos, value, radius)
    elif (abs(xLen) < abs(yLen)):
        coeff = (xLen/yLen)

        for i in range(int(lineStartPos.y), int(lineEndPos.y), 1):
            pos = Vector2(lineStartPos.x + coeff * (i - lineStartPos.y), i)
            if (valueCallback != None):
                value = valueCallback(pos)
            modifyCallback(renderArray, pos, value, radius)


class LineTool(Tool):
    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

        self.adding = False
        self.start = Vector2(0, 0)
        # we do walls fancily here and make them actually affect the particles in the world
        self.addingType = None
        self.addingColour = 0
        self.pastValid = False
        self.pastPos = Vector2(0, 0)
        self.pastToolSize = 0

    def handle(self, mousePos):
        if (pygame.mouse.get_pressed()[0] and self.adding):
            if (self.addingType == WallParticle):
                if (self.pastValid and self.pastPos != self.start and self.pastPos != mousePos):
                    drawLine(self.worldArray, self.start, self.pastPos, 0, self.pastToolSize)
                    drawLine(self.worldArray, self.start, mousePos, Vector2(1,1), self.config.toolSize, modifyCallback = setWorldVelRad)


                if (mousePos != self.start):
                    self.pastPos = mousePos
                    self.pastToolSize = self.config.toolSize
                    self.pastValid = True

        if (pygame.mouse.get_pressed()[0] and not self.adding):
            self.start = mousePos
            self.addingType = self.config.particle.read()
            self.addingColour = self.addingType(Vector2(0, 0), Vector2(0, 0), 0).colour
            self.adding = True
        elif (not pygame.mouse.get_pressed()[0] and self.adding):
            self.pastValid = False
            self.pastPos = Vector2(0, 0)
            self.adding = False

            drawLine(self.worldArray, self.start, mousePos, None, self.config.toolSize, valueCallback = lambda pos : self.addingType(pos, Vector2(0, 0), AIR_DENSITY_DEF))

    def draw(self, renderArray, mousePos):
        if (self.adding):
            drawLine(renderArray, self.start, mousePos, self.addingColour, self.config.toolSize)

    def deselect(self):
        self.pastValid = False
        self.pastPos = Vector2(0, 0)
        self.adding = False

class ForceTool(Tool):
    class Force:
        def __init__(self, origin, direction, particle, size):
            self.origin = origin
            self.direction = direction 
            self.particle = particle
            self.size = size

    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

        self.adding = False
        self.start = Vector2(0, 0)
        self.forces = []

    def handle(self, mousePos):
        if (pygame.mouse.get_pressed()[0] and not self.adding):
            self.start = mousePos
            self.adding = True
        elif (not pygame.mouse.get_pressed()[0] and self.adding):
            end = mousePos

            relVector = self.start - end
            relVector.x = -relVector.x
            relVector.y = -relVector.y

            self.forces.append(self.Force(self.start, relVector, self.config.particle.read(), self.config.toolSize))
            self.adding = False

    def update(self):
        for force in self.forces:
            setWorldRad(self.worldArray, Vector2(force.origin), force.particle(Vector2(force.origin), Vector2(force.direction), AIR_DENSITY_DEF), force.size)

    def draw(self, renderArray, mousePos):
        if (self.adding):
            setWorld(renderArray, self.start, 0xFFFFFF)
            setWorld(renderArray, mousePos, 0xAAAAAA)

    def deselect(self):
        self.adding = False


class CopiPeTool(Tool):
    class Force:
        def __init__(self, origin, direction, particle, size):
            self.origin = origin
            self.direction = direction 
            self.particle = particle
            self.size = size

    def __init__(self, worldArray, config):
        super().__init__(worldArray, config)

        self.adding = False
        self.start = Vector2(0, 0)
        self.pasting = False
        self.copi = None
        self.end = Vector2(0,0)
        self.xSt = None
        self.xDist = None
        self.ySt = None
        self.yDist = None
        
        

    def handle(self, mousePos):
        if (pygame.mouse.get_pressed()[0] and not self.adding and not self.pasting):
            self.start = mousePos
            self.adding = True
        elif (not pygame.mouse.get_pressed()[0] and self.adding and not self.pasting):
            end = mousePos

            self.xDist = self.start.x - end.x
            xDist =  abs(self.xDist)

            xSt = min(self.start.x, end.x)
            self.yDist = self.start.y - end.y
            yDist = abs(self.yDist)
            ySt = min(self.start.y, end.y)
            self.xSt = xSt
            self.ySt = ySt

            self.copi = numpy.empty(shape=(int(xDist),int(yDist)), dtype=object)

            print(xDist)
            print(yDist)

            for x in range(int(xDist)):
                for y in range(int(yDist)):
                    self.copi[x][y] = getWorld(self.worldArray, Vector2(xSt + x, ySt + y))
                            

            
            self.adding = False
            self.pasting = True
            self.end = end
        elif (pygame.mouse.get_pressed()[0] and self.pasting):
            for x in range(int(abs(self.xDist))):
                for y in range(int(abs(self.yDist))):
                    setWorld(self.worldArray, Vector2(mousePos.x - x, mousePos.y + y), copy.copy(self.copi[abs(int(self.xDist))-x-1][y]))
                    try:
                        getWorld(self.worldArray, Vector2(mousePos.x - x, mousePos.y + y)).position = Vector2(mousePos.x - x, mousePos.y + y)
                    except:
                        pass
                    
            print(self.copi)
            self.pasting = False


    def draw(self, renderArray, mousePos):
        if (self.adding):
            setWorld(renderArray, self.start, 0xFFFFFF)
            setWorld(renderArray, Vector2(self.start.x, mousePos.y), 0xFFFFFF)
            setWorld(renderArray, Vector2(mousePos.x, self.start.y), 0xFFFFFF)

            setWorld(renderArray, mousePos, 0xFFFFFF)

        if (self.pasting):
            setWorld(renderArray, mousePos, 0x00FF00)
            setWorld(renderArray, Vector2(mousePos.x + self.xDist, mousePos.y), 0x00FF00)
            setWorld(renderArray, Vector2(mousePos.x, mousePos.y + self.yDist), 0x00FF00)

            setWorld(renderArray, Vector2(mousePos.x + self.xDist, mousePos.y + self.yDist), 0x00FF00)

    def deselect(self):
        self.adding = False
        
class Particle:
    def __init__(self, position, velocity, mass, colour, airDensity, dragCoeff, static, liquid, invincible = False):
        self.velocity = Vector2(velocity.x, velocity.y)
        self.position = position
        self.mass = mass
        self.colour = colour
        self.airDensity = airDensity
        self.dragCoeff = dragCoeff
        self.static = static
        self.liquid = liquid
        self.weight = GRAVITY * self.mass
        self.collided = False
        self.invincible = invincible
        
    def tickCallback(self, worldArrayNew):
        pass
    
    def moveCallback(self, worldArrayNew):
        pass

    def electricalTickCallback(self, worldArrayNew):
        pass
    
    def process(self, worldArrayNew, config):
        self.collided = False

        if (self.static):
            self.collided = True
#            setWorld(worldArrayNew, self.position, self)
            self.tickCallback(worldArrayNew)
            return


        setWorld(worldArrayNew, self.position, 0)
        oldPosition = Vector2(self.position.x, self.position.y)

        self.position.x, self.position.y, self.velocity.x, self.velocity.y = doParticleCalcsQuick(self.velocity.y, self.dragCoeff, self.airDensity, GRAVITY.y, self.velocity.x, self.position.x, self.position.y)
        if (config.borderSides.read() == BorderReflection):
            self.position.x = self.position.x % (PARTICLE_AREA.x - 1)
        elif (config.borderSides.read() == BorderVoid and (self.position.x <= 0 or self.position.x >= 255)):
            return # delete - bye!!!

        if (config.borderTop.read() == BorderVoid and (self.position.y < 0 or self.position.y >= 255)):
            return # delete - bye!!
        elif (config.borderTop.read() == BorderSolid and (self.position.y <= 2 or self.position.y >= 255)):
            if (self.position.y <= 2):
                self.position.y = 3
            else:
                self.position.y = 254


        collision = getWorld(worldArrayNew, self.position)
        if (collision != None and (issubclass(type(collision), Particle))):
            disprint("Collision")
            
            if (isinstance(collision, WallParticle)):
                self.collided = True
            elif (isinstance(collision, CoolerWallParticle)):
                self.collided = True
            elif (isinstance(collision, HeaterWallParticle)):
                self.collided = True

            momentum = self.velocity * self.mass 
            momentumCollision = collision.velocity * collision.mass
            combinedMass = collision.mass + self.mass

            # Our new velocity for us and the particle we collided with
            velocitySharedNew = (momentum + momentumCollision) / combinedMass

            if (self.collided):
                disprint("Collision: Collided")
                velocitySharedNew = Vector2()

            if (self.airDensity == AIR_DENSITY_DEF and collision.airDensity > AIR_DENSITY_DEF):
                self.velocity.y +=  min(collision.velocity.y, 2) if collision.velocity.y > 0 else 0
            elif (self.airDensity != AIR_DENSITY_DEF):
                pass
            else:
                collision.velocity = velocitySharedNew
#                self.velocity = velocitySharedNew

            if (collision.mass < self.mass):
                oldPosition2 = collision.position
                collision.position = oldPosition
                setWorld(worldArrayNew, collision.position, collision)
                self.position = oldPosition2

                setWorld(worldArrayNew, self.position, self)
                self.moveCallback(worldArrayNew)

                return


            found = False

            if (self.velocity.y < 0):
                disprint("winner")
                for pos in (random.sample((pygame.Vector2(-1, -1), pygame.Vector2(1, -1)), 2)) if not self.liquid else random.sample((pygame.Vector2(-1, -1), pygame.Vector2(1, -1), pygame.Vector2(-1, 0), pygame.Vector2(1, 0)), 4):
                    disprint("winner2")
                    collision = getWorld(worldArrayNew, oldPosition + pos)
                    if (collision == None or not issubclass(type(collision), Particle)):
                        disprint("Found2")
                        self.position = oldPosition + pos
                        found = True
                        break
            elif (self.velocity.y > 0):
                for pos in (random.sample((pygame.Vector2(-1, 1), pygame.Vector2(1, 1)), 2)) if not self.liquid else random.sample((pygame.Vector2(-1, 1), pygame.Vector2(1, 1), pygame.Vector2(-1, 0), pygame.Vector2(1, 0)), 4):
                    disprint("winner2")
                    collision = getWorld(worldArrayNew, oldPosition + pos)
                    if (collision == None or not issubclass(type(collision), Particle)):
                        disprint("Found2")
                        self.position = oldPosition + pos
                        found = True
                        break
#           Roll back position so we don't have two in same space
            if (not found):
                disprint("Found")
                self.position = oldPosition
            

        setWorld(worldArrayNew, self.position, self)

        self.moveCallback(worldArrayNew)


class DustParticle(Particle):
        def __init__(self, position, velocity, airDensity):
            super().__init__(position, velocity, 1.540, (219, 227, 75), airDensity, 0.30, False, False)

class CoolerWallParticle(Particle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, 10000000000, (0, 0, 200), airDensity, 1.0, True, False, invincible = True)
class HeaterWallParticle(Particle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, 10000000000, (200, 0, 0), airDensity, 1.0, True, False, invincible = True)
                       
class ThermalParticle(Particle):
    def __init__(self, position, velocity, mass, airDensity, temp = 24.0, coeff = 0.4, colour = (199, 23, 109), colourtemp = True, liquid = False):
        self.temp = temp
        self.coeff = coeff
        self.commit = False
        self.colourtemp = colourtemp
        super().__init__(position, velocity, mass, colour, airDensity, 0.30, False, liquid)


    def tempCallback(self, temp):
        pass;
    def moveCallback(self, worldArrayNew):
        checkArray = []
        self.tempCallback(self.temp)

        for x in range(-1, 1 + 1):
            for y in range(-1, 1 + 1):
                collision = getWorld(worldArrayNew, self.position + Vector2(x,y))
                if (collision != None and isinstance(collision, CoolerWallParticle)):
                    self.temp -= COLD_WALL_STRENGTH
                if (collision != None and isinstance(collision, HeaterWallParticle)):
                    self.temp += COLD_WALL_STRENGTH
                if (collision != None and issubclass(type(collision), ThermalParticle)):
                    if (collision.temp > self.temp):
                        self.temp += self.coeff
                        collision.temp -= self.coeff
                    elif (collision.temp < self.temp):
                        collision.temp += self.coeff
                        self.temp -= collision.coeff

        
        if (self.colourtemp):
            self.colour = (min(self.temp * 5, 255) , self.colour[1], self.colour[2])


class WaterParticle(ThermalParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, 0.1, airDensity, coeff = 2,  colour = (20, 27, 180), colourtemp = False, liquid = True)

    def tempCallback(self, temp):
        self.liquid = True

        if (self.temp > 100):
            self.airDensity = 600
            self.colour = (0xf0, 0xf0, 0xff)
        elif (self.temp > 0):
            self.airDensity = AIR_DENSITY_DEF
            self.colour= (20, 27, 180)
        else:
            self.airDensity = AIR_DENSITY_DEF
            self.liquid = False
            self.colour = (0x99,255,255)



class ElectricalBaseParticle(Particle):
    def __init__(self, position, velocity, mass, colour, airDensity, dragCoeff, static, liquid, invincible = False):
        super().__init__(position, velocity, mass, colour, airDensity, dragCoeff, static, liquid, invincible = invincible)

    def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
        return False

class HeavyParticle(ElectricalBaseParticle):
        def __init__(self, position, velocity, airDensity, ultimate = False, colour = (199, 23, 9), static = False):
            self.ultimate = ultimate
            self.toExplode = 0
            super().__init__(position, velocity, 9000, colour, airDensity, 0.30, static, False, invincible = False)

        def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
            if (disable):
                return False
            
            self.explode(worldArrayNew)
            return True

        def explode(self, worldArrayNew, depth = 0):
            checkArray = []
            for x in range(-EXPLOSION_RADIUS, EXPLOSION_RADIUS + 1):
                for y in range(-EXPLOSION_RADIUS, EXPLOSION_RADIUS + 1):
                    checkArray.append(Vector2(int(x), int(y)))

            for pos in (random.sample(checkArray, len(checkArray))):
                collision = getWorld(worldArrayNew, self.position + pos)
                if (collision == None or not issubclass(type(collision), Particle)):
                    continue
                else:
                    collision.toExplode = 1 if pos.x < 0 else 2
                    collision.velocity = Vector2(random.randint(-EXPLOSION_STRENGTH, EXPLOSION_STRENGTH), random.randint(0, EXPLOSION_STRENGTH))

                    if issubclass(type(collision), ThermalParticle):
                        collision.temp += EXPLOSION_HEAT * ((EXPLOSION_RADIUS * 2) - (pos.x + pos.y) + 1)


            setWorld(worldArrayNew, self.position, None)
                
        def tickCallback(self, worldArrayNew):
            if (not self.ultimate):
                success = False

                checkArray = []
                for x in range(-EXPLOSION_ACTIVATION_RADIUS, EXPLOSION_ACTIVATION_RADIUS):
                    for y in range(-EXPLOSION_ACTIVATION_RADIUS, EXPLOSION_ACTIVATION_RADIUS + 1):
                        checkArray.append(Vector2(x, y))

                # Are we touching something to activate
                for pos in checkArray:
                    collision = getWorld(worldArrayNew, self.position + pos)
                    if (collision == None or not issubclass(type(collision), Particle) or collision.invincible or issubclass(type(collision), HeavyParticle)):
                        continue
                    else:
                        success = True

                # If we touch something then explode
                if (success):
                    self.explode(worldArrayNew)

            if (self.toExplode > 1):
                self.toExplode -= 1
            elif (self.toExplode == 1):
                self.explode(worldArrayNew)
            
        def moveCallback(self, worldArrayNew):
            self.tickCallback(worldArrayNew)


class C4Particle(HeavyParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, ultimate = True, colour = (121, 226, 242), static = True)

class WallParticle(ElectricalBaseParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, 10000000000, (29, 255, 29), airDensity, 1.0, True, False, invincible = True)

class WireParticle(ElectricalBaseParticle):
    def __init__(self, position, velocity, airDensity):
        self.charged = False
        self.ignore = False
        self.chargeSrc = Vector2(0,0)
        super().__init__(position, velocity, 10000000000, (0x46, 0x47, 0x3e), airDensity, 1.0, True, False, invincible = True)

    def electricalTickCallback(self, worldArrayNew):
        if (not self.charged or self.ignore):   
            self.ignore = False
            return
        else:
            for x in range(-1, 1 + 1):

                for y in range(-1, 1 + 1):
                    if (abs(y) == abs(x)):
                        continue

                    if (self.chargeSrc.x == x and self.chargeSrc.y == y):
                        continue

                    collision = getWorld(worldArrayNew, self.position + Vector2(x,y))
                    if (issubclass(type(collision), ElectricalBaseParticle)):
                        if (collision.setCharge(Vector2(-x, -y), worldArrayNew)):
                            self.charged = False
                            self.colour = (0x46, 0x47, 0x3e)
            self.charged = False
            self.colour = (0x46, 0x47, 0x3e)
            

    def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
        if (disable):
            return False
        
        self.charged = True
        self.colour = (255, 255, 0)
        self.chargeSrc = direction
        self.ignore = True

        return True


class InstWireParticle(ElectricalBaseParticle):
    def __init__(self, position, velocity, airDensity):
        self.charged = False
        self.chargeSrc = Vector2()
        self.expire = 0
        super().__init__(position, velocity, 10000000000, (0x46, 0x47, 0x3e), airDensity, 1.0, True, False, invincible = True)

    def electricalTickCallback(self, worldArrayNew):
        if (self.expire > 0):
            self.expire -= 1
            if (self.expire == 0):
                self.setCharge(Vector2(0,0), worldArrayNew, disable = True)

        pass
            

    def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
        self.charged = True
        self.colour = (0x46, 0x47, 0x3e) if disable else (255, 255, 0)
        self.chargeSrc = direction

        if (not disable):
            self.expire = expire

        for x in range(-1, 1 + 1):
            for y in range(-1, 1 + 1):
                if (abs(y) == abs(x)):
                    continue

                if (self.chargeSrc.x == x and self.chargeSrc.y == y):
                    continue

                collision = getWorld(worldArrayNew, self.position + Vector2(x,y))
                if (issubclass(type(collision), ElectricalBaseParticle)):
                    collision.setCharge(Vector2(-x, -y), worldArrayNew, disable = disable)

        return True


class WireWrapper:
    def __init__(self, direction):
        self.direction = direction
        self.chargeDirection = Vector2(-self.direction.x, -self.direction.y)
        self.charged = False

    def prepare(self, position, worldArray, updateCharged = False, charged = False):
        self.target = getWorld(worldArray, position + self.direction)
        self.worldArray = worldArray
        if (updateCharged):
            self.charged = charged

    def set(self, enable):
        if (issubclass(type(self.target), Particle)):
            self.target.setCharge(self.chargeDirection, self.worldArray, disable = not enable)
        self.charged = True
        
    def get(self):
        return self.charged
    
class BaseGateParticle(ElectricalBaseParticle):
    def __init__(self, position, velocity, airDensity, op):
        self.operation = op
            
        super().__init__(position, velocity, 10000000000, (0xff, 0xff, 0xff), airDensity, 1.0, True, False, invincible = True)

        self.dirs = ((-1, 0), (1, 0), (0, 1), (0, -1))
        self.wires = {}
        for direction in self.dirs:
            self.wires[direction] = WireWrapper(Vector2(direction))
            
    def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
        for key in self.wires:
            self.wires[key].prepare(self.position, worldArrayNew, updateCharged = (direction == Vector2(key)), charged = not disable)

        self.operation(self.wires[self.dirs[0]], self.wires[self.dirs[1]], self.wires[self.dirs[2]], self.wires[self.dirs[3]])
        

        return True

def notOp(l, r, u, d):
    r.set(not l.get())

def orOp(l, r, u, d):
    r.set(u.get() or d.get())

def xorOp(l, r, u, d):
    r.set((u.get() and not d.get()) or (d.get() and not u.get()))

def andOp(l, r, u, d):
    r.set(u.get() and d.get())



class NotGateParticle(BaseGateParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, notOp)

class OrGateParticle(BaseGateParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, orOp)

class XorGateParticle(BaseGateParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, xorOp)

class AndGateParticle(BaseGateParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, andOp)

class JunctionParticle(BaseGateParticle):
    def __init__(self, position, velocity, airDensity):
        super().__init__(position, velocity, airDensity, junctionOp)
        
class JunctionParticle(ElectricalBaseParticle):
    def __init__(self, position, velocity, airDensity):        
        super().__init__(position, velocity, 10000000000, (0x00, 0xff, 0xff), airDensity, 1.0, True, False, invincible = True)
            
    def setCharge(self, direction, worldArrayNew, expire = 0, disable = False):
        target = getWorld(worldArrayNew, self.position + Vector2(-direction.x,-direction.y))

        return target.setCharge(direction, worldArrayNew, disable = disable)

class GameWindow(Window):
    def __init__(self, position, extent, config):
        super().__init__(position, extent, config)
        
        self.worldArray = None
        if (os.path.isfile("worldarray.p")):
            self.worldArray = pickle.load(open("worldarray.p", "rb"))
        else:
            self.worldArray = numpy.empty(shape=(int(PARTICLE_AREA.x),int(PARTICLE_AREA.y)), dtype=object)

        
        for i in range(int(PARTICLE_AREA.x)):
            for height in range(2):
                setWorld(self.worldArray, Vector2(i, height), WallParticle(Vector2(i, height), Vector2(0, 0), AIR_DENSITY_DEF))

        self.renderTexture.fill((0,0,25))

        self.tools = {
                PointTool: PointTool(self.worldArray, self.config),
                ForceTool: ForceTool(self.worldArray, self.config),
                LineTool: LineTool(self.worldArray, self.config),
                TempTool: TempTool(self.worldArray, self.config),
                SparkTool: SparkTool(self.worldArray, self.config),
                CopiPeTool: CopiPeTool(self.worldArray, self.config)

        }

   
    def draw(self):
        self.renderTexture.fill((0,0,25))
        pos = list(pygame.mouse.get_pos())
        pos[0] /= WIDTH
        pos[0] *= RENDERWIDTH
        pos[1] /= HEIGHT
        pos[1] *= RENDERHEIGHT
        activeWindow = True
        if (pos[0] < 32 or pos[1] > self.renderTexture.get_height()):
            activeWindow = False
        pos[1] = -pos[1] + RENDERHEIGHT - 32
        pos[0] -= 32
        pos2  = (int(pos[0]), int(pos[1]))
        posVector = Vector2(int(pos[0]), int(pos[1]))

        if (not activeWindow):
            self.tools[self.config.tool.read()].deselect()

        if (activeWindow):
            self.tools[self.config.tool.read()].handle(posVector)

            piece = getWorld(self.worldArray, Vector2(pos))
            if issubclass(type(piece), ThermalParticle):
                self.renderTexture.blit(FONT.render("Temp: " + str(int(piece.temp)), True, (255, 50, 100)), Vector2(0,30))


        for tool in self.tools:
            self.tools[tool].update()


        for y in self.worldArray:
            for x in y:
                if (x == None or (not issubclass(type(x), Particle))):
                    continue;
                x.electricalTickCallback(self.worldArray)
        # Render array needs to be closed before exit
        renderArray = pygame.PixelArray(self.renderTexture)

        ncnt = 1
        pcnt = 0
        for i in range(ncnt):
            # Create new world array for updating
            worldArrayOld = numpy.copy(self.worldArray)
            for y in worldArrayOld:
                for x in y:
                    if (x == None or (not issubclass(type(x), Particle))):
                        continue;
                    if (i == ncnt - 1):
                        setWorld(renderArray, x.position, x.colour)

                        pcnt += 1
                        x.process(self.worldArray, self.config)


#            self.worldArray = worldArrayNew

        for tool in self.tools:
            self.tools[tool].draw(renderArray, posVector)

        renderArray.close()
        self.renderTexture.blit(FONT.render("Particles: " + str(pcnt), True, (255, 50, 100)), Vector2(0,0))
        self.renderTexture.blit(FONT.render("Brush: " + str(self.config.toolSize), True, (255, 50, 100)), Vector2(132,0))

windowParams = [
    (StatsWindow, (0, 0), ((TILE_SIZE * 2), 0), 0),
    (GameWindow, ((TILE_SIZE * 2), 0), PARTICLE_AREA),
    (ControlWindow, (TILE_SIZE * 2, RENDERHEIGHT - TILE_SIZE * 2), (PARTICLE_AREA.x, TILE_SIZE * 2) , 0),
]

# Creates all windows
def init_windowing(windowList, config):
    for window in windowParams:
        extent = (window[2][0] if window[2][0] != 0 else RENDERWIDTH, window[2][1] if window[2][1] != 0 else RENDERHEIGHT)
        windowList.append(window[0](window[1], extent, config))

    return windowList

def main():
    global screen
    global frameCounter
    global FONT
    pygame.init()
    FONT = pygame.font.SysFont("comicsans", 21, italic=True)

    screenTarget = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.Surface((RENDERWIDTH, RENDERHEIGHT))

    config = Configuration(DataHolder(PointTool), DataHolder(DustParticle), 2, DataHolder(BorderVoid), DataHolder(BorderReflection))

    windowList = init_windowing([], config) # Holds all windows to be rendered
    sys.setrecursionlimit(1500)

    prev_time = time.time()

    clicked = False
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):           
                pickle.dump(windowList[1].worldArray, open("worldarray.p", "wb"))

                sys.exit()
            if event.type == pygame.KEYDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                if event.button == 4:
                    config.toolSize += 1
                elif event.button == 5:
                    if (config.toolSize >= 1):
                        config.toolSize -= 1

        if (clicked):
            for window in windowList:        
                window.draw()
                screen.blit(window.renderTexture, window.position)
        else:
            screen.blit(FONT.render("Lclick: place particle", False, (255, 50, 100)), Vector2(0,24))
            screen.blit(FONT.render("Rclick: erase particle", False, (255, 50, 100)), Vector2(0,48))
            screen.blit(FONT.render("Mwheel: change tool size", False, (255, 50, 100)), Vector2(0,72))
            screen.blit(FONT.render("ANY KEY TO START", False, (255, 50, 100)), Vector2(30,90))
        screenTarget.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0,0))

        pygame.display.flip()


        frameCounter += 1
        frameCounter %= TARGET_FPS

        #Timing code at the END!
        curr_time = time.time()#so now we have time after processing
        diff = curr_time - prev_time#frame took this much time to process and render
        delay = max(1.0/TARGET_FPS - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
#        time.sleep(delay)
        fps = 1.0/diff#fps is based on total time ("processing" diff time + "wasted" delay time)
        prev_time = curr_time
        pygame.display.set_caption("{0}: {1:.2f}".format(TITLE, fps))

frameCounter = 0

main()
