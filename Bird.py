#Creating the bird subclass from Obstacle
from random import random
import pygame
from Obstacle import Obstacle
from typing import List
import random

class Bird(Obstacle):
    def __init__(self, image: List[pygame.Surface]) -> None:
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(120, 320)
        self.index = 0
    
    def draw(self, SCREEN: pygame.Surface):
        if self.index >= 19:
            self.index = 0
        
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1