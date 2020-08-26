'''
This is a snake game ported from GamerGorl Project to Wio Terminal(ArduPy). For more information, please also visit: https://github.com/bpwagner/GamerGorl

Author: Anson He(Seeed Studio)
'''

import time
import random
from machine import LCD, Pin, Map, DAC
from machine import Sprite

# LCD setup
lcd = LCD()
spr = Sprite(lcd)

# Pins setup
LEFT = Pin(Map.WIO_5S_LEFT, Pin.IN, Pin.PULL_UP)
RIGHT = Pin(Map.WIO_5S_RIGHT, Pin.IN, Pin.PULL_UP)
UP = Pin(Map.WIO_5S_UP, Pin.IN, Pin.PULL_UP)
DOWN = Pin(Map.WIO_5S_DOWN, Pin.IN, Pin.PULL_UP)
APressed = Pin(Map.WIO_KEY_C, Pin.IN, Pin.PULL_UP)
BPressed = Pin(Map.WIO_KEY_A, Pin.IN, Pin.PULL_UP)
BUZZER = DAC(Pin(Map.WIO_BUZZER))

# Game size
gameW = 220
gameH = 150

def showHighscore(score, highscore):
    time.sleep(0.2)
    spr.fillScreen(lcd.color.BLACK)
    spr.drawString("SCORE: " + str(score), 0, 0)
    spr.drawString("HIGHSCORE: " + str(highscore), 0, 10)
    spr.drawString("PLAY AGAIN?", 20, 30)
    spr.drawString("YES[A]", 10, 45)
    spr.drawString("NO[B]", 80, 45)
    spr.pushSprite(50,45)

# update snake
def showBoard(fruitPoint, segments, dots):
    spr.createSprite(gameW, gameH) # buffer
    spr.fillScreen(lcd.color.BLACK)
    spr.drawRoundRect(0, 0 , gameW, gameH, 5, lcd.color.WHITE) # Board Frame

    spr.fillRect(fruitPoint[0], fruitPoint[1], 5, 5 ,random.randint(0,65535)) # Random colour fruit

    for i in range(0, dots):
        spr.fillRect(segments[i][0], segments[i][1], 5, 5, lcd.color.GREEN) # SNAKE
        # print(segments[i][0], segments[i][1])
    spr.pushSprite(50,45)
    

print("SETUP DONE")

def main():
    lcd.fillScreen(lcd.color.BLACK)
    lcd.setTextSize(2)
    lcd.setTextColor(lcd.color.WHITE)
    lcd.drawString("ArduPy Snakes", 85, 10)

    playagain = True
    f = open("snakehighscore", 'r')
    highscore = int(f.readline())
    f.close()
    playagain = True

    while playagain:
        # snake game setup
        dotSize = 5
        score = 0
        gameOver = False
        loopDelay = 50
        dots = 3

        fruitPoint = (random.randint(1,11)*10, random.randint(1,5)*5) # generate random fruit point
        segments = []

        # snake directions
        leftDirection = False
        rightDirection = False
        upDirection = False
        downDirection = False

        # add snake segments
        for i in range(0, dots):
            segments.append((50 - i * dotSize, 50))
        # print(segments)

        while not gameOver:
            # print(fruitPoint[0], fruitPoint[1])
            if segments[0][0] == fruitPoint[0] and segments[0][1] == fruitPoint[1]:
                segments.append((0,0))
                dots = dots + 1
                fruitPoint = (random.randint(1,11)*10, random.randint(1,5)*5) # generate random fruit point
                score += 1                
                BUZZER.write(64) # Beep
                time.sleep_ms(20)
                BUZZER.write(0)

            # wall collision
            if segments[0][0] == 0 or segments[0][0] == (gameW-5) or segments[0][1] == 0 or segments[0][1] == (gameH-5):
                gameOver = True

            # check snake
            if LEFT.value() == 0:
                leftDirection = True
                rightDirection = False
                upDirection = False
                downDirection = False

            elif RIGHT.value() == 0:
                leftDirection = False
                rightDirection = True
                upDirection = False
                downDirection = False

            elif UP.value() == 0:
                leftDirection = False
                rightDirection = False
                upDirection = True
                downDirection = False

            elif DOWN.value() == 0:
                leftDirection = False
                rightDirection = False
                upDirection = False
                downDirection = True

            # the body
            time.sleep_ms(10) # small delay to slow down the snake
            for i in range(dots - 1, 0, -1):
                segments[i] = (segments[(i - 1)][0], segments[(i - 1)][1])

            # the head
            if leftDirection:
                segments[0] = (segments[0][0] - dotSize, segments[0][1])

            if rightDirection:
                segments[0] = (segments[0][0] + dotSize, segments[0][1])

            if upDirection:
                segments[0] = (segments[0][0], segments[0][1] - dotSize)

            if downDirection:
                segments[0] = (segments[0][0], segments[0][1] + dotSize)

            showBoard(fruitPoint, segments, dots)
            time.sleep(0.05)

        if score > highscore:
            highscore = score
            f = open("snakehighscore", "w")
            f.write(str(highscore))
            f.close()

        state = True
        showHighscore(score, highscore)
        time.sleep(0.2)

        while state:
            if APressed.value() == 0:
                playagain = True
                state = False
            if BPressed.value() == 0:
                playagain = False
                state = False
                time.sleep(0.2)

while True:
    main()