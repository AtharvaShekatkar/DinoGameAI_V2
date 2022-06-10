#Creating a Cloud class
import pygame
from LoadImages import CLOUD
from Globals import SCREEN_WIDTH
import random

class Cloud:
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed: int):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
    

    def draw(self, SCREEN: pygame.Surface):
        SCREEN.blit(self.image, (self.x, self.y))            