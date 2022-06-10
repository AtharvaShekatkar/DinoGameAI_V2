# Creating Cactus subclasses from Obstacle
import pygame
from Obstacle import Obstacle
import random
from typing import List

class LargeCactus(Obstacle):
    def __init__(self, image: List[pygame.Surface]) -> None:
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class SmallCactus(Obstacle):
    def __init__(self, image: List[pygame.Surface]) -> None:
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325