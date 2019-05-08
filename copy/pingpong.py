# based on tutorial: https://prog-ag.de/pong-in-python-mit-pygame/

#TODO: paddles bisschen naeher an bildschirmrand schieben damit ball nicht stecken bleiben kann

import pygame
import math
import random
import numpy as np
import random
import datetime as dt
import time
import sys

# Global variables
sign = 1

WIDTH = 600
HEIGHT = 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

border_distance_x = 60
border_distance_y = 60

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
BLACK = (0,0,0)

score_left = 0
score_right = 0


#TODO bug entfernen das paddle am ball stecken bleibt

def check_for_collision(ball, paddle_left, paddle_right):
    global score_left, score_right

    # check if ball collides with left paddle
    if abs(ball.x - ball.r) <= (paddle_left.x + paddle_left.w):

        # TODO: Abfrage anpassen in relation to paddle speed
        # also: mit jedem abprallen wird paddle schneller,
        # dann muss last collison irgendwann auch > 1s sein, weil so schnell
        # deswegen statt hardcoden irgendwie noch relative to speed machen
        if (time.time() - paddle_left.last_collision_time < 1):
            return False

        # check if ball is behind left paddle
        if (ball.x + ball.r) < paddle_left.x + paddle_left.w:
            return False

        # ball is above paddle -> no collisiob
        if (ball.y - ball.r) > (paddle_left.y + paddle_left.h):

            return False

        # ball is underneath paddle -> no collision
        if (ball.y - ball.r) < (paddle_left.y):
            
            return False

        paddle_left.last_collision_time = time.time()

        return True
    
    # check if ball collides with right paddle
    if (ball.x + ball.r) >= (paddle_right.x):

        if (time.time() - paddle_right.last_collision_time < 1):
            return False

        # ball is behind paddle -> no collision
        if (ball.x + ball.r) > paddle_right.x + paddle_right.w:
            return False

        # ball is above paddle -> no collision
        if (ball.y + ball.r) > (paddle_right.y + paddle_right.h):
      
            return False
        
        # ball is underneath paddle -> no collision
        if (ball.y + ball.r) < paddle_right.y:
    
            return False
        
        paddle_right.last_collision_time = time.time()

        
        return True

    return False
     


class Paddle:
    """ Paddle class for representing a paddle to move on board"""
    
    def __init__(self, pos_x, pos_y, rect_w, rect_h, paddle_col):
        """ Create a new paddle object """
        self.x = pos_x
        self.y = pos_y
        self.w = rect_w
        self.h = rect_h
        self.color = paddle_col
        self.is_moving = False
        self.direction = 0 # Neutral = 0, Up = +1, Down = -1

        self.velocity = 15
        self.last_collision_time = 0
     



    def draw(self):
        pygame.draw.rect(SCREEN, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


    def move(self):
        # prevent paddle moving after button was pressed
        global ball

        if not self.is_moving:
            return

        # if (self.y - self.velocity) or (self.y + self.velocity):
        #     return
        
        # move up
        if self.direction == 1 and self.y > 0:
            self.y -= self.velocity

        # move down
        if self.direction == -1 and self.y + self.h < HEIGHT:
            self.y += self.velocity

class Ball:
    """ Class to represent ping pong ball """
    global HEIGHT, WIDTH

    def __init__(self, radius, velocity_x, velocity_y, color,):
        global HEIGHT, WIDTH
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.r = radius 
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        
    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.r)

    def move(self):
        #TODO: implement ball movement 
        self.x += self.velocity_x
        self.y += self.velocity_y

    def reset(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2

        random.seed(dt.datetime.now())
        #TODO: besser randomisieren
        #TODO: ball beschleunigen mit jedem score
        #TODO: reinforcement learning einbinden


        sign_x = 1
        sign_y = 1
        rnd_x = random.randint(0, 1)
        rnd_y = random.randint(0,1)
        
        if (rnd_x == 0):
            sign_x *= -1
        if (rnd_y == 0):
            sign_y *= -1
        
        self.velocity_x *= sign_x
        self.velocity_y *= sign_y

def draw_paddle(screen, color, x, y, w, h):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))

def draw_circle(screen, color, x, y, r):
    pygame.draw.circle(screen, color, (x, y), r)

def draw_score(screen, color, score, dest): #render(text, antialias, color, background=None) -> Surface
    #blit(source, dest, area=None, special_flags = 0) -> Rect
    src = score_font.render(str(score), True, color)
    screen.blit(src, dest)
        






# Rectangle varaibles
rect_height = 100
rect_width = 10
rect_movement = 100

#center of screen
left_rect_pos_x =  border_distance_x
left_rect_pos_y = int(HEIGHT/2 - rect_height/2)


right_rect_pos_x = int(WIDTH - rect_width) - border_distance_x
right_rect_pos_y = int(HEIGHT/2 - rect_height/2)




paddle_left_move_up = True
paddle_left_move_down = True
paddle_right_move_up = True
paddle_right_move_down = True

center_x = int(WIDTH/2)
center_y = int(HEIGHT/2)

circle_pos_x = center_x
circle_pos_y = center_y
radius = 10
circle_mvm_x = 450
circle_mvm_y = 450
circle_respawn = False
circle_init = True


pygame.init()

pygame.display.set_caption("PyBong 2.0")

#Set up score 
score_font = pygame.font.SysFont("Clear Sans Regular", 60)
score_left_dest = (WIDTH/4, 50)
score_right_dest = (WIDTH/1.25, 50)

end_game = False
clock = pygame.time.Clock()

paddle_left = Paddle(left_rect_pos_x, left_rect_pos_y, rect_width, rect_height, BLUE)
paddle_right = Paddle(right_rect_pos_x, right_rect_pos_y, rect_width, rect_height, RED)
vel_x = 5
vel_y = 5
ball = Ball(10, vel_x, vel_y, WHITE)

#pygame.draw.circle(screen, WHITE, (circle_pos_x, circle_pos_y), radius)

while not end_game:
    SCREEN.fill(BLACK)

    paddle_left.move()
    paddle_right.move()

    paddle_left.draw()
    paddle_right.draw()

    ball.move()
    ball.draw()
    
    if ball.y > HEIGHT or ball.y < 0:
        ball.velocity_y = - ball.velocity_y

    if check_for_collision(ball, paddle_left, paddle_right):
        ball.velocity_x = - ball.velocity_x
     

    # check if player scores a win
    if ball.x < 0:
        score_right += 1
        ball.reset()
    
    if ball.x > WIDTH:
        score_left += 1
        ball.reset()
    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

        # setup movement on key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("yes")
                sys.exit()

            if event.key == pygame.K_DOWN:
                paddle_right.direction = -1
                paddle_right.is_moving = True

            if event.key == pygame.K_UP:
                paddle_right.direction = 1
                paddle_right.is_moving = True

            if event.key == pygame.K_s:
                paddle_left.direction = -1
                paddle_left.is_moving = True

            if event.key == pygame.K_w:
                paddle_left.direction = 1
                paddle_left.is_moving = True

        # end movement on key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                paddle_right.is_moving = False
            if event.key == pygame.K_UP:
                paddle_right.is_moving = False
            if event.key == pygame.K_s:
                paddle_left.is_moving = False
            if event.key == pygame.K_w:
                paddle_left.is_moving = False

        

    # Circle movement
    circle_time_passed = clock.tick(60)
    circle_time_sec = circle_time_passed / 1000.0

    draw_score(SCREEN, BLUE, score_left, score_left_dest)
    draw_score(SCREEN, RED, score_right, score_right_dest)
        
    pygame.display.update() 
    #Frames per second
    clock.tick(60)
