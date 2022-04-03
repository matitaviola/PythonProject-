

#consente di caricare mappe realizzate con Tiled tramite l'uso della libreria
import pygame
import pytmx
import settings

class Map:
    def __init__(self, map_name):
        self.tmxmap = pytmx.load_pygame("Maps/"+ map_name +".tmx", pixelalpha=True)
        self.width = self.tmxmap.width * settings.SCALE
        self.height = self.tmxmap.height * settings.SCALE
    
    def render(self, surface_under, surface_above):
        for layer in self.tmxmap.visible_layers: #per ogni layer, in ordine di apparizione
            if isinstance(layer, pytmx.TiledTileLayer): #se è un layer di tiles (e non di oggetti/immagini)
                for x, y, gid in layer:
                    tile = self.tmxmap.get_tile_image_by_gid(gid)
                    if tile: #se hoi trovato un tile, lo disegno
                        if ("_up" in str(layer.name)): #se deve stare sopra gli obj/player, in tiled c'è "_up"
                            surface_above.blit(tile, (x * self.tmxmap.tilewidth, y * self.tmxmap.height))
                        else:
                            surface_under.blit(tile, (x * self.tmxmap.tilewidth, y * self.tmxmap.height))

    def make_map(self): #creo la superficie su cui disegnare la mappa
        temp_surface_under = pygame.Surface((self.width, self.height))
        temp_surface_above = pygame.Surface((self.width, self.height))
        temp_surface_above.set_colorkey(settings.BLACK)
        self.render(temp_surface_under, temp_surface_above)
        return temp_surface_under,temp_surface_above.convert_alpha()


#gestisce la visuale che segue il pg
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height= height

    def apply(self, entity): #entity è il pg o npc a cui fa riferimento la camera
        return entity.rect.move(self.camera.topleft) #ritorna un nuovo rettangolo shiftato dell'ammontare passato
    
    def apply_rect(self, rect): #funziona su un rect generico
        return rect.move(self.camera.topleft) 

    def update(self, target): #target è lo sprite che vogliamo fargli seguire
        # limiti bordi sinistro, destro, su, giù
        x_pos = min(0, -target.rect.x + int(settings.WIDTH / 2)) #/2 per avere il pg centrato
        x_pos = max(-(self.width - settings.WIDTH), x_pos)  # right
        y_pos = min(0, -target.rect.y + int(settings.HEIGHT / 2))
        y_pos = max(-(self.height - settings.HEIGHT), y_pos)  # bottom
        self.camera = pygame.Rect(x_pos, y_pos, self.width, self.height)