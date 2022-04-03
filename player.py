import pygame
import settings
from sprite_sheet import Sprite_sheet

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x_pos, y_pos):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.game = game
        self.position = pygame.math.Vector2(x_pos, y_pos)

        self.spritesheet = Sprite_sheet('Graphical_Assets/Characters/char0.png')
        self.pg_images = {"front":self.spritesheet.parse_sprite("front.png"),
                            "back":self.spritesheet.parse_sprite("back.png"),
                            "left":self.spritesheet.parse_sprite("left.png"),
                            "right":self.spritesheet.parse_sprite("right.png")}

        #self.image = pygame.image.load("Graphical_Assets/Char_1.png")
        #self.image = pygame.transform.scale(self.image, (settings.SCALE, settings.SCALE))
        self.image = self.pg_images["front"]
        self.rect = self.image.get_rect()
        print("player created")

    def update(self):
            self.next_move = [0,0]
            self.handle_keys()
            self.update_position(self.next_move[0], self.next_move[1])

    def handle_keys(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.image = self.pg_images["back"]
            self.next_move = [0, -1]
        elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.image = self.pg_images["front"]
            self.next_move = [0, 1]
        elif pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.image = self.pg_images["left"]
            self.next_move = [-1, 0]
        elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.image = self.pg_images["right"]
            self.next_move = [1, 0]
        else:
            self.next_move = [0,0]

    def collision_check(self, group, x, y): 
        for object in group:
            if self.rect.colliderect(object.rect):
                print("Check di collisioni per l'obj in pos: "+str(object.x_pos)+","+str(object.y_pos))
                if x > 0 and object.rect.left < self.rect.right :
                    self.position.x = self.position.x -1
                if x < 0 and object.rect.right > self.rect.left:
                    self.position.x = self.position.x + 1
                if y < 0 and object.rect.top < self.rect.bottom:
                    self.position.y = self.position.y + 1
                if y > 0 and object.rect.bottom > self.rect.top:
                    self.position.y = self.position.y - 1



    def update_position(self, x_repos, y_repos):
        self.rect = self.image.get_rect()
        self.position.x += x_repos
        self.position.y += y_repos
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        if self.next_move != [0, 0]:
            self.collision_check(self.game.walls, x_repos, y_repos)
        print("pos: "+str(self.position.x)+","+str(self.position.y))
    
    def render(self, screen):
        self.screen = screen
        screen.blit(self.image, self.rect)