import os, hashlib
import subprocess as sp

def processPlayerMove(num, board):
    col = int(input("Column: "))
    for i in range(len(board)):
        if(board[i][col] == 0 and not board[i+1][col] == 0):
            board[i][col] = num
            break;
    return board;
def processPlayerMoveNoInput(num, col, board):
    for i in range(len(board)):
        if(board[i][col] == 0 and not board[i+1][col] == 0):
            board[i][col] = num
            break;
    return board;

def checkWin(board):
    checkamount = 0
    checkplayerid = 0
    for i in range(len(board) - 1):
        for j in range(len(board[i])):
            if(not board[i][j] == 0):
                if(board[i][j] == checkplayerid):
                    checkamount += 1
                else:
                    checkplayerid = board[i][j]
                    checkamount = 0
            if(checkamount == 3):
                return checkplayerid;
        checkplayerid = 0
        checkamount = 0

    checkamount = 0
    checkplayerid = 0
    for i in range(len(board[0])):
        for j in range(len(board) - 1):
            if(not board[j][i] == 0):
                if(board[j][i] == checkplayerid):
                    checkamount += 1
                else:
                    checkplayerid = board[j][i]
                    checkamount = 0
            if(checkamount == 3):
                return checkplayerid
        checkplayerid = 0
        checkamount = 0

    checkamount = 0
    checkplayerid = 0
    for i in range(len(board) - 1):
        for j in range(len(board[i])):
            if (board[i][j] == 0):
                continue;
            checkplayerid = board[i][j]
            checkamount = 0
            for c in range(4):
                if (i-c < 0):
                    break;
                if (len(board[i]) - 1 < j+c):
                    break;
                if (board[i-c][j+c] == checkplayerid):
                    checkamount += 1
            if (checkamount == 4):
                return checkplayerid

    checkamount = 0
    checkplayerid = 0
    for i in range(len(board) - 1):
        for j in range(len(board[i])):
            if (board[i][j] == 0):
                continue;
            checkplayerid = board[i][j]
            checkamount = 0
            for c in range(4):
                if (len(board) - 2 < i+c):
                    break;
                if (len(board[i]) - 1 < j+c):
                    break;
                if (board[i+c][j+c] == checkplayerid):
                    checkamount += 1
            if (checkamount == 4):
                return checkplayerid
    return 0;

def printBoard(game_board):
    print("\033[1;34;47m " + "_" * (len(game_board[0]) * 2) + " ")
    for i in range(len(game_board) - 1):
        print("\033[1;34;47m|", end="")
        for j in range(len(game_board[i])):
            if (game_board[i][j] == 0):
                print(" ", end=" ")
            elif (game_board[i][j] == 1):
                print("\u001b[33;1mo\033[1;34;47m", end=" ")
            else: print("\u001b[31;1mo\033[1;34;47m", end=" ")
        print("|")
    print("|" + "-" * (len(game_board[0]) * 2) + "|")
    print("|", end="")
    for i in range(len(game_board[0])):
        print(str(i)[0], end=" ")
    print("|")
    print("|", end="")
    for i in range(len(game_board[0])):
        if (len(str(i)) > 1):
            print(str(i)[1], end=" ")
        else: print(" ", end=" ")
    print("|")
def printBoardAI(game_board):
    print(" " + "_" * (len(game_board[0]) * 2) + " ")
    for i in range(len(game_board) - 1):
        print("|", end="")
        for j in range(len(game_board[i])):
            if (game_board[i][j] == 0):
                print(" ", end=" ")
            elif (game_board[i][j] == 1):
                print("x", end=" ")
            else: print("o", end=" ")
        print("|")
    print("|" + "-" * (len(game_board[0]) * 2) + "|")
    print("|", end="")
    for i in range(len(game_board[0])):
        print(str(i)[0], end=" ")
    print("|")
    print("|", end="")
    for i in range(len(game_board[0])):
        if (len(str(i)) > 1):
            print(str(i)[1], end=" ")
        else: print(" ", end=" ")
    print("|")

def main():
    game_board = [[0,0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [9,9,9,9,9,9]]
    while(True):
        print("Connect 4")
        printBoardAI(game_board)
        print("Player One")
        game_board = processPlayerMove(1, game_board)
 
        winner = checkWin(game_board)
        if (winner):
            printBoard(game_board)
            print(" Player", winner, "Won")
            return 0;

        print("Connect 4")
        printBoardAI(game_board)

        print("Player Two")
        game_board = processPlayerMove(2, game_board)


        winner = checkWin(game_board)
        if (winner):
            printBoardAI(game_board)
            print(" Player", winner, "Won")
            return 0;
main()
