import subprocess as sp
import os
import random
import pygame

WIDTH = 20
HEIGHT = 20

DOWN = 2
LEFT = -1
RIGHT = 1
ROTATE = 9
LONGFOUR= 0
SQUARE = 1
LPIECE = 3
RPIECE = 4
PIECE_SIZE = 30
X = 0
Y = 1

DEG0 = 0
DEG90 = 1
DEG180 = 2
DEG270 = 3

pieces =[
        [ # Long 4 piece
            1,
            [ # 0 deg rotate            
                1, # Max length
                [ # Actual shape
                    [1],
                    [1],
                    [1],
                    [1]
                ],
                [4]
            ], [ # 90 deg rotate
                4,
                [
                    [1, 1, 1, 1]
                ],
                [1, 1, 1, 1]
            ], [ # 180 deg rotate
                1,
                [
                    [1],
                    [1],
                    [1],
                    [1]
                ],
                [4]
            ], [ #270 deg rotate
                4,
                [
                    [1, 1, 1, 1]
                ],
                [1, 1, 1, 1]
            ]
        ], [ # Square
            2,
            [ # 0 deg rotate
                2, # Max length
                [ # Actual shape
                    [2,2],
                    [2,2]
                ],
                [2, 2]
            ], [ # 90 deg rotate
                2, # Max length
                [ # Actual shape
                    [2,2],
                    [2,2]
                ],
                [2, 2]
            ], [ # 180 deg rotate
                2, # Max length
                [ # Actual shape
                    [2,2],
                    [2,2]
                ],
                [2, 2]
            ], [ #270 deg rotate
                2, # Max length
                [ # Actual shape
                    [2,2],
                    [2,2]
                ],
                [2, 2]
            ]
        ], [ # L Shape
            3,
            [ # 0 deg rotate
                2, # Max length
                [ # Actual shape
                    [3],
                    [3],
                    [3,3]
                ],
                [3,1]
            ], [ # 90 deg rotate
                3, # Max length
                [ # Actual shape
                    [3,3,3],
                    [3]
                ],
                [2,1,1]
            ], [ # 180 deg rotate
                2, # Max length
                [ # Actual shape
                    [3,3],
                    [0,3],
                    [0,3]
                ],
                [1,3]
            ], [ #270 deg rotate
                3, # Max length
                [ # Actual shape
                    [0,0,3],
                    [3,3,3]
                ],
                [2,2,2]
            ]
        ], [ # J Shape
            4,
            [ # 0 deg rotate
                2, # Max length
                [ # Actual shape
                    [0,4],
                    [0,4],
                    [4,4]
                ],
                [3,3]
            ], [ # 90 deg rotate
                3, # Max length
                [ # Actual shape
                    [4,0,0],
                    [4,4,4]
                ]
            ], [ # 180 deg rotate
                2, # Max length
                [ # Actual shape
                    [4,4],
                    [4,0],
                    [4,0]
                ],
                [3, 1]
            ], [ #270 deg rotate
                3, # Max length
                [ # Actual shape
                    [4,4,4],
                    [0,0,4]
                ],
                [1,1,2]
            ]
        ],  [ # oIo Shape
            5,
            [ # 0 deg rotate
                3, # Max length
                [ # Actual shape
                    [0,5,0],
                    [5,5,5]
                ],
                [2,2,2]
            ], [ # 90 deg rotate
                2, # Max length
                [ # Actual shape
                    [5,0],
                    [5,5],
                    [5,0]
                ],
                [3,2]
            ], [ # 180 deg rotate
                2, # Max length
                [ # Actual shape
                    [5,5,5],
                    [0,5,0]
                ],
                [1,2,1]
            ], [ #270 deg rotate
                3, # Max length
                [ # Actual shape
                    [0,5],
                    [5,5],
                    [0,5]
                ],
                [2,3]
            ]
        ]
        ]
def get_piece(num, rot):
    return pieces[num][0], pieces[num][rot+1]

def get_key(uchar):
    # Arrow key code start, recurse
    if (uchar == b'\xe0'):
        return get_key(getch())
    if (uchar == b'M'):
        return RIGHT
    if (uchar == b'K'):
        return LEFT
    if (uchar == b'P'):
        return DOWN
    if (uchar == b'r'):
        return ROTATE

def clearLines(board):
#    for row in range(len(board)):
#        if (str(board[row]) == FULL_ROW and row < len(board) - 1):
#            board.pop(row)
#            board.insert(0, [0] * WIDTH)
#               print("MATHC")
    return board;

   
