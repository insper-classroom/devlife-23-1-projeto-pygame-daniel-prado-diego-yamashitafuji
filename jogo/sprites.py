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

class PlayerUm(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.rect.x = x
        self.rect.y = y
        self.vel = 400
        self.image = image

class PlayerDois(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite. __init__(self)

        self.rect.x = x
        self.rect.y = y
        self.vel = 400
        self.image = image
