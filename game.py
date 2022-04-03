#Gamestate
from enum import Enum
import settings

class GameState(Enum):
    NONE = 0
    RUNNING = 1
    ENDED = 2

#Game
import pygame
from os import path
from player import Player
from map_cam import Map, Camera
from map_objects import Obstacle

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.game_state = GameState.NONE
        self.show_rect_debug = False
        

    def setup(self):
        self.game_state = GameState.RUNNING

        self.map = Map("Test")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img[0].get_rect()

        for tile_obj in self.map.tmxmap.objects:
            if tile_obj.name == 'Player': #spawn point player
                self.player = Player(self, tile_obj.x, tile_obj.y)
                self.player_img = self.player.image
            if tile_obj.name == 'Wall' or tile_obj.name == 'Obstacle' or tile_obj.name == 'Tree':
                Obstacle(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
            if tile_obj.name == 'Water':
                pass
        self.camera = Camera(self.map.width, self.map.height)

    
    def update(self):
        self.handle_events()
        self.sprites.update()
        self.camera.update(self.player)

       
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE):
                self.game_state = GameState.ENDED
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.show_rect_debug = not(self.show_rect_debug)
            
    def render(self):
        self.screen.blit(self.map_img[0], self.camera.apply_rect(self.map_rect)) #disegno la parte sotto agli sprite
        for sprite in self.sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.show_rect_debug:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camera.apply_rect(sprite.rect), 1)
        self.screen.blit(self.map_img[1], self.camera.apply_rect(self.map_rect)) #disegno la parte sopra agli sprite

        if self.show_rect_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, settings.BLACK, self.camera.apply_rect(wall.rect), 1)
        pygame.display.flip()
