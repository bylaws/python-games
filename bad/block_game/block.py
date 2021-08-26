import pyglet
from pyglet.gl import *
from pyglet.window import key
import math, random

WIDTH = 1000
HEIGHT = 1000

WORLD_HEIGHT = 20
WORLD_WIDTH = 21
WORLD_LENGTH = 20
TEX_SIDE = 0
TEX_TOP = 1
TEX_BOTTOM = 2
PLAYER_HEIGHT = 2
BLOCK_AIR = 0
BLOCK_DIRT = 1
GFS = 0.01
world = [[[BLOCK_DIRT] * WORLD_LENGTH for i in range(WORLD_WIDTH)]]
for k in range(WORLD_HEIGHT - 1): #For bottom blocks
    world.append([[BLOCK_AIR] * WORLD_LENGTH for i in range(WORLD_WIDTH)])

worldQuads = [[[[0] for x in range(WORLD_LENGTH)] for z in range(WORLD_WIDTH)] for y in range(WORLD_HEIGHT)] #4D array FTW
yVelocity = 0
print(world)
textures = []
rot = [0,0]
pos = [0,0,0]
touchingFloor = False
window = pyglet.window.Window(height=HEIGHT, width=WIDTH) 
keys = key.KeyStateHandler()
window.push_handlers(keys)
def set_block(x, y, z, blockid):
    world[y][z][x] = blockid;

    if (len(worldQuads[y][z][x]) > 1):
        for quad in worldQuads[y][z][x]:
            quad.delete()

    worldQuads[y][z][x] = make_block(x, y, z, blockid)

def load_image(file_path):
    tex = pyglet.image.load(file_path).get_texture()
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

def load_air():
    textures.append([]) # STUB AS DIR IS NOTHING


def load_dirt():
    tex = []
    tex.append(load_image("b.bmp")) # SIDE
    tex.append(load_image("a.bmp")) # TOP
    tex.append(load_image("b.bmp")) # BOTTOM
    textures.append(tex) # BLOCK_DIRT

def set_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, WIDTH/HEIGHT, 0.05, 1000)#fov
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def set_2d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,WIDTH,0,HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def make_block(x, y, z, blockid):
    if (blockid == 0):
        return [0];
    quadGroup = []
    X, Y, Z = x+1, y+1, z+1

    tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_SIDE],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords)) # back
    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_SIDE],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)) # front

    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_SIDE],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords))  # left
    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_SIDE],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords))  # right

    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_TOP],   ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords))  # bottom
    quadGroup.append(batch.add(4, GL_QUADS, textures[blockid][TEX_BOTTOM],   ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords))  # top
    
    return quadGroup
@window.event
def update(dt):
    global touchingFloor
    global yVelocity
    s = dt*10
    rotY = -rot[1]/180*math.pi
    dx,dz = s*math.sin(rotY),s*math.cos(rotY)
    if keys[key.W]:
        pos[0]+=dx
        pos[2]-=dz
    if keys[key.S]:
        pos[0]-=dx
        pos[2]+=dz
    if keys[key.A]:
        pos[0]-=dz
        pos[2]-=dx
    if keys[key.D]:
        pos[0]+=dz
        pos[2]+=dx

    if (world[math.ceil(pos[1])][int(pos[2])][int(pos[0])]):
        touchingFloor = True
        yVelocity = 0
    else:
        touchingFloor = False
    if (keys[key.SPACE] and touchingFloor):
        yVelocity = 0.214

    pos[1] += yVelocity
    if (not touchingFloor):
        yVelocity -= GFS

@window.event
def on_mouse_press(x, y, button, modifiers):
    print(rot)
    m = math.cos(math.radians(rot[0]))
    stepY = (math.sin(math.radians(rot[0]))) / 10000
    stepZ = -((math.cos(-math.radians(rot[1])) * m)) / 10000
    stepX = ((math.sin(-math.radians(rot[1])) * m)) / 10000

    hit = False
    rayY = stepY
    rayX = stepX
    rayZ = stepZ
    step = 0
    while (not hit):
        if (world[int(pos[1] + rayY + PLAYER_HEIGHT)][int(pos[2] + rayZ)][int(pos[0] + rayX)]):
            print(step)
            hit = True
            if (step == 0): # ABOVE BLOCK
                set_block(int(pos[0] + rayX), int(pos[1] + rayY) + 2, int(pos[2] + rayZ), 1)
            break
        step = (step + 1) % 3
        if (step == 0):
            rayY += stepY
        if (step == 1):
            rayX += stepX
        if (step == 3):
            rayZ += stepZ
        if (rayX > 5 or rayY > 5 or rayZ > 5):
            return
        

@window.event
def on_show():
    global batch
    load_air()
    load_dirt()
    batch = pyglet.graphics.Batch()
    for y in range(WORLD_HEIGHT):
        for z in range(WORLD_WIDTH):
            for x in range(WORLD_LENGTH):
                worldQuads[y][z][x] = make_block(x, y, z, world[y][z][x])

@window.event
def on_mouse_motion(x,y,dx,dy):
    global rot
    dx/= 8
    dy/= 8
    rot[0] += dy
    rot[1] -= dx
    if rot[0]>90:
        rot[0] = 90
    elif rot[0] < -90:
        rot[0] = -90

@window.event
def on_draw():
    global batch
    global rot
    window.clear()
    data = [0xffffff for _ in range (0, 50*50*3)]
    set_3d()
    glPushMatrix()
    glRotatef(-rot[0],1,0,0)
    glRotatef(-rot[1],0,1,0)
    glTranslatef(-pos[0], -pos[1] - PLAYER_HEIGHT - 0.5, -pos[2])
    batch.draw()
    glPopMatrix()
    set_2d()
    glRasterPos2f(int(WIDTH/2), int(HEIGHT/2))
    glDrawPixels(50, 50, GL_RGB, GL_UNSIGNED_INT, (GLuint * len(data))(*data))
pyglet.clock.schedule(update)
glClearColor(0.5,0.7,1,1)
glEnable(GL_DEPTH_TEST)
pyglet.app.run()


























