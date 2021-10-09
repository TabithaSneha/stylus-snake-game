import cv2 as cv
import numpy as np
import pygame
import sys
import time
import random
import os

img_counter = 0
H = [0, 0, 0]
p = [0, 0, 0]
c = 0

# Creating a window to position and capture the Stylus
cam = cv.VideoCapture(0)
while True:
    ret, frame = cam.read()
    frame = cv.flip(frame, 1)
    frame = cv.putText(frame, 'Position the rectangle within the Stylus', (1, 110), cv.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    frame = cv.putText(frame, 'Press ESC', (240,380), cv.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    cv.rectangle(frame, (315,235), (325,245), (255,255,255), 2)
    cv.imshow("Capturing Stylus", frame)
    cv.moveWindow("Capturing Stylus", 100, 100)

    k = cv.waitKey(1)
    if k % 256 == 27:
        break

# Capturing the pixels in the Region of Interest
img = frame[235:245, 315:325]
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# Taking the average of HSV values of those pixels
for i in range(0, 10):
    for j in range(0, 10):
        if img[i, j][0] != 0:
            H = H + img[i, j]
            c = c + 1
p = H//c

cam.release()
cv.destroyAllWindows()


cap = cv.VideoCapture(0)
cx1 = 0
cy1 = 0


# Capturing the centroid of the Stylus using HSV Thresholding
def vdp():
    while 1:
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Setting the upper and lower HSV limits
        lower = np.array([p[0] - 10, p[1] - 50, p[2] - 50])
        upper = np.array([p[0] + 10, p[1] + 50, p[2] + 50])

        mask = cv.inRange(hsv, lower, upper)

        # Reducing noise in the mask image
        kernel = np.ones((11,11), np.uint8)
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
        blur = cv.GaussianBlur(opening, (5, 5), 0)

        ret1, thresh = cv.threshold(blur, 127,255,0)

        # Finding the contours of the Stylus
        contours, hierarchy = cv.findContours(thresh, 1, 2)

        # Displaying the Stylus Frame
        frame = cv.line(frame, (0, 0), (640, 480), (0, 0, 0), 5)
        frame = cv.line(frame, (0, 480), (640, 0), (0, 0, 0), 5)
        frame = cv.putText(frame, 'RIGHT', (485, 250), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        frame = cv.putText(frame, 'LEFT', (100, 250), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        frame = cv.putText(frame, 'UP', (300, 120), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        frame = cv.putText(frame, 'DOWN', (280, 390), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

        cv.imshow('Stylus Frame', frame)
        cv.moveWindow("Stylus Frame", 100, 100)

        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break

        # Calculating the centroid coordinates
        if len(contours) > 0:
            cnt = contours[0]
            M = cv.moments(cnt)
            cx1 = int(M['m10'] / M['m00'])
            cy1 = int(M['m01'] / M['m00'])
            return cx1, cy1


# Function to calculate area of triangles
def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


# Function to check if the given point lies within a triangle region
def check_region(x1, y1, x2, y2, x3, y3, cx, cy):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(cx, cy, x2, y2, x3, y3)
    A2 = area(x1, y1, cx, cy, x3, y3)
    A3 = area(x1, y1, x2, y2, cx, cy)
    if A == (A1 + A2 + A3):
        return True
    else:
        return False


# Obtaining centroid coordinate and checking its triangle region
cx, cy = vdp()
up = check_region(0, 0, 320, 240, 640, 0, cx, cy)
down = check_region(0, 480, 320, 240, 640, 480, cx, cy)
left = check_region(0, 0, 320, 240, 0, 480, cx, cy)
right = check_region(640, 0, 320, 240, 640, 480, cx, cy)

# Window size
window_w = 640
window_h = 480

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (780, 130)
pygame.init()

# Initialising game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_w, window_h))

# Defining colours
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(247, 42, 27)
obsc = pygame.Color(110, 15, 45)

# FPS controller
clock = pygame.time.Clock()

# Game variables
snake_pos = [window_w / 2 - 10, window_h / 2 - 10]
snake_body = [[window_w / 2 - 10, window_h / 2 - 10]]

food_pos = [random.randrange(1, ((window_w-10)//10)) * 10, random.randrange(7, ((window_h-10)//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Function for Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over!', True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_w / 2, window_h / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, white, 'times', 40)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Function to display Score at the top
def show_score(choice, color, font, size):
    pygame.draw.rect(game_window, (224, 224, 204), pygame.Rect(0, 0, window_w, 60))
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_w / 10, 15)
    else:
        score_rect.midtop = (window_w / 2, window_h / 1.25)
    game_window.blit(score_surface, score_rect)


# Functions for generating 5 obstacles
def obstacle_1():
    pygame.draw.rect(game_window, obsc, pygame.Rect(350, 140, 200, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(100, 240, 200, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(350, 340, 200, 20))


def obstacle_2():
    pygame.draw.rect(game_window, obsc, pygame.Rect(100, 140, 20, 130))
    pygame.draw.rect(game_window, obsc, pygame.Rect(120, 140, 120, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(400, 260, 20, 130))
    pygame.draw.rect(game_window, obsc, pygame.Rect(420, 370, 120, 20))


def obstacle_3():
    pygame.draw.rect(game_window, obsc, pygame.Rect(100, 280, 120, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(220, 280, 20, 130))
    pygame.draw.rect(game_window, obsc, pygame.Rect(400, 100, 20, 130))
    pygame.draw.rect(game_window, obsc, pygame.Rect(420, 210, 120, 20))


def obstacle_4():
    pygame.draw.rect(game_window, obsc, pygame.Rect(100, 140, 200, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(280, 160, 20, 120))
    pygame.draw.rect(game_window, obsc, pygame.Rect(300, 260, 200, 20))
    pygame.draw.rect(game_window, obsc, pygame.Rect(480, 280, 20, 100))


def obstacle_5():
    pygame.draw.rect(game_window, obsc, pygame.Rect(130, 130, 100, 100))
    pygame.draw.rect(game_window, obsc, pygame.Rect(420, 290, 100, 100))


ob = random.choice([0,1,2,3,4])

# Main Snake Game logic
while True:
    up = check_region(0, 0, 320, 240, 640, 0, cx, cy)
    down = check_region(0, 480, 320, 240, 640, 480, cx, cy)
    left = check_region(0, 0, 320, 240, 0, 480, cx, cy)
    right = check_region(640, 0, 320, 240, 640, 480, cx, cy)

    if up:
        change_to = 'UP'
    if down:
        change_to = 'DOWN'
    if left:
        change_to = 'LEFT'
    if right:
        change_to = 'RIGHT'

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, ((window_w - 10) // 10)) * 10,
                    random.randrange(7, ((window_h - 10) // 10)) * 10]
    food_spawn = True

    # Displaying the Game Screen
    game_window.fill((206, 245, 66))
    if ob == 0:
        obstacle_1()
    elif ob == 1:
        obstacle_2()
    elif ob == 2:
        obstacle_3()
    elif ob == 3:
        obstacle_4()
    else:
        obstacle_5()

    pygame.draw.line(game_window, (245, 102, 66), (0, 64), (640, 64), 10)
    pygame.draw.line(game_window, (245, 102, 66), (4, 65), (4, 480), 10)
    pygame.draw.line(game_window, (245, 102, 66), (0, 475), (640, 475), 10)
    pygame.draw.line(game_window, (245, 102, 66), (634, 65), (634, 480), 10)

    # Snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions:-
    # Getting out of bounds
    if snake_pos[0] < 10 or snake_pos[0] > window_w - 20:
        game_over()
        break
    if snake_pos[1] < 70 or snake_pos[1] > window_h - 20:
        game_over()
        break

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
            break

    # Touching the obstacles
    if ob == 0:
        if (340 < snake_pos[0] < 550 and 130 < snake_pos[1] < 160) or (90 < snake_pos[0] < 300 and 230 < snake_pos[1] < 260) or (340 < snake_pos[0] < 550 and 330 < snake_pos[1] < 360):
            food_spawn = True
            game_over()
            break
    elif ob == 1:
        if (90 < snake_pos[0] < 120 and 130 < snake_pos[1] < 270) or (
                110 < snake_pos[0] < 240 and 130 < snake_pos[1] < 160) or (
                390 < snake_pos[0] < 420 and 250 < snake_pos[1] < 390) or (410 < snake_pos[0] < 540 and 360 < snake_pos[1] < 390):
            food_spawn = True
            game_over()
            break
    elif ob == 2:
        if (90 < snake_pos[0] < 220 and 270 < snake_pos[1] < 300) or (
                210 < snake_pos[0] < 240 and 270 < snake_pos[1] < 410) or (
                390 < snake_pos[0] < 420 and 90 < snake_pos[1] < 230) or (
                410 < snake_pos[0] < 540 and 200 < snake_pos[1] < 230):
            food_spawn = True
            game_over()
            break
    elif ob == 3:
        if (90 < snake_pos[0] < 300 and 130 < snake_pos[1] < 160) or (
                270 < snake_pos[0] < 300 and 150 < snake_pos[1] < 280) or (
                290 < snake_pos[0] < 500 and 250 < snake_pos[1] < 280) or (
                470 < snake_pos[0] < 500 and 270 < snake_pos[1] < 380):
            food_spawn = True
            game_over()
            break
    else:
        if (120 < snake_pos[0] < 230 and 120 < snake_pos[1] < 230) or (
                410 < snake_pos[0] < 520 and 280 < snake_pos[1] < 390):
            food_spawn = True
            game_over()
            break

    show_score(1, black, 'times new roman', 30)
    # Refreshing game screen
    pygame.display.update()
    # Refreshing rate
    clock.tick(10)
    cx, cy = vdp()

cv.destroyAllWindows()
cap.release()