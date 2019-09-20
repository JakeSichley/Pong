import pygame
from pygame.locals import *
from math import *
import random
import sys
import threading


class PlayerPaddle:
    def __init__(self, image, left, top, alignment):
        self.__image = pygame.image.load(image)
        self.__rect = pygame.Rect(left, top, self.__image.get_size()[0], self.__image.get_size()[1])
        self.__type = alignment
        self.__valid = True

    def resetposition(self, left, top):
        self.__rect = pygame.Rect(left, top, self.__image.get_size()[0], self.__image.get_size()[1])

    def getvalid(self):
        return self.__valid

    def setvalid(self, valid):
        self.__valid = valid

    def getimage(self):
        return self.__image

    def getrect(self):
        return self.__rect

    def gettype(self):
        return self.__type

    def movedown(self, windowheight, movespeed):
        if self.__rect.bottom < windowheight:
            self.__rect.top += movespeed

    def moveup(self, movespeed):
        if self.__rect.top > 0:
            self.__rect.top -= movespeed

    def moveleft(self, windowwidth, movespeed):
        if self.__rect.left > int(windowwidth / 2):
            self.__rect.left -= movespeed

    def moveright(self, windowwidth, movespeed):
        if self.__rect.right < windowwidth:
            self.__rect.left += movespeed


class ComputerPaddle:
    def __init__(self, image, left, top, alignment):
        self.__image = pygame.image.load(image)
        self.__rect = pygame.Rect(left, top, self.__image.get_size()[0], self.__image.get_size()[1])
        self.__type = alignment
        self.__valid = True

    def resetposition(self, left, top):
        self.__rect = pygame.Rect(left, top, self.__image.get_size()[0], self.__image.get_size()[1])

    def getvalid(self):
        return self.__valid

    def setvalid(self, valid):
        self.__valid = valid

    def getimage(self):
        return self.__image

    def getrect(self):
        return self.__rect

    def gettype(self):
        return self.__type

    def movehorizontal(self, windowwidth, movespeed, ball):
        if ball.right < self.__rect.left + 20:
            self.__moveleft(movespeed)
        elif ball.left > self.__rect.right - 20:
            self.__moveright(windowwidth, movespeed)

    def movevertical(self, windowheight, movespeed, ball):
        if ball.top < self.__rect.top:
            self.__moveup(movespeed)
        elif ball.bottom > self.__rect.bottom:
            self.__movedown(windowheight, movespeed)

    def __movedown(self, windowheight, movespeed):
        if self.__rect.bottom < windowheight:
            self.__rect.top += movespeed

    def __moveup(self, movespeed):
        if self.__rect.top > 0:
            self.__rect.top -= movespeed

    def __moveleft(self, movespeed):
        if self.__rect.left > 0:
            self.__rect.left -= movespeed

    def __moveright(self, windowwidth, movespeed):
        if self.__rect.right < int(windowwidth / 2) - 5:
            self.__rect.left += movespeed


class Ball:
    def __init__(self, image, left, top):
        self.__image = pygame.image.load(image)
        self.__rect = pygame.Rect(left, top, self.__image.get_size()[0], self.__image.get_size()[1])
        self.__collisionPending = False
        # Set up x and y movement
        movespeed = random.randint(6, 10)
        angle = random.randint(20, 55)
        self.__velocities = [int(movespeed * cos(radians(angle))), int(movespeed * sin(radians(angle)))]
        if random.randint(0, 1) == 0:
            self.__velocities[0] *= -1
        if random.randint(0, 1) == 0:
            self.__velocities[1] *= -1

    def getimage(self):
        return self.__image

    def getrect(self):
        return self.__rect

    def getvelocities(self):
        return self.__velocities

    def getcollisionpending(self):
        return self.__collisionPending

    def move(self, windowwidth, windowheight):
        self.__rect.left += self.__velocities[0]
        self.__rect.top += self.__velocities[1]
        self.__prepareforcollision(windowwidth, windowheight)

    def __prepareforcollision(self, windowwidth, windowheight):
        if self.__rect.left < 0:
            self.__rect.left = 0
            self.__collisionPending = True
        elif self.__rect.right > windowwidth:
            self.__rect.right = windowwidth
            self.__collisionPending = True

        if self.__rect.top < 0:
            self.__rect.top = 0
            self.__collisionPending = True
        elif self.__rect.bottom > windowheight:
            self.__rect.bottom = windowheight
            self.__collisionPending = True

    def hithorizontal(self):
        self.__velocities[0] *= -1
        self.__collisionPending = False

    def hitvertical(self):
        self.__velocities[1] *= -1
        self.__collisionPending = False


