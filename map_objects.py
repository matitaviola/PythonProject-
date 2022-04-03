import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, gioco, x, y, width, height):
        self.groups = gioco.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = gioco
        self.rect = pygame.Rect(x, y, width, height)
        self.x_pos = x
        self.y_pos = y
        self.rect.x = x
        self.rect.y = y