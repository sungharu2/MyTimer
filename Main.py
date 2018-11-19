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
    global curTime
    i = 0
    while True:
        calendarHour = getHour(readCalendar(i))
        calendarMin = getMin(readCalendar(i))
        calMins = calendarHour*60+calendarMin
        curMins = (curTime.tm_hour+9)*60+curTime.tm_min # UTC+9

        if calMins <= curMins:
            calendarHour = getHour(readCalendar(i+1))
            calendarMin = getMin(readCalendar(i+1))
            calMins = calendarHour*60+calendarMin

            if curMins < calMins:
                return i+2      # Now Calendar index
        i += 1

def readCalendar(index):
    global calendar
    with open('data\\CalendarList.txt', 'rt', encoding='UTF8') as file:
        for i in range(index+1):
            calendar = file.readline()
            if i is index:
                calendar = calendar.replace('\ufeff', '')
                return calendar

def getHour(cal):
    splitedCal = cal.split()
    calTime = splitedCal[1].split(':')
    hour = calTime[0]
    return int(hour)

def getMin(cal):
    splitedCal = cal.split()
    calTime = splitedCal[1].split(':')
    min = calTime[1]
    return int(min)

def getName(cal):
    splitedCal = cal.split()
    calName = splitedCal[0]
    return calName

def subTime(calTime):
    curTime = time.gmtime(time.time())
    calTime = calTime.split(':')
    calHour = calTime[0]
    calMin = calTime[1]
    curHour = curTime.tm_hour+9 # UTC+9
    if curHour > 24:
        curHour -= 24
    curMin = curTime.tm_min
    calResult = int(calHour)*60+int(calMin)
    curResult = curHour*60+curMin
    resultMin = calResult - curResult
    resultTime = str(resultMin//60) + ':' + str(resultMin%60)   # Hour : Min
    return resultTime

def fontInit(text, font):
    textSurface = font.render(text, True, fontColor)
    return textSurface, textSurface.get_rect()

def updateTime():
    global curTime, screen, curCalendar

    timeFont = pygame.font.Font('data\\test_sans.ttf', 200)
    nameFont = pygame.font.Font('data\\NanumPen.ttf', 200)

    with open('data\\CalendarList.txt', 'rt', encoding='UTF8') as file:
        for i in range(nowCalender()):
            curCalendar = file.readline()
    curCalendar = curCalendar.split()

    curCalName = curCalendar[0]
    curCalTime = curCalendar[1]
    remainderTime = subTime(curCalTime) + ':' + str(60-int(time.time()%60+1))   # subTime(hh:mm):(0~59)

    timeTextSurf, timeTextRect = fontInit(remainderTime, timeFont)
    timeTextRect.center = ((width/2), (height/2))
    screen.blit(timeTextSurf, timeTextRect)

    nameTextSurf, nameTextRect = fontInit(curCalName, nameFont)
    nameTextRect.center = ((width/2), (height-800))
    screen.blit(nameTextSurf, nameTextRect)

def runScreen():
    global curTime, screen, clock

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        curTime = time.gmtime(time.time())
        screen.fill(BGColor)
        updateTime()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

initScreen()