# Singleton class SoundManager
class SoundManager:
    __instance = None

    @staticmethod
    def getinstance():
        # Static access
        if SoundManager.__instance is None:
            SoundManager()
        return SoundManager.__instance

    def __init__(self):
        if SoundManager.__instance is not None:
            raise Exception("Instance already exists")
        else:
            SoundManager.__instance = self
            pygame.mixer.init(buffer=16)
            self.__announcerThree = pygame.mixer.Sound('Resources\\three.wav')
            self.__announcerThree.set_volume(0.25)
            self.__announcerTwo = pygame.mixer.Sound('Resources\\two.wav')
            self.__announcerTwo.set_volume(0.25)
            self.__announcerOne = pygame.mixer.Sound('Resources\\one.wav')
            self.__announcerOne.set_volume(0.25)
            self.__hitSound = pygame.mixer.Sound('Resources\\hitsound.wav')
            self.__hitSound.set_volume(0.25)
            self.__roundWon = pygame.mixer.Sound('Resources\\roundwon.wav')
            self.__roundWon.set_volume(0.25)
            self.__roundLost = pygame.mixer.Sound('Resources\\roundlost.wav')
            self.__roundLost.set_volume(0.25)
            self.__playerwonround = pygame.mixer.Sound('Resources\\playerwinstheround.wav')
            self.__playerwonround.set_volume(0.15)
            self.__computerwonround = pygame.mixer.Sound('Resources\\computerwinstheround.wav')
            self.__computerwonround.set_volume(0.15)
            self.__newroundin = pygame.mixer.Sound('Resources\\newroundin.wav')
            self.__newroundin.set_volume(0.15)
            pygame.mixer.music.load('Resources\\music.ogg')
            self.__musicPlaying = False

    def startgame(self):
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.1)
        self.__musicPlaying = True

    def startround(self):
        self.__announcerThree.play()
        pygame.time.wait(1300)
        self.__announcerTwo.play()
        pygame.time.wait(1300)
        self.__announcerOne.play()
        pygame.time.wait(1300)

    @staticmethod
    def threadedsound(function):
        thread = threading.Thread(target=function, args=(), daemon=True)
        thread.start()

        # Threading the sound function to allow exiting of the game
        # Sound functions 'lock' the window with .wait()
        while thread.is_alive():
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def hitsound(self):
        self.__hitSound.play()

    def roundwon(self):
        self.__roundWon.play()
        pygame.time.wait(3000)

    def roundlost(self):
        self.__roundLost.play()
        pygame.time.wait(3000)

    def playerwonround(self):
        self.__playerwonround.play()
        pygame.time.wait(3000)
        self.__newroundin.play()
        pygame.time.wait(2000)

    def computerwonround(self):
        self.__computerwonround.play()
        pygame.time.wait(3000)
        self.__newroundin.play()
        pygame.time.wait(2000)


# round -> game -> match
class ScoreManager:
    def __init__(self):
        self.__roundScores = [0, 0]
        self.__matches = [0, 0]

    def debug_setscore(self, scores):
        self.__roundScores = scores

    def computerscored(self, soundmanager):
        self.__roundScores[0] += 1
        soundmanager.threadedsound(soundmanager.roundlost)
        self.__checkforcomputerwonround(soundmanager)

    def playerscored(self, soundmanager):
        self.__roundScores[1] += 1
        soundmanager.threadedsound(soundmanager.roundwon)
        self.__checkforplayerwonround(soundmanager)

    def __checkforcomputerwonround(self, soundmanager):
        if self.__roundScores[0] > self.__roundScores[1] and self.__roundScores[0] >= 11 and\
           self.__roundScores[0] - self.__roundScores[1] >= 2:
            self.__matches[0] += 1
            self.__endroundcomputer(soundmanager)

    def __checkforplayerwonround(self, soundmanager):
        if self.__roundScores[1] > self.__roundScores[0] and self.__roundScores[1] >= 11 and\
           self.__roundScores[1] - self.__roundScores[0] >= 2:
            self.__matches[1] += 1
            self.__endroundplayer(soundmanager)

    def __endroundcomputer(self, soundmanager):
        self.__roundScores = [0, 0]
        soundmanager.threadedsound(soundmanager.computerwonround)

    def __endroundplayer(self, soundmanager):
        self.__roundScores = [0, 0]
        soundmanager.threadedsound(soundmanager.playerwonround)

    def displayscore(self, windowsurface):
        # Computer Score
        font = pygame.font.Font('Resources\\gameover.ttf', 60)
        text = 'Round: ' + str(self.__roundScores[0]) + '     Match: ' + str(self.__matches[0])
        textsurface = font.render(text, True, (255, 255, 255))
        textrect = textsurface.get_rect()
        textrect.center = (125, 475)
        windowsurface.blit(textsurface, textrect)
        # Player Score
        text = 'Round: ' + str(self.__roundScores[1]) + '     Match: ' + str(self.__matches[1])
        textsurface = font.render(text, True, (255, 255, 255))
        textrect = textsurface.get_rect()
        textrect.center = (675, 475)
        windowsurface.blit(textsurface, textrect)
        # Score Needed
        neededscores = [self.__getpointsneededforwin(self.__roundScores[0], self.__roundScores[1]),
                        self.__getpointsneededforwin(self.__roundScores[1], self.__roundScores[0])]
        scoreneeded = neededscores[0] if neededscores[0] > neededscores[1] else neededscores[1]
        text = 'Round Point at: ' + str(scoreneeded)
        textsurface = font.render(text, True, (255, 255, 255))
        textrect = textsurface.get_rect()
        textrect.center = (400, 475)
        windowsurface.blit(textsurface, textrect)

    @staticmethod
    def __getpointsneededforwin(scorea, scoreb):
        if scorea < 9:
            return 11
        elif scorea > scoreb:
            return scoreb + 2
        else:
            return scorea + (2 - abs(scorea - scoreb))


class Paddle:
    def __init__(self, image, left, top):
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(left, top, self.image.get_size()[0], self.image.get_size()[1])
