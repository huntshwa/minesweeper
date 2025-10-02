import random
import time
import pygame
import os

field = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1]]

visible =[[False for _ in row] for row in field]

flagged =[[False for _ in row] for row in field]

blockNum = len(field) * len(field[0])
start = 0
isZero = []

width = 35
height = 35

lightGray = (192, 192, 192)
black = (0, 0, 0)

def loadImage(name, folder, size=None):
    #load and optionally scale an image
    path = os.path.join(folder, name + ".png")
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def printGrid(grid):
    #prints the grid to console

    for row in grid:
        for i in row:
            print(i, end=" ")
        print()


def startBombs():
    #assigns bombs to squares

    bombs =[]
    global numBombs

    while numBombs != 10:
        row = random.randint(0,len(field) - 1)
        column = random.randint(0,len(field) - 1)

        if field[row][column] != 9 and 0 not in surroundingCells(field, row, column) and field[row][column] != 0:
            field[row][column] = 9
            numBombs += 1

def endGame():
    #ends the game when bomb is clicked

    for rowIndex, row in enumerate(field):
        for colIndex, element in enumerate(row):
            if element == 9:
                visible[rowIndex][colIndex] = True

def checkWin():
    #checks for win

    count = 0
    for rowIndex, row in enumerate(field):
        for colIndex, element in enumerate(row):
            if element != 9 and visible[rowIndex][colIndex]:
                count += 1

    return count == blockNum - numBombs

def surroundingCells(grid,row,column):
    #checks the surrounding squares of an element in a dict

    displacement = [[-1,1],[0,1],[1,1],[-1,0],[1,0],[-1,-1],[0,-1],[1,-1]]
    newSurround = []
    squares = []

    for i in displacement:
        if not((i[1] + row) == len(field) or (i[0] + column) == len(field[0]) or (i[1] + row) == -1 or (i[0] + column) == -1):
            newSurround.append(i)
    for i in newSurround:
        squares.append(grid[i[1] + row][i[0] + column])

    return squares

def zeroingCells(grid,row,column):
    '''
    when you coded this you were stupid and didnt make it dictionary and then i tried
    to change this but other stuff already uses this so here you go, new function!
    '''
    #reports surrounding squares of an element as a nested list w/ value at 0 and pos after

    displacement = [[-1,1],[0,1],[1,1],[-1,0],[1,0],[-1,-1],[0,-1],[1,-1]]
    newSurround = []
    squares = []

    for i in displacement:
        if not((i[1] + row) == len(field) or (i[0] + column) == len(field[0]) or (i[1] + row) == -1 or (i[0] + column) == -1):
            newSurround.append(i)
    for i in newSurround:
        squares.append([grid[i[1] + row][i[0] + column], i])

    return squares

def numberTiles():
    #numbers each tile

    surrounding = []

    for rowIndex, row in enumerate(field):
        for colIndex, element in enumerate(row):
            if element != 9:
                surrounding = surroundingCells(field,rowIndex,colIndex)
                for i in surrounding[:]:
                    if i != 9:
                        surrounding.remove(i)
                field[rowIndex][colIndex] = len(surrounding)

pygame.init()

screensize = [width * len(field) + 20, height * len(field[0]) + 60]
screen = pygame.display.set_mode(screensize)

#tells computer to take resources from minesweeper folder
base_dir = os.path.dirname(os.path.abspath(__file__))
resources = os.path.join(base_dir, "Minesweeper Resources")

tile_size = (width, height)
sprites = {
    "0": loadImage("zeroTile", resources, tile_size),
    "1": loadImage("oneTile", resources, tile_size),
    "2": loadImage("twoTile", resources, tile_size),
    "3": loadImage("threeTile", resources, tile_size),
    "4": loadImage("fourTile", resources, tile_size),
    "5": loadImage("fiveTile", resources, tile_size),
    "6": loadImage("sixTile", resources, tile_size),
    "7": loadImage("sevenTile", resources, tile_size),
    "8": loadImage("eightTile", resources, tile_size),
    "cell": loadImage("cell", resources, tile_size),
    "bomb": loadImage("bomb", resources, tile_size),
    "flag": loadImage("flag", resources, tile_size),
}

