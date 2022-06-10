# Running the loop for a single game instance
import random
import sys
import pygame
from Dino import Dino
from Globals import *
from Cloud import Cloud
import math
from Cactus import *
from Bird import Bird
from LoadImages import BACKGROUND, BIRD, SMALL_CACTUS, LARGE_CACTUS

def update_score(points: int, game_speed: int, SCREEN: pygame.Surface, font: pygame.font.Font):
    points += 1
    if points % 200 == 0:
        game_speed += 1

    text = font.render("Points: " + str(points), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (1000, 40)
    SCREEN.blit(text, textRect)

    return points, game_speed

def update_background(game_speed: int, x_pos_bg: int, SCREEN: pygame.Surface):
    image_width = BACKGROUND.get_width()

    SCREEN.blit(BACKGROUND, (x_pos_bg, Y_POS_BG))
    SCREEN.blit(BACKGROUND, (x_pos_bg + image_width, Y_POS_BG))

    if x_pos_bg <= -image_width:
        SCREEN.blit(BACKGROUND, (x_pos_bg + image_width, Y_POS_BG))
        x_pos_bg = 0
    
    x_pos_bg -= game_speed
    return x_pos_bg


def get_dist(pos_a: list, pos_b: list):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]

    return math.sqrt(dx**2 + dy**2)





def game():
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    obstacles = []

    run = True
    clock = pygame.time.Clock()

    cloud = Cloud()

    game_speed = INIT_GAME_SPEED

    font = pygame.font.Font("freesansbold.ttf", 20)

    dino_player = Dino()

    x_pos_bg = X_POS_BG_INIT

    points = 0

    while run is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()
        moves = []

        if len(obstacles) == 0:
            obstacle_prob = random.randint(0, 100)
            if obstacle_prob == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_prob == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_prob == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN=SCREEN)
            obstacle.update(obstacles, game_speed)
            if dino_player.dino_rect.colliderect(obstacle.rect):
                dino_player.score = points
                pygame.quit()
                obstacles.pop()
                print("Game over!")
                return


        # get move code here
        dino_player.draw(SCREEN)

        dino_player.update(user_input)

        x_pos_bg = update_background(game_speed, x_pos_bg, SCREEN)

        cloud.draw(SCREEN)

        cloud.update(game_speed)

        points, game_speed = update_score(points, game_speed, SCREEN, font) 

        clock.tick(60)

        pygame.display.update()