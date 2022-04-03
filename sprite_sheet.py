import pygame
import settings
import json

class Sprite_sheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey(settings.WHITE)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite.convert_alpha()

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = pygame.transform.scale(self.get_sprite(x, y, w, h),(settings.SCALE, settings.SCALE))
        return image
