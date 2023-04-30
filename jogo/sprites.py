import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class UnbreakBlock(Block):
    def __init__(self, x, y, sprite_width, sprite_height):
        self.x = x
        self.y = y
        # Inicializa imagem
        imagem_w, imagem_h = pygame.image.load('assets/Blocos/blocoinquebravel.png').get_size()
        imagem_res = imagem_w / imagem_h
        self.width = sprite_width
        self.height = sprite_height
        self.image = pygame.transform.scale(pygame.image.load('assets/Blocos/blocoinquebravel.png'), (self.width, self.height * imagem_res ** -1))

        Block.__init__(self)


    def eh_qubravel(self):
        return False


class BreakBlock(Block):
    def __init__(self, x, y, sprite_width, sprite_height):
        self.x = x
        self.y = y
        self.width = sprite_width
        self.height = sprite_height
        self.image = pygame.transform.scale(pygame.image.load('assets/Blocos/blocoquebravel.png'), (self.width, self.height))

        Block.__init__(self)

    def eh_quebravel(self):
        return False

    
class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_width, sprite_height):
        pygame.sprite.Sprite.__init__(self)
        # Inicializa estado dos jogadores
        self.direcao = 'sul'
        self.vel = [0, 0]
        self.esta_movendo = False
        self.ind_imagem = 0
        self.tick_origem_animacao = 0 
        self.frequencia = 20  # Frequencia da animacao em hertz
        # Inicializa surface e rect do player
        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]
        self.rect = pygame.Rect(0, 0, sprite_width, sprite_height)

    # Da a posicao do retangulo
    def posiciona(self, x, y):
        self.rect.x = x
        self.rect.y = y

    #  Atualiza o estado do jogadorS
    def update(self, tick_anterior, tick_atual, blocos):
        # Atualiza a velodcidade do jogador
        if self.esta_movendo:
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
            self.tick_origem_animacao = tick_atual
            self.se_moveu = False
        if self.tick_origem_animacao + 1000 / self.frequencia < tick_atual and not self.se_moveu:
            self.tick_origem_animacao += 1000 / self.frequencia
            self.ind_imagem = (self.ind_imagem + 1) % len(self.sprite_sheet[self.direcao])

        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]


class PlayerWhite(Player):
    def __init__(self, sprite_width, sprite_height):
        self.width = sprite_width
        self.height = sprite_height * 1.6

        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoNorte/branconorte_3.png'), (self.width, self.height)),
            ],
            'oeste': [
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoOeste/brancooeste_3.png'), (self.width, self.height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoSul/brancosul_3.png'), (self.width, self.height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/BrancoLeste/brancoleste_3.png'), (self.width, self.height)),
            ]
        }
        
        Player.__init__(self, sprite_width, sprite_height)


class PlayerBlack(Player):
    def __init__(self, sprite_width, sprite_height):
        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoNorte/pretonorte_3.png'), (self.width, self.height)),
            ],
            'oeste': [
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_0.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_1.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_2.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PretoOeste/brancooeste_3.png'), (self.width, self.height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoSul/pretosul_3.png'), (self.width, self.height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
            ],
        }


class Bomb(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)

