import pygame
import time

BGColor = (255, 255, 255)
fontColor = (0, 0, 0)
width = 1920
height = 1080

def initScreen() :
    global screen, clock

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MyTimer')

    clock = pygame.time.Clock()
    runScreen()


def fontInit(text, font) :
    textSurface = font.render(text, True, fontColor)
    return textSurface, textSurface.get_rect()

def updateTime() :
    global screen

    timeFont = pygame.font.Font('test_sans.ttf', 200)
    curTime = time.strftime('%H:%M:%S')
    TextSurf, TextRect = fontInit(curTime, timeFont)
    TextRect.center = ((width/2), (height/2))
    screen.blit(TextSurf, TextRect)


def runScreen() :
    global screen, clock

    crashed = False
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                crashed = True

        screen.fill(BGColor)
        updateTime()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()

initScreen()


