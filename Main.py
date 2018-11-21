# -*- coding: utf-8 -*-

import pygame
import time

curTime = time.gmtime(time.time())
BGColor = (0, 0, 0)
fontColor = (255, 255, 255)
width = 1920
height = 1080

def initScreen() :
    global screen, clock

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MyTimer')

    clock = pygame.time.Clock()
    runScreen()

def nowCalender():
    i = 0
    while True:
        calSec = getSec(readCalendar(i))
        curSec = (homeTime(curTime.tm_hour)*60+curTime.tm_min)*60+curTime.tm_sec     # UTC+9
        if calSec <= curSec:
            calSec = getSec(readCalendar(i+1))
            if curSec < calSec:
                return i+1      # Now Calendar index
        i += 1

def readCalendar(index):
    with open('data\\CalendarList.txt', 'rt', encoding='UTF8') as file:
        for i in range(index+1):
            calendar = file.readline()
            if i is index:
                calendar = calendar.replace('\ufeff', '')
                return calendar

def getSec(cal):
    splitedCal = cal.split()        # string to list
    calTime = splitedCal.pop()      # get last element
    splitedCalTime = calTime.split(':')     # split hour:min
    calHour = int(splitedCalTime[0])
    calMin = int(splitedCalTime[1])
    calSec = calHour*3600 + calMin*60
    return calSec

def getName(cal):
    splitedCal = cal.split()
    return splitedCal[0]

def homeTime(hour):
    hour += 9
    if hour > 24:
        hour -= 24
    return hour

def subTime(calTime):
    calSec = getSec(calTime)
    curSec = (homeTime(curTime.tm_hour) * 60 + curTime.tm_min) * 60 + curTime.tm_sec

    resultSec = calSec - curSec
    resultHour = resultSec // 3600
    resultSec = resultSec - (resultHour*3600)
    resultMin = resultSec // 60
    resultSec = resultSec - (resultMin*60)

    resultTime = str(resultHour) + ':' + str(resultMin) + ':' + str(resultSec)   # Hour:Min:Sec
    return resultTime


def fontInit(text, font):
    textSurface = font.render(text, True, fontColor)
    return textSurface, textSurface.get_rect()

def initName():
    global screen, nameFont

    nameFont = pygame.font.Font('data\\NanumPen.ttf', 200)

def initTime():
    global screen, timeFont

    timeFont = pygame.font.Font('data\\test_sans.ttf', 200)

def updateData():
    global screen, nameFont, timeFont

    calSec = readCalendar(nowCalender())
    remainderTime = subTime(calSec)        # subTime(hh:mm):(0~59)

    curCalName = getName(readCalendar(nowCalender()))

    screen.fill(BGColor)
    nameTextSurf, nameTextRect = fontInit(curCalName, nameFont)
    nameTextRect.center = ((width / 2), (height - 800))
    screen.blit(nameTextSurf, nameTextRect)

    timeTextSurf, timeTextRect = fontInit(remainderTime, timeFont)
    timeTextRect.center = ((width / 2), (height / 2))
    screen.blit(timeTextSurf, timeTextRect)

def runScreen():
    global curTime, screen, clock

    initName()
    initTime()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        curTime = time.gmtime(time.time())
        updateData()
        pygame.display.update()
        clock.tick(1)

    pygame.quit()

initScreen()