def game_loop(board):
    
    running = True
    pnis =0
    pnos = 0
    fpsCounter = pygame.time.Clock()
    currentPiece = 0
    currentPieceColor = 0
    currentPiecePos = [int(WIDTH / 2) - 1,0]
    currentPieceRot = DEG0
    pastPieceRot = DEG0
    pastPiecePos = [0,0]
    screenTarget = pygame.display.set_mode((WIDTH*PIECE_SIZE, HEIGHT*PIECE_SIZE))
    while running:
        pnis += 1
        currentInput = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    currentInput = RIGHT
                elif event.key == pygame.K_LEFT:
                    currentInput = LEFT
                elif event.key == pygame.K_e:
                    currentInput = ROTATE
        screenTarget.fill((0,0,0))
        for row in range(len(board)):
            for col in range(len(board[row])):
                if (board[row][col]==1):
                    pygame.draw.rect(screenTarget, (255,255,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==2):
                    pygame.draw.rect(screenTarget, (0,255,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==3):
                    pygame.draw.rect(screenTarget, (255,255,0), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==4):
                    pygame.draw.rect(screenTarget, (255,0,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==5):
                    pygame.draw.rect(screenTarget, (0,0,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==6):
                    pygame.draw.rect(screenTarget, (0,255,0), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==7):
                    pygame.draw.rect(screenTarget, (255,0,0), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==8):
                    pygame.draw.rect(screenTarget, (0,100,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
                if (board[row][col]==9):
                    pygame.draw.rect(screenTarget, (100,0,255), pygame.Rect(PIECE_SIZE*col, PIECE_SIZE*row, PIECE_SIZE, PIECE_SIZE))
#        if (kbhit()):
#            currentInput = get_key(getch())

        if (currentInput == ROTATE):
            if (currentPieceRot == DEG270):
                currentPieceRot = DEG0
            else:
                currentPieceRot += 1
            currentInput = 0
            
        currentPieceColor, pieceArray = get_piece(currentPiece, currentPieceRot)
        pieceMaxLen = pieceArray[0]
        pieceHArray = pieceArray[2]
        pieceArray = pieceArray[1]
        currestPieceColor, pastPieceArray = get_piece(currentPiece, pastPieceRot)
        pastPieceMaxLen = pastPieceArray[0]
        pastPieceArray = pastPieceArray[1]


#
#        print(pastPiecePos)
#        print(currentPiecePos)
                        
        for row in range(len(pastPieceArray)):
            for col in range(len(pastPieceArray[row])):
                if (pastPieceArray[row][col]):
                    board[pastPiecePos[Y] + row][pastPiecePos[X] + col] = 0

        for row in range(len(pieceArray)):
            for col in range(len(pieceArray[row])):
                if (pieceArray[row][col]):
                    try:
                        board[currentPiecePos[Y] + row][currentPiecePos[X] + col] = pieceArray[row][col]
                    except IndexError:
                        pass
        for i in range(pieceMaxLen):
            if (board[currentPiecePos[Y] + pieceHArray[i]][currentPiecePos[X] + i] and not pnos):
                pnos = 100


        if (pnos > 0):
            pnos -= 1
            if (pnos == 0):
                board = clearLines(board)
                currentPiece = random.randint(0, 2)
                currentPiecePos = [int(WIDTH / 2) - 1,0]
                currentPieceRot = 0
                pastPiecePos = [0,0]
                pnis = 0
        pastPieceRot = currentPieceRot
        pastPiecePos[X] = currentPiecePos[X]
        pastPiecePos[Y] = currentPiecePos[Y]
        if (pnis == 80 and not pnos):
            currentPiecePos[Y] += 1
            pnis = 0
        if (currentPiecePos[X] + currentInput < 0 or currentPiecePos[X] + currentInput > WIDTH):
            currentInput = 0;
        for row in range(len(pieceArray)):
            if (board[currentPiecePos[Y] + row][currentPiecePos[X] + currentInput] and board[currentPiecePos[Y] + row][currentPiecePos[X] + currentInput] != currentPieceColor and pieceArray[row]):
                currentInput = 0;

        currentPiecePos[X] += currentInput
        pygame.display.flip()

        
            
        
        
    
def main():
    pygame.init()
    board = [ [0] * WIDTH for j in range(HEIGHT)]
    board.append([1] * WIDTH)
    return game_loop(board)
    


main()
