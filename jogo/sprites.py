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
    def __init__(self, sprite_width, sprite_height):
        pygame.sprite.Sprite.__init__(self)
        # Inicializa estado dos jogadores
        self.direcao = 'sul'
        self.vel = [0, 0]
        self.movendo = False
        self.ind_imagem = 0
        self.tick_animacao = 0 
        self.frequencia = 20  # Frequencia da animacao em hertz
        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    # Da a posicao do retangulo
    def posiciona(self, coordeanda_x, coordenada_y): 
        self.rect.x = coordeanda_x
        self.rect.y = coordenada_y
    #  Atualiza o estado do jogador
    def update(self, tick_anterior, tick_atual, blocos):
        # Atualiza a velodcidade do jogador
        if self.movendo:
            if self.direcao == 'norte':
                self.vel = [0, -400]
            elif self.direcao == 'oeste':
                self.vel = [-400, 0]
            elif self.direcao == 'sul':
                self.vel = [0, 400]
            elif self.direcao == 'leste':
                self.vel = [400, 0]
        else:
            self.vel = [0, 0]
        # Atualiza a posicao do jogador
        ultimo_x, ultimo_y = self.rect.x, self.rect.y
        frame_time = tick_atual - tick_anterior
        self.rect.x += self.vel[0] * frame_time / 1000
        if len(pygame.sprite.spritecollide(self, blocos, False)) > 0:
            self.rect.x = ultimo_x
        self.rect.y += self.vel[1] * frame_time / 1000
        if len(pygame.sprite.spritecollide(self, blocos, False)) > 0:
            self.rect.y = ultimo_y
        # Atualiza a sprite do jogador
        if ultimo_x == self.rect.x and ultimo_y == self.rect.y:
            self.ind_imagem = 0
            self.se_moveu = True
        elif self.se_moveu:
            self.tick_animacao = tick_atual
            self.se_moveu = False
        if self.tick_animacao + 1000 / self.frequencia < tick_atual and not self.se_moveu:
            self.tick_animacao += 1000 / self.frequencia
            self.ind_imagem = (self.ind_imagem + 1) % len(self.sprite_sheet[self.direcao])

        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]

class PlayerWhite(Player):
    def __init__(self, sprite_width, sprite_height):

        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_3.png'), (sprite_width, sprite_height)),
            ],
            'oeste': [
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_3.png'), (sprite_width, sprite_height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_0.png'), (sprite_width, sprite_height )),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_3.png'), (sprite_width, sprite_height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_3.png'), (sprite_width, sprite_height)),
            ]
        }
        
        Player.__init__(self, sprite_width, sprite_height)

class PlayerBlack(Player):
    def __init__(self, sprite_width, sprite_height):
        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_3.png'), (sprite_width, sprite_height)),
            ],
            'oeste': [
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_0.png'), (sprite_width, sprite_height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_1.png'), (sprite_width, sprite_height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_2.png'), (sprite_width, sprite_height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_3.png'), (sprite_width, sprite_height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_1.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_2.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_3.png'), (sprite_width, sprite_height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (sprite_width, sprite_height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (sprite_width, sprite_height)),
            ],
        }

class Bomb(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)

