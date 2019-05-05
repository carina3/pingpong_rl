# based on tutorial: https://prog-ag.de/pong-in-python-mit-pygame/

#TODO: paddles bisschen naeher an bildschirmrand schieben damit ball nicht stecken bleiben kann

import pygame
import math
import random
import numpy as np
import random
from datetime import datetime

# Global variables
sign = 1

WIDTH = 800
HEIGHT = 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

border_distance_x = 20
border_distance_y = 20

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
BLACK = (0,0,0)

score_left = 0
score_right = 0

def check_for_collision(ball, paddle_left, paddle_right):
    global score_left, score_right

    # check if ball collides with left paddle
    if (ball.x - ball.r) <= (paddle_left.x + paddle_left.w):
        # ball is above paddle -> no collisiob
        if (ball.y - ball.r) > (paddle_left.y + paddle_left.h):
            return False

        # ball is underneath paddle -> no collision
        if (ball.y - ball.r) < (paddle_left.y):
            return False

        return True
    
    # check if ball collides with right paddle
    if (ball.x + ball.r) >= (paddle_right.x):

        if (ball.y + ball.r) > (paddle_right.y + paddle_right.h):
            return False
        
        if (ball.y + ball.r) < paddle_right.y:
            return False
        
        return True
    
    return False

    
           
    # check if ball collides with right paddle
    if (ball.x + ball.r) >= paddle_right.x:
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

        self.move_up = True
        self.move_down = True
        self.velocity = 15
        self.last_key_pressed = None
        self.key_released = False
        self.bounding_box = pygame.Rect(pos_x, pos_y, rect_w, rect_h) #Rect(left, top, width, height) -> Rect

    def get_velocity(self):
        return self.velocity

    def get_bbox(self):
        return self.bounding_box

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_w(self):
        return self.w
    
    def get_h(self):
        return self.h 
    
    def get_last_key_pressed(self):
        return self.last_key_pressed
    
    def get_key_released(self):
        return self.key_released

    def set_x(self, pos_x):
        self.x = pos_x

    def set_y(self, pos_y):
        self.y = pos_y
    
    def set_w(self, rect_w):
        self.w = rect_w
    
    def set_h(self, rect_h):
        self.h = rect_h

    def set_key_released(self, is_released):
        self.key_released = is_released      

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


    def move2(self):
        # prevent paddle moving after button was pressed
        if not self.is_moving:
            return
        
        if self.direction == 1 and self.h/2 > 0:
            self.y -= self.velocity

        if self.direction == -1 and self.y + self.h/2 < HEIGHT:
            self.y += self.velocity

    
    def can_move_down(self):
        if self.y > HEIGHT - self.h/2:
            self.move_down = False
        else:
            self.move_down = False

        return self.move_down

    def can_move_up(self):
        if self.y < 0 - self.h/2:
            self.move_up = False
        else:
            self.move_up = True
        return self.move_up


    # if left_rect_pos_y < 0 - rect_height/2:
        #     paddle_left_move_up = False
        # else:
        #     paddle_left_move_up = True

        # if left_rect_pos_y > HEIGHT - rect_height/2:
        #     paddle_left_move_down = False
        # else:
        #     paddle_left_move_down = True
    def check_movement_possibilities(self):
        global HEIGHT
        offset_down = 0.75 * self.h
        offset_up = 0.05 * self.h

        if self.y < 0 - offset_up:
            self.move_up = False
        else:
            self.move_up = True

        print("self.y = ", self.y)
        print("max height = ", HEIGHT)

        if self.y >= (HEIGHT - offset_down):
            self.move_down = False
        else: 
            self.move_down = True

        print("can move up?", self.move_up)
        print("can move down?", self.move_down)

    def move(self, key_down, key_up):
        self.check_movement_possibilities()
        print("self.move_down = " + str(self.move_down) + " inside move()")
        
        if key_down:
            self.last_key_pressed = "down"
            if self.move_down:
                self.y += self.velocity
            #print("paddle_right move down to pos_y = ", self.y)
            
        if key_up:
            self.last_key_pressed = "up"
            if self.move_up:
                self.y -= self.velocity
            #print("paddle_right move up to pos_y = ", self.y)

        print("last key pressed: ", self.last_key_pressed)
        
        # if input_map[0] and paddle_right.can_move_down:
        #     paddle_right.set_y(paddle_right.get_y() + rect_movement)
        
        # if input_map[1] and paddle_right.can_move_up:
        #     paddle_right.set_y(paddle_right.get_y() - rect_movement)

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




def set_input_map(event, input_map):
     # Check if buttons are pressed to move paddle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                input_map[0] = True

            if event.key == pygame.K_UP:
                input_map[1] = True
            if event.key == pygame.K_s:
                input_map[2] = True
            if event.key == pygame.K_w:
                input_map[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                input_map[0] = False
            if event.key == pygame.K_UP:
                input_map[1] = False
            if event.key == pygame.K_s:
                input_map[2] = False
            if event.key == pygame.K_w:
                input_map[3] = False

        return input_map

def draw_paddle(screen, color, x, y, w, h):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))

def draw_circle(screen, color, x, y, r):
    pygame.draw.circle(screen, color, (x, y), r)

def draw_score(screen, color, score, dest): #render(text, antialias, color, background=None) -> Surface
    #blit(source, dest, area=None, special_flags = 0) -> Rect
    src = score_font.render(str(score), True, color)
    screen.blit(src, dest)
        



random.seed(datetime.now())


# Rectangle varaibles
rect_height = 100
rect_width = 20
rect_movement = 50

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

paddle_left = Paddle(left_rect_pos_x, left_rect_pos_y, rect_width, rect_height, BLUE)
paddle_right = Paddle(right_rect_pos_x, right_rect_pos_y, rect_width, rect_height, RED)
ball = Ball(10, 10, 5, WHITE)
# paddle_left = Paddle(left_rect_pos_x, left_rect_pos_y, rect_width, rect_height, RED, 50)
# paddle_right = Paddle(right_rect_pos_x, right_rect_pos_y, rect_width, rect_height, BLUE, 50)
# Circle

circle_pos_x = center_x
circle_pos_y = center_y
radius = 10
circle_mvm_x = 450
circle_mvm_y = 450
circle_respawn = False
circle_init = True

#Input map to control  paddle movement
input_map = 4*[False] # (W, S, Up, Down)

pygame.init()

pygame.display.set_caption("PyBong 2.0")

#Set up score 
score_font = pygame.font.SysFont("Clear Sans Regular", 60)
score_left_dest = (WIDTH/4, 50)
score_right_dest = (WIDTH/1.25, 50)

end_game = False
clock = pygame.time.Clock()

#pygame.draw.circle(screen, WHITE, (circle_pos_x, circle_pos_y), radius)

while not end_game:
    SCREEN.fill(BLACK)

    paddle_left.move2()
    paddle_right.move2()

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


    
    # paddle_left.draw(screen)
    # paddle_right.draw(screen)

    draw_score(SCREEN, BLUE, score_left, score_left_dest)
    draw_score(SCREEN, RED, score_right, score_right_dest)
        
    pygame.display.update() 
    #Frames per second
    clock.tick(60)
