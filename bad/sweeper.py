import pygame, os, numpy, math, random
MAP_SIZE = 10
WIDTH, HEIGHT = 500,500
BOMBS = 30
BOMB = 9
PIECE_SIZE = 16
UNDISC = 10
MAP = numpy.zeros((MAP_SIZE, MAP_SIZE), dtype=int)
MAP_DISPLAY = numpy.full((MAP_SIZE, MAP_SIZE), UNDISC, dtype=int)
pygame.init()
screenTarget = pygame.display.set_mode((WIDTH, HEIGHT))
PALETTE = [(0,100,0),(0,200,0),(0,255,0),(0,0,100),(0,0,200),(0,0,255),(100,0,0),(200,0,0),(255,0,0)]
FLAG = 78
def find_stuff(x, y):
    global MAP_DISPLAY
    global MAP
    for pos in [(x - 1, y), (x + 1, y), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x, y - 1), (x, y + 1), (x,y)]:
        try:
            if (pos[0] >= 0 and pos[1] >= 0):
                if (MAP[pos[0], pos[1]] < BOMB and MAP_DISPLAY[pos[0], pos[1]] == UNDISC):
                    MAP_DISPLAY[pos[0], pos[1]] = MAP[pos[0], pos[1]]
                    if (MAP[pos[0], pos[1]] == 0):
                        find_stuff(pos[0], pos[1])
        except IndexError:
            continue;

for i in range(BOMBS):
    bombX, bombY = random.randint(0,MAP_SIZE-1),random.randint(0,MAP_SIZE-1)
    MAP[bombX, bombY] = BOMB
    for pos in [(bombX - 1, bombY), (bombX + 1, bombY), (bombX - 1, bombY - 1), (bombX + 1, bombY - 1), (bombX - 1, bombY + 1), (bombX + 1, bombY + 1), (bombX, bombY - 1), (bombX, bombY + 1)]: #All 8 directions aside
        try:
            if (pos[0] >= 0 and pos[1] >= 0):
                if (MAP[pos[0], pos[1]] != BOMB):
                    MAP[pos[0], pos[1]] += 1
        except IndexError:
            continue;

#font = pygame.font.Font('mine.ttf', int((30*HEIGHT) / 500))
#scoreText = font.render(str(score), True, (13,11,230), (0,0,0))

while True:
    for event in pygame.event.get():
        pass
    screenTarget.fill((0,0,0))
    for row in range(len(MAP_DISPLAY)):
         for col in range(len(MAP_DISPLAY[row])):
            if (MAP_DISPLAY[row][col] == BOMB):
                pygame.draw.rect(screenTarget, (255,255,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
            elif (MAP_DISPLAY[row][col] == FLAG):
                pygame.draw.rect(screenTarget, (255,0,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
            elif (MAP_DISPLAY[row][col] == UNDISC):
                pygame.draw.rect(screenTarget, (0,0,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
            elif (MAP_DISPLAY[row][col] == 0):
                pygame.draw.rect(screenTarget, (0,0,0), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
            elif (MAP_DISPLAY[row][col] > 0):
                pygame.draw.rect(screenTarget, PALETTE[MAP_DISPLAY[row][col]-1], pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))

    if (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
        mousePos = pygame.mouse.get_pos()
        if (pygame.mouse.get_pressed()[2]):
            MAP_DISPLAY[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE)] = FLAG
            if (MAP[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE)] != BOMB):
                print("LOSS")
                djks.sysd()
        elif (MAP[int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE)] == BOMB):
            print("LOSS")
            sys.cfsdio()
        else:
            find_stuff(int(mousePos[1] / PIECE_SIZE), int(mousePos[0] / PIECE_SIZE))
            
        
    pygame.display.flip()

    
 

    
