# Running the loop for a single game instance
from argparse import Action
import random
import sys
import pygame
import numpy as np
from sqlalchemy import asc
from Dino import Dino
from Globals import *
from Cloud import Cloud
import math
from Cactus import *
import time
from Bird import Bird
from LoadImages import BACKGROUND, BIRD, SMALL_CACTUS, LARGE_CACTUS
from tqdm import tqdm

class Game:
    def __init__(self, epsilon) -> None:
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
        
        self.epsilon = epsilon

        self.ep_rewards = [-200]
    

    def reset(self):
        self.game_speed = INIT_GAME_SPEED
        old_dino = self.dino
        self.dino = Dino()
        self.dino.replay_memory = old_dino.replay_memory
        self.dino.target_update_counter = old_dino.target_update_counter
        self.dino.model.set_weights(old_dino.model.get_weights())
        self.dino.target_model.set_weights(old_dino.target_model.get_weights())


        self.x_pos_bg = X_POS_BG_INIT
        self.points = 0
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def get_dist(self, pos_a: tuple, pos_b:tuple):
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
    
    def get_state(self):
        state = []
        state.append(self.dino.dino_rect.y / self.dino.Y_DUCK_POS + 10) 
        pos_a = (self.dino.dino_rect.x, self.dino.dino_rect.y)
        if len(self.obstacles) == 0:
            dist = self.get_dist(pos_a, tuple([SCREEN_WIDTH + 10, self.dino.Y_POS])) / math.sqrt(SCREEN_HEIGHT**2 + SCREEN_WIDTH**2)
            obs_height = 0
            obj_width = 0
        else:
            dist = self.get_dist(pos_a, (self.obstacles[0].rect.midtop)) / math.sqrt(SCREEN_HEIGHT**2 + SCREEN_WIDTH**2)
            obs_height = self.obstacles[0].rect.midtop[1] / self.dino.Y_DUCK_POS
            obj_width = self.obstacles[0].rect.width / SMALL_CACTUS[2].get_rect().width
        
        state.append(dist)
        state.append(obs_height)
        state.append(self.game_speed / 24)
        state.append(obj_width)
        
        
        return state


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
    
    def update_game(self, moves, user_input=None):
        self.dino.draw(self.SCREEN)
        if user_input is not None:
            self.dino.update(user_input)
        else:
            self.dino.update_auto(moves)

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


    def play_auto(self):
        for episode in tqdm(range(1, NUM_EPISODES + 1), ascii=True, unit='episodes'):
            episode_reward = 0
            step = 1
            current_state = self.get_state()
            self.run = True
            while self.run is True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                
                self.SCREEN.fill((255, 255, 255))

                if len(self.obstacles) == 0:
                    self.create_obstacle()

                # if self.run == False:
                #     print(current_state)
                #     time.sleep(2)
                #     continue

                if np.random.random() > self.epsilon:
                    action = self.dino.get_qs(current_state)
                    # print(action)
                    action = np.argmax(action)
                    # print(action)
                else:
                    num = np.random.randint(0, 10)
                    if num == 0:
                        # print("yes")
                        action = num
                    elif num <= 5:
                        action = 1
                    else:
                        action = 2

                self.update_game(moves=action)
                # print(self.game_speed)
                next_state = self.get_state()
                reward = 0

                for obstacle in self.obstacles:
                    obstacle.draw(SCREEN=self.SCREEN)
                    obstacle.update(self.obstacles, self.game_speed)
                    next_state = self.get_state()
                    if self.dino.dino_rect.x > obstacle.rect.x + obstacle.rect.width:
                        reward = 3
                    if self.dino.dino_rect.colliderect(obstacle.rect):
                        self.dino.score = self.points
                        # pygame.quit()
                        self.obstacles.pop()
                        self.reset()
                        reward = -10
                        print("Game over!")
                        self.run = False
                        break
                if reward != 0:
                    print(reward > 0)

                episode_reward += reward
                
                self.dino.update_replay_memory(tuple([current_state, action, reward, next_state, self.run]))

                self.dino.train( not self.run, step=step)

                current_state = next_state

                step += 1

                self.clock.tick(60)

                # print(current_state)

                pygame.display.update()
            

            self.ep_rewards.append(episode_reward)
            if episode % 100 == 0:
                self.dino.model.save(f'models/Episode_{episode}_model.model')
            

            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY
                self.epsilon = max(MIN_EPSILON, self.epsilon)
                # print(self.epsilon)
                # print((self.dino.replay_memory))
