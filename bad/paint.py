import pygame, os, numpy, math, random
WIDTH, HEIGHT = 500,500
MAP_SIZE = 30
PIECE_SIZE = 20
MAP_DISPLAY = numpy.zeros((MAP_SIZE, MAP_SIZE, 3), dtype=int)
pygame.init()
screenTarget = pygame.display.set_mode((WIDTH, HEIGHT))
currentBrushColor = (100,100,0)
while True:
    for event in pygame.event.get():
        pass
    screenTarget.fill((0,0,0))
    for row in range(len(MAP_DISPLAY)):
         for col in range(len(MAP_DISPLAY[row])):
            pygame.draw.rect(screenTarget, (MAP_DISPLAY[row,col,0],MAP_DISPLAY[row,col,1],MAP_DISPLAY[row,col,2]), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
            
    if (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
        mousePos = pygame.mouse.get_pos()
        color = currentBrushColor
        if (pygame.mouse.get_pressed()[2]):
            color = (0,0,0)

        MAP_DISPLAY[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE),0] = color[0]
        MAP_DISPLAY[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE),1] = color[1]
        MAP_DISPLAY[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE),2] = color[2]

    pygame.display.flip()

    
 

    
