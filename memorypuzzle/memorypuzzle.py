#Memory Puzzle


import random, pygame, sys
from pygame.locals import *

FPS = 30 #초당 프레임 프로그램의 일반 속도
WINDOWWIDTH = 640 #윈도우의 너비(픽셀 단위)
WINNDOWHEIGHT = 480 #원도우의 높이(픽셀 단위)
REVEALSPEED = 8 #상자가 보였다 가려지는 속도
BOXSIZE = 40 #상자의 너비와 높이(팍셀 단위)
GAPSIZE = 10 #상자 사이의 간격(픽셀 단위)
BOARDWIDTH = 10 #아이콘 가로줄 수
BOARDHEIGHT = 7

assert (BOARDWIDTH * BOARDHEIGHT) %2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) /2)
YMARGIN = int((WINNDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) /2)


#
gray = (100,100,100)
navyblue = (60,60,100)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0, 0,255)
yello = (255, 255,  0)
orange = (255,128,0)
purple = (255, 0, 255)
cyan = (0.255,255)

bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue

dount = 'dount'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'


allcolor = (red,green,blue,yello,orange,purple,cyan)
allshapes = (dount, square, diamond, lines, oval)

assert len(allcolor) * len(allshapes) * 2 >= BOARDWIDTH * BOARDHEIGHT,"Board is too big for the number of shapes/colors definded."


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINNDOWHEIGHT))

    mousex = 0 #마우스이벤트 발생시 x좌표
    mousey = 0 # 마우스이벤트 발생시 x좌표
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesDate(False)


    firstSelection = None #첫번째 상자를 클릭했을때 (x,y를 저장)

    DISPLAYSURF.fill(bgcolor)
    startGameAnimation(mainBoard)

    while True:
        mouserClicked = False

        DISPLAYSURF.fill(bgcolor) #윈도우를 그린다
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

                mouserClicked = True
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx != None and boxy != None:
                    if not revealedBoxes[boxx][boxy]:
                        drawHighlightBoxes(boxx,boxy)
                    if not revealedBoxes[boxx][boxy] and mouserClicked:
                        revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                        revealedBoxes[boxx][boxy] = True
                        if firstSelection == None:
                            firstSelection = (boxx,boxy)
                        else:
                            icon1shape, icon1color = getShapeAndColor(mainBoard,firstSelection[0], firstSelection[1])
                            icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                            if icon1shape != icon2shape or icon1color != icon2color:
                                #아이콘이 맞지 않을때, 상자를 모두 덮는다.
                                pygame.time.wait(1000)
                                coverBoxesAnimation(mainBoard, [(firstSelection[0],firstSelection[1]), (boxx,boxy)])
                                revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                                revealedBoxes[boxx][boxy] = False
                            elif hasWon(revealedBoxes):
                                gameWonAnimation(mainBoard)
                                pygame.time.wait(2000)


                                #게임판을 재설정한다.
                                mainBoard = getRandomizedBoard()
                                revealedBoxes = generateRevealedBoxesDate(False)

                                #잠시동안 게임판의 상자를 열어서 보여준다.
                                drawBoard(mainBoard, revealedBoxes)
                                pygame.display.update()
                                pygame.time.wait(1000)

                                #게임시작 애니메이션을 보여준다.
                                startGameAnimation(mainBoard)
                            firstSelection = None #firstSelection변수를 리셋한다.
                #화면을 다시 그린 다음 시간 지연을 기다린다.
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def generateRevealedBoxesDate(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    #모든 가능한 생에서 가능한 모양의 목록을 모두 얻어낸다.
    icons = []
    for color in allcolor:
        for shape in allshapes:
            icons.append((shape,color))

    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT /2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    #랜덤으로 아이콘이 놓여 있는 게임판의 데이터 구조를 만든다.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    #리스트를 2차원 리스트로 만든다. 안쪽의 리스트는 쵀대로 groupSize개 만큼의 아이템이 있다.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    #게임판 좌표계를 픽셀 좌표계로 변환한다.
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return(boxx,boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)


    left, top = leftTopCoordsOfBox(boxx,boxy)
    if shape == dount:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top+ half), half-5 )
        pygame.draw.circle(DISPLAYSURF, bgcolor, (left + half, top+half), quarter -5)
    elif shape == square:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE -half, BOXSIZE - half))
    elif shape == diamond:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left+ BOXSIZE - 1, top + half), (left + half, top + BOXSIZE -1), (left, top + half)))
    elif shape == lines:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF,color, (left + i, top + BOXSIZE - 1), (left+ BOXSIZE - 1, top +i))
    elif shape == oval:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def getShapeAndColor(board,boxx,boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:

        left, top  = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, bgcolor, (left, top, BOXSIZE, BOXSIZE))
        shape,color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, boxcolor, (left,top,coverage,BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) -1, -REVEALSPEED):
        drawBoxCovers(board,boxesToReveal,coverage)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0,BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board,revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF,boxcolor,(left,top,BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape,color, boxx, boxy)

def drawHighlightBoxes(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, highlightcolor, (left -5, top -5, BOXSIZE + 10, BOXSIZE + 10), 4)



def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesDate(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesDate(True)
    color1 = lightbgcolor
    color2 = bgcolor

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


if __name__ == '__main__':
    main()
