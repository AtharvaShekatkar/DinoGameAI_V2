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

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.obstacles = []

        self.run = True

        self.clock = pygame.time.Clock()

        self.cloud = Cloud()

        self.game_speed = INIT_GAME_SPEED

        self.font = pygame.font.Font("freesansbold.ttf", 20)

        self.dino = Dino()

        self.x_pos_bg = X_POS_BG_INIT

        self.points = 0

    def get_dist(pos_a: list, pos_b: list):
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]

        return math.sqrt(dx**2 + dy**2) 

    def update_background(self):
        image_width = BACKGROUND.get_width()

        self.SCREEN.blit(BACKGROUND, (self.x_pos_bg, Y_POS_BG))
        self.SCREEN.blit(BACKGROUND, (self.x_pos_bg + image_width, Y_POS_BG))

        if self.x_pos_bg <= -image_width:
            self.SCREEN.blit(BACKGROUND, (self.x_pos_bg + image_width, Y_POS_BG))
            self.x_pos_bg = 0
        
        self.x_pos_bg -= self.game_speed
        return self.x_pos_bg
    
    def update_score(self):
        self.points += 1
        if self.points % 200 == 0:
            self.game_speed += 1

        text = self.font.render("Points: " + str(self.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        self.SCREEN.blit(text, textRect)
    
    def create_obstacle(self):
        obstacle_prob = random.randint(0, 100)
        if obstacle_prob == 0:
            self.obstacles.append(SmallCactus(SMALL_CACTUS))
        elif obstacle_prob == 1:
            self.obstacles.append(LargeCactus(LARGE_CACTUS))
        elif obstacle_prob == 2:
            self.obstacles.append(Bird(BIRD))
    
    def update_game(self, user_input=None):
        self.dino.draw(self.SCREEN)

        self.dino.update(user_input)

        self.update_background()

        self.cloud.draw(self.SCREEN)

        self.cloud.update(self.game_speed)

        self.update_score() 

        self.clock.tick(60)

        pygame.display.update()

    def play_manual(self):
        
        while self.run is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
            self.SCREEN.fill((255, 255, 255))
            user_input = pygame.key.get_pressed()
            # moves = []

            if len(self.obstacles) == 0:
                self.create_obstacle()

            for obstacle in self.obstacles:
                obstacle.draw(SCREEN=self.SCREEN)
                obstacle.update(self.obstacles, self.game_speed)
                if self.dino.dino_rect.colliderect(obstacle.rect):
                    self.dino.score = self.points
                    pygame.quit()
                    self.obstacles.pop()
                    print("Game over!")
                    return

            self.update_game(user_input=user_input)