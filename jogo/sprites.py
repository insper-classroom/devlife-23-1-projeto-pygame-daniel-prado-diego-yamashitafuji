import pygame


class Mapa(pygame.Surface):
    def __init__(self, largura_mapa, altura_mapa):
        pygame.Surface.__init__(self, (largura_mapa, altura_mapa))
        
        self.width = largura_mapa
        self.height = altura_mapa

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
    def __init__(self, sprite_width, sprite_height, blocos):
        pygame.sprite.Sprite.__init__(self)
        # Inicializa estado dos jogadores
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.tick_anterior = 0
        self.direcao = 'sul'
        self.vel = [0, 0]
        self.esta_movendo = False
        self.ind_imagem = 0
        self.tick_origem_animacao = 0 
        self.frequencia = 20  # Frequencia da animacao em hertz
        # Inicializa surface e rect do player
        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]
        self.rect = pygame.Rect(0, 0, sprite_width, sprite_height)
        self.blocos = blocos

    # Da a posicao do retangulo
    def posiciona(self, x, y):
        self.rect.x = x
        self.rect.y = y

    #  Atualiza o estado do jogadorS
    def update(self, tick_atual):
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
        ultima_pos = [self.rect.x, self.rect.y]
        frame_time = tick_atual - self.tick_anterior
        self.tick_anterior = tick_atual
        self.rect.x += self.vel[0] * frame_time / 1000
        self.rect.y += self.vel[1] * frame_time / 1000
        if len(pygame.sprite.spritecollide(self, self.blocos, False)) > 1:
            self.rect.x,self.rect.y = ultima_pos
        # Deslocamento suavizado em vertices de bloco
        elif len(pygame.sprite.spritecollide(self, self.blocos, False)) == 1:
            bloco_colidido = pygame.sprite.spritecollide(self, self.blocos, False)[0]
            if self.direcao == 'norte':  # Colisao para cima
                self.rect.y = ultima_pos[1]
                if self.rect.midtop[0] > bloco_colidido.rect.right:
                    self.rect.x += 1
                elif self.rect.midtop[0] < bloco_colidido.rect.left:
                    self.rect.x -= 1
                else:
                    self.rect.x = ultima_pos[0]
            elif self.direcao == 'leste':  # ... direita
                self.rect.x = ultima_pos[0]
                if self.rect.midright[1] > bloco_colidido.rect.bottom:
                    self.rect.y += 1
                elif self.rect.midright[1] < bloco_colidido.rect.top:
                    self.rect.y -= 1
                else:
                    self.rect.y = ultima_pos[1]
            elif self.direcao == 'sul':  # ... baixo
                self.rect.y = ultima_pos[1]
                if self.rect.midbottom[0] > bloco_colidido.rect.right:
                    self.rect.x += 1
                elif self.rect.midbottom[0] < bloco_colidido.rect.left:
                    self.rect.x -= 1
                else:
                    self.rect.y = ultima_pos[1]
            elif self.direcao == 'oeste':  # ...esquerda
                self.rect.x = ultima_pos[0]
                if self.rect.midleft[1] > bloco_colidido.rect.bottom:
                    self.rect.y += 1
                elif self.rect.midleft[1] < bloco_colidido.rect.top:
                    self.rect.y -= 1
                else:
                    self.rect.x = ultima_pos[0]
        # Atualiza a sprite do jogador
        if ultima_pos == [self.rect.x, self.rect.y]:
            self.ind_imagem = 0
            self.esta_parado = True
        elif self.esta_parado:
            self.tick_origem_animacao = tick_atual
            self.esta_parado = False
        if self.tick_origem_animacao + 1000 / self.frequencia < tick_atual and not self.esta_parado:
            self.tick_origem_animacao += 1000 / self.frequencia
            self.ind_imagem = (self.ind_imagem + 1) % len(self.sprite_sheet[self.direcao])

        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]


class PlayerWhite(Player):
    def __init__(self, sprite_width, sprite_height, blocos):
        self.width = sprite_width
        self.height = sprite_height * 1.6

        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoNorte/branconorte_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoNorte/branconorte_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoNorte/branconorte_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoNorte/branconorte_3.png'), (self.width, self.height)),
            ],
            'oeste': [
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoOeste/brancooeste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoOeste/brancooeste_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoOeste/brancooeste_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoOeste/brancooeste_3.png'), (self.width, self.height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoSul/brancosul_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoSul/brancosul_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoSul/brancosul_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoSul/brancosul_3.png'), (self.width, self.height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoLeste/brancoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoLeste/brancoleste_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoLeste/brancoleste_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerBranco/BrancoLeste/brancoleste_3.png'), (self.width, self.height)),
            ]
        }
        
        Player.__init__(self, sprite_width, sprite_height, blocos)


class PlayerBlack(Player):
    def __init__(self, sprite_width, sprite_height):
        self.sprite_sheet = {
            'norte': [
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoNorte/pretonorte_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoNorte/pretonorte_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoNorte/pretonorte_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoNorte/pretonorte_3.png'), (self.width, self.height)),
            ],
            'oeste': [
                pygame.transfrom.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_0.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_1.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_2.png'), (self.width, self.height)),
                pygame.transfrom.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_3.png'), (self.width, self.height)),
            ],
            'sul': [
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoSul/pretosul_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoSul/pretosul_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoSul/pretosul_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoSul/pretosul_3.png'), (self.width, self.height)),
            ],
            'leste': [
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoLeste/pretoleste_0.png'), (self.width, self.height)),
            ],
        }


class Bomb(pygame.sprite.Sprite):
    def __init__(self,x, y, sprite_widht, sprite_height):
        pygame.sprite.Sprite.__init__(self)
        self.width = sprite_widht
        self.height = sprite_height
        # Inicializa imagens da bomba
        self.sprite_sheet = [
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_0.png'), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_1.png'), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_2.png'), (self.width, self.height)),
        ]
        self.ind_imagem = 0
        self.image = self.sprite_sheet[self.ind_imagem]
        # Inicializa retangulo da bomba
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Inicializa parametros da bomba
        self.tick_inicial = pygame.time.get_ticks()
        self.raio = 2 

    #def update(self):
