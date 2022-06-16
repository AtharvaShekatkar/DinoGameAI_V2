#Creating the Dino class
import pygame
from LoadImages import RUNNING, JUMPING, DUCKING
import numpy as np
from DQNAgent import DQNAgent

class Dino(DQNAgent):
    X_POS = 80
    Y_POS = 310
    Y_DUCK_POS = 340
    JUMP_VEL = 8.5
    #code here
    def __init__(self) -> None:
        #Initializing the images for the dino
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING


        #Initially the dino starts running
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.score = 0

        super().__init__()
    
    
    # Update the Dino's state
    def update(self, move: pygame.key.ScancodeWrapper):
        if self.dino_duck:
            self.duck()
        
        if self.dino_jump:
            self.jump()
        
        if self.dino_run:
            self.run()

        if self.step_index >= 20:
            self.step_index = 0
        

        if move[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False

        elif move[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        
        elif not(self.dino_jump or move[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
    
    def update_auto(self, move):
        if self.dino_duck == True:
            self.duck()
        
        if self.dino_jump == True:
            self.jump()
        
        if self.dino_run == True:
            self.run()

        if self.step_index >= 20:
            self.step_index = 0
        
        if move == 0 and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False

        elif move == 1 and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        
        elif not(self.dino_jump or move == 1):
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False

    def duck(self) -> None:
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_DUCK_POS
        self.step_index += 1

    def run(self) -> None:
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        

    def jump(self) -> None:
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.6
        
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN: pygame.Surface):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))