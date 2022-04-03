import pygame
import settings
from game import Game, GameState

pygame.init()

screen = pygame.display.set_mode(size=(settings.WIDTH, settings.HEIGHT))

pygame.display.set_caption("First Python Game")

clock = pygame.time.Clock() #serve per settare il framerate

#creo Game gioco e gli passo lo schermo
gioco = Game(screen)
gioco.setup()
clock.tick(settings.FPS)

while gioco.game_state == GameState.RUNNING:
    gioco.update()
    gioco.render()
    pygame.display.flip()