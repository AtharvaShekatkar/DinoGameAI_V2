#Loading Images
import pygame
import os

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")), 
        pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")), 
        pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]


JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]


LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))