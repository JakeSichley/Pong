# import pygame
from classes import *
from pygame.locals import *
import sys

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Set up window
WINDOWWIDTH = 800
WINDOWHEIGHT = 450
FULLHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, FULLHEIGHT), 0, 32)
pygame.display.set_caption('Pong')

# Set up background
gameBackgroundImage = pygame.image.load('Resources\\completeBackground.png')
gameBackgroundRect = pygame.Rect(0, 0, 800, 450)

# Set up game constants
BLACK = (0, 0, 0)
MOVESPEED = 5
CMOVESPEED = 3
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
collisionCheckCounter = 0

# Set up score
score = ScoreManager()

# Set up ball
ball = Ball('Resources\\ball.png', int(WINDOWWIDTH / 2) - 10, int(WINDOWHEIGHT / 2))

# Player paddles
playerPaddleTop = PlayerPaddle('Resources\\bluePaddleH.png', int(WINDOWWIDTH * .75) - 20, 0, 'H')
playerPaddleSide = PlayerPaddle('Resources\\bluePaddleV.png', WINDOWWIDTH - 9, int(WINDOWHEIGHT / 2) - 20, 'V')
playerPaddleBottom = PlayerPaddle('Resources\\bluePaddleH.png', int(WINDOWWIDTH * .75) - 20, WINDOWHEIGHT - 9, 'H')

# Computer paddles
compPaddleTop = ComputerPaddle('Resources\\redPaddleH.png', int(WINDOWWIDTH / 4) - 20, 0, 'H')
compPaddleSide = ComputerPaddle('Resources\\redPaddleV.png', 0, int(WINDOWHEIGHT / 2) - 20, 'V')
compPaddleBottom = ComputerPaddle('Resources\\redPaddleH.png', int(WINDOWWIDTH / 4) - 20, WINDOWHEIGHT - 9, 'H')

# Create list of paddles
playerPaddles = [playerPaddleTop, playerPaddleSide, playerPaddleBottom]
compPaddles = [compPaddleTop, compPaddleSide, compPaddleBottom]
invalidPaddles = []

# Set up SoundManager
SoundManager.getinstance().startgame()
roundStart = True

score.debug_setscore([10, 7])

while True:
    # Clear and re-blit background
    windowSurface.fill(BLACK)
    windowSurface.blit(gameBackgroundImage, gameBackgroundRect)
    windowSurface.blit(ball.getimage(), ball.getrect())
    score.displayscore(windowSurface)

    if roundStart:
        playerPaddleTop.resetposition(int(WINDOWWIDTH * .75) - 20, 0)
        playerPaddleSide.resetposition(WINDOWWIDTH - 9, int(WINDOWHEIGHT / 2) - 20)
        playerPaddleBottom.resetposition(int(WINDOWWIDTH * .75) - 20, WINDOWHEIGHT - 9)
        compPaddleTop.resetposition(int(WINDOWWIDTH / 4) - 20, 0)
        compPaddleSide.resetposition(0, int(WINDOWHEIGHT / 2) - 20)
        compPaddleBottom.resetposition(int(WINDOWWIDTH / 4) - 20, WINDOWHEIGHT - 9)

    for paddle in playerPaddles:
        windowSurface.blit(paddle.getimage(), paddle.getrect())

    for paddle in compPaddles:
        windowSurface.blit(paddle.getimage(), paddle.getrect())

    if roundStart:
        pygame.display.update()
        SoundManager.getinstance().threadedsound(SoundManager.getinstance().startround)
        pygame.event.clear()
        moveLeft = False
        moveRight = False
        moveUp = False
        moveDown = False
        roundStart = False

    ball.move(WINDOWWIDTH, WINDOWHEIGHT)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False

    if moveDown:
        playerPaddleSide.movedown(WINDOWHEIGHT, MOVESPEED)
    if moveUp:
        playerPaddleSide.moveup(MOVESPEED)
    if moveLeft:
        playerPaddleTop.moveleft(WINDOWWIDTH, MOVESPEED)
        playerPaddleBottom.moveleft(WINDOWWIDTH, MOVESPEED)
    if moveRight:
        playerPaddleTop.moveright(WINDOWWIDTH, MOVESPEED)
        playerPaddleBottom.moveright(WINDOWWIDTH, MOVESPEED)

    compPaddleTop.movehorizontal(WINDOWWIDTH, CMOVESPEED, ball.getrect())
    compPaddleBottom.movehorizontal(WINDOWWIDTH, CMOVESPEED, ball.getrect())
    compPaddleSide.movevertical(WINDOWHEIGHT, CMOVESPEED, ball.getrect())

    for paddle in invalidPaddles:
        paddle[1] += 1
        if paddle[1] == 5:
            paddle[0].setvalid(True)
            invalidPaddles.remove(paddle)

    if ball.getcollisionpending():
        for paddle in playerPaddles:
            if paddle.getrect().colliderect(ball.getrect()) and paddle.getvalid():
                if paddle.gettype() == 'H':
                    SoundManager.getinstance().hitsound()
                    ball.hitvertical()
                    invalidPaddles.append([paddle, 0])
                    paddle.setvalid(False)
                    collisionCheckCounter = 0
                    break
                else:
                    SoundManager.getinstance().hitsound()
                    ball.hithorizontal()
                    invalidPaddles.append([paddle, 0])
                    paddle.setvalid(False)
                    collisionCheckCounter = 0
                    break

        for paddle in compPaddles:
            if paddle.getrect().colliderect(ball.getrect()) and paddle.getvalid():
                if paddle.gettype() == 'H':
                    SoundManager.getinstance().hitsound()
                    ball.hitvertical()
                    invalidPaddles.append([paddle, 0])
                    paddle.setvalid(False)
                    collisionCheckCounter = 0
                    break
                else:
                    SoundManager.getinstance().hitsound()
                    ball.hithorizontal()
                    invalidPaddles.append([paddle, 0])
                    paddle.setvalid(False)
                    collisionCheckCounter = 0
                    break

    if collisionCheckCounter == 2:
        if ball.getrect().centerx < int(WINDOWWIDTH / 2):
            score.playerscored(SoundManager.getinstance())
        else:
            score.computerscored(SoundManager.getinstance())
        ball = Ball('Resources\\ball.png', int(WINDOWWIDTH / 2) - 10, int(WINDOWHEIGHT / 2))
        collisionCheckCounter = 0
        roundStart = True

    if ball.getcollisionpending():
        collisionCheckCounter += 1

    pygame.display.update()
    mainClock.tick(40)
