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
        calendarHour = getHour(readCalendar(i))
        calendarMin = getMin(readCalendar(i))
        calSecs = (calendarHour*60+calendarMin)*60
        curSecs = ((curTime.tm_hour+9)*60+curTime.tm_min)*60+curTime.tm_sec     # UTC+9

        if calSecs <= curSecs:
            calendarHour = getHour(readCalendar(i+1))
            calendarMin = getMin(readCalendar(i+1))
            calSecs = (calendarHour * 60 + calendarMin) * 60

            if curSecs < calSecs:
                return i+1      # Now Calendar index
        i += 1

def readCalendar(index):
    with open('data\\CalendarList.txt', 'rt', encoding='UTF8') as file:
        for i in range(index+1):
            calendar = file.readline()
            if i is index:
                calendar = calendar.replace('\ufeff', '')
                return calendar

def getTime(cal):
    cal = cal.split()
    return cal.pop()

def getHour(cal):
    calTime = getTime(cal)
    splitedCal = calTime.split(':')
    hour = splitedCal[0]
    return int(hour)

def getMin(cal):
    calTime = getTime(cal)
    splitedCal = calTime.split(':')
    min = splitedCal[1]
    return int(min)

def getName(cal):
    splitedCal = cal.split()
    return splitedCal[0]

def subTime(calTime, curTime):
    calHour = getHour(calTime)
    calMin = getMin(calTime)
    curHour = getHour(curTime)
    curMin = getMin(curTime)

    curHour += 9 # UTC+9
    if curHour > 24:
        curHour -= 24
    calResult = calHour*60+calMin
    curResult = curHour*60+curMin
    resultMin = calResult - curResult
    resultTime = str(resultMin//60) + ':' + str(resultMin%60)   # Hour : Min
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

    curTime = time.gmtime(time.time())
    calTime = getTime(readCalendar(nowCalender()))
    remainderTime = subTime(calTime, str(curTime.tm_hour) + ':' + str(curTime.tm_min)) + ':' + \
                    str(60 - int(curTime.tm_sec % 60 + 1))  # subTime(hh:mm):(0~59)

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

        updateData()
        pygame.display.update()
        clock.tick(1)
        print("tick")

    pygame.quit()

initScreen()