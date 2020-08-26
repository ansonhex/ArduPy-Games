import time, random
from machine import LCD, Sprite, Pin, Map

lcd = LCD()
spr = Sprite(lcd)

# Pins setup
LEFT = Pin(Map.WIO_5S_LEFT, Pin.IN, Pin.PULL_UP)
RIGHT = Pin(Map.WIO_5S_RIGHT, Pin.IN, Pin.PULL_UP)
UP = Pin(Map.WIO_5S_UP, Pin.IN, Pin.PULL_UP)
DOWN = Pin(Map.WIO_5S_DOWN, Pin.IN, Pin.PULL_UP)
APressed = Pin(Map.WIO_KEY_C, Pin.IN, Pin.PULL_UP)
BPressed = Pin(Map.WIO_KEY_A, Pin.IN, Pin.PULL_UP)

def newNum(board):
    xrand = random.randint(0, 3)
    yrand = random.randint(0, 3)
    while(board[xrand][yrand] > 0):
        xrand = random.randint(0, 3)
        yrand = random.randint(0, 3)
    board[xrand][yrand] = random.randint(1, 2)

def showBoard(board):
    spr.createSprite(220, 100) # 2048 game size
    spr.fillScreen(lcd.color.BLACK)
    spr.setTextSize(3)
    x = 20
    y = 2
    spaceing = 25
    global max
    max = 0
    for r in board:
        for c in r:
            if c > max:
                max = c
                time.sleep_ms(20)
            # print(c, end=" ")
            if c == -1:
                spr.drawString("_   ", x, y)
            else:
                spr.drawString(str(c), x, y)
            x += spaceing
        x = 20
        y += spaceing

    spr.drawRect(18,0,58,58,1)
    spr.setTextColor(lcd.color.GREEN)
    spr.drawString("Score", 130, 22)
    spr.setTextColor(lcd.color.WHITE)
    spr.drawString(str(max*max), 130, 52)
    spr.pushSprite(50, 70) # Target point to push sprite

def isGameOver(board):
    for r in range(0, 3):
        for c in range(0, 3):
            if board[r][c] < 0:
                return False
    return True

def goRight(board):
    repeat = True
    while repeat:
        repeat = False
        for r in range(0,4):
            for c in range(0,3):
                if board[r][c] > 0:
                    if board[r][c+1] < 0:
                        board[r][c+1] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r][c+1]:
                        board[r][c + 1] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board)

def goLeft(board):
    repeat = True
    while repeat:
        repeat = False
        for r in range(0,4):
            for c in range(3,0,-1):
                if board[r][c] > 0:
                    if board[r][c-1] < 0:
                        board[r][c-1] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r][c-1]:
                        board[r][c-1] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board)

def goDown(board):
    repeat = True
    while repeat:
        repeat = False
        for c in range(0,4):
            for r in range(0,3):
                if board[r][c] > 0:
                    if board[r+1][c] < 0:
                        board[r+1][c] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r+1][c]:
                        board[r+1][c] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board)


def goUp(board):
    repeat = True
    while repeat:
        repeat = False
        for c in range(0,4):
            for r in range(3,0,-1):
                if board[r][c] > 0:
                    if board[r-1][c] < 0:
                        board[r-1][c] = board[r][c]
                        board[r][c] = -1
                        repeat = True
                    elif board[r][c] == board[r-1][c]:
                        board[r-1][c] = board[r][c]+1
                        board[r][c] = -1
                        repeat = True
                    showBoard(board)

def main():
    board = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
    newNum(board)
    lcd.setTextSize(3)
    lcd.fillScreen(lcd.color.BLACK)
    lcd.drawString("ArduPy 2048", 65, 10)
    showBoard(board)

    while (not isGameOver(board)):
        if RIGHT.value() == 0:
            goRight(board)
        elif LEFT.value() == 0:
            goLeft(board)
        elif DOWN.value() == 0:
            goDown(board)
        elif UP.value() == 0:
            goUp(board)
        
        newNum(board)
        showBoard(board)
        
        time.sleep_ms(200)
    
    # Game is over
    lcd.fillScreen(lcd.color.BLACK)
    lcd.setTextSize(3)
    lcd.setTextColor(lcd.color.RED)
    lcd.drawString("Game Over", 10, 10)
    lcd.setTextColor(lcd.color.WHITE)
    lcd.drawString(str(max*max), 10, 40)

while True:
    main()
    time.sleep_ms(4000)