digits = {
    "t0": loadImage("zeroChar", resources, tile_size),
    "t1": loadImage("oneChar", resources, tile_size),
    "t2": loadImage("twoChar", resources, tile_size),
    "t3": loadImage("threeChar", resources, tile_size),
    "t4": loadImage("fourChar", resources, tile_size),
    "t5": loadImage("fiveChar", resources, tile_size),
    "t6": loadImage("sixChar", resources, tile_size),
    "t7": loadImage("sevenChar", resources, tile_size),
    "t8": loadImage("eightChar", resources, tile_size),
    "t9": loadImage("nineChar", resources, tile_size)
}

faces = {
    "smile": loadImage("smileFace", resources, tile_size),
    "frown": loadImage("sadFace", resources, tile_size),
    "neutral": loadImage("neutralFace", resources, tile_size)
}


pygame.display.set_caption("Budget Minesweeper")
pygame.display.set_icon(sprites["bomb"])

timer = None
numBombs = 0
flags = 0
currentFace = faces["neutral"]


running = True
gameOver = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and gameOver:
            #checks mouse position when clicked and stores

            x, y = pygame.mouse.get_pos()
            col = (x - 10) // width
            row = (y - 40) // height

            if pygame.mouse.get_pressed()[0]: #left click

                if 0 <= row < len(field) and 0 <= col < len(field[0]):
                    #changes status on a cell to be revealed
                    if not any(any(r) for r in visible):
                        #checks for first click

                        field[row][col] = 0
                        startBombs()
                        numberTiles()
                        timer = time.time()
                        flags = numBombs

                    if not flagged[row][col]:
                        visible[row][col] = True


            elif pygame.mouse.get_pressed()[2] and any(any(r) for r in visible): #right click
                if 0 <= row < len(field) and 0 <= col < len(field[0]):
                    if not visible[row][col]:
                        if not flagged[row][col] and flags > 0:
                            flagged[row][col] = True
                            flags -= 1

                        elif flagged[row][col] and flags <= numBombs:
                            flagged[row][col] = False
                            flags += 1

    screen.fill(lightGray)
    screen.blit(sprites["flag"], (10, 5))

    yPos = 0

    for rowIndex, row in enumerate(field):
        xPos = 0  # Reset for each row
        for colIndex, element in enumerate(row):
            x = xPos + 10
            y = yPos + 50

            if visible[rowIndex][colIndex]:
                #checks if cell has been revealed or not
                if element == 9:
                    #changes sprite to bomb
                    screen.blit(sprites["bomb"], (x, y))
                    currentFace = faces["frown"]
                    endGame()
                    gameOver = False
                elif element == 0:
                    #changes sprite to 0 and does zeroing feature by checking surrounding squares
                    screen.blit(sprites["0"], (x, y))
                    for i in zeroingCells(field, rowIndex, colIndex):
                        visible[rowIndex + i[1][1]][colIndex + i[1][0]] = True
                else:
                    #changes sprite to designated square according to field
                    screen.blit(sprites[str(element)], (x, y))
            elif flagged[rowIndex][colIndex]:
                #detects flagging
                screen.blit(sprites["flag"], (x, y))
            else:
                #cell stays hidden
                screen.blit(sprites["cell"], (x, y))
            xPos += width
        yPos += height

    if timer is None:
        #sets the timer to the default setting

        screen.blit(digits["t0"], (290, 5))
        screen.blit(digits["t0"], (255, 5))
        screen.blit(digits["t0"], (220, 5))

    if timer is not None and gameOver:
        #ticks the timer while the game is running

        elapsed = min(int(time.time() - timer), 999)
        elapsedStr = str(elapsed).zfill(3)
        elapsedInt = list(map(int, elapsedStr))

        timerXPos = 220
        for i in elapsedInt:

            screen.blit(digits["t" + str(i)], (timerXPos, 5))
            timerXPos += 35

    if not gameOver:
        #freezes timer when game ends

        timerXPos = 220
        for i in elapsedInt:

            screen.blit(digits["t" + str(i)], (timerXPos, 5))
            timerXPos += 35

    if checkWin():
        currentFace = faces["smile"]
        gameOver = False

    flagStr = str(flags).zfill(3)
    flagInt = list(map(int, flagStr))

    flagXPos = 50
    for i in flagInt:

        screen.blit(digits["t" + str(i)], (flagXPos, 5))
        flagXPos += 35

    screen.blit(currentFace, (170, 5))

    pygame.display.update()

pygame.quit()
