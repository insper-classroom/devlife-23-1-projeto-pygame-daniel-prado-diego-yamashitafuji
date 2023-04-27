import pygame

class UnbreakBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def eh_qubravel(self):
        return False

class BreakBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def eh_quebravel(self):
        return False

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = pygame.Surface((55, 50))
        self.rect.center = [x, y]
        self.vel = [0, 0]


    def atualiza_pos(self, last_tick, current_tick, blocks):
        preview_x, preview_y = self.rect.x, self.rect.y

        frame_time = current_tick - last_tick
        self.rect.x += self.vel[0] * frame_time / 1000
        if len(pygame.sprite.spritecollide(self, blocks, False)) > 0:
            self.rect.x = preview_x
        self.rect.y += self.vel[1] * frame_time / 1000
        if len(pygame.sprite.spritecollide(self, blocks, False)) > 0:
            self.rect.y = preview_y


class Bomb(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)

