# Creating an Obstacle class
import pygame
from typing import List

from Globals import SCREEN_WIDTH

class Obstacle:
    def __init__(self, image: List[pygame.Surface], type: int) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, obstacles: list, game_speed: int):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
    def draw(self, SCREEN: pygame.Surface):
        SCREEN.blit(self.image[self.type], self.rect)