import pygame


class Mapa(pygame.Surface):
    def __init__(self, estado_jogo):
        pygame.Surface.__init__(self, (estado_jogo.largura_mapa, estado_jogo.altura_mapa))
        
        self.width = estado_jogo.largura_mapa
        self.height = estado_jogo.altura_mapa


class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class UnbreakBlock(Block):
    def __init__(self, estado_jogo, x, y):
        self.width = estado_jogo.sprite_size[0]
        self.height = estado_jogo.sprite_size[1]
        self.x = x
        self.y = y
        # Inicializa imagem
        imagem_w, imagem_h = pygame.image.load('assets/Blocos/blocoinquebravel.png').get_size()
        imagem_res = imagem_w / imagem_h
        self.image = pygame.transform.scale(pygame.image.load('assets/Blocos/blocoinquebravel.png'), (self.width, self.height * imagem_res ** -1))

        Block.__init__(self)


    def eh_qubravel(self):
        return False


class BreakBlock(Block):
    def __init__(self, estado_jogo, x, y):
        self.width = estado_jogo.sprite_size[0]
        self.height = estado_jogo.sprite_size[1]
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('assets/Blocos/blocoquebravel.png'), (self.width, self.height))

        Block.__init__(self)

    def eh_quebravel(self):
        return False

    
class Player(pygame.sprite.Sprite):
    def __init__(self, estado_jogo, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Parametros dos jogadores
        self.estoque_bomba = 2
        self.alcance_bomba = 2
        self.bombas = pygame.sprite.Group()
        # Inicializa estado dos jogadores
        self.sprite_size = estado_jogo.sprite_size
        self.sprite_width = estado_jogo.sprite_size[0]
        self.sprite_height = estado_jogo.sprite_size[1]
        self.tick_anterior = 0
        self.direcao = 'sul'
        self.vel = [0, 0]
        self.esta_movendo = False
        self.ind_imagem = 0
        self.tick_origem_animacao = 0 
        self.frequencia = 20  # Frequencia da animacao em hertz
        # Inicializa surface e rect do player
        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]
        self.rect = pygame.Rect(0, 0, estado_jogo.sprite_size[0], estado_jogo.sprite_size[1])
        self.rect.x = x
        self.rect.y = y
        self.blocos = estado_jogo.blocos
    #  Atualiza o estado do jogadorS
    def update(self, estado_jogo):
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
        frame_time = estado_jogo.tick_atual - self.tick_anterior
        self.tick_anterior = estado_jogo.tick_atual
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
            self.tick_origem_animacao = estado_jogo.tick_atual
            self.esta_parado = False
        if self.tick_origem_animacao + 1000 / self.frequencia < estado_jogo.tick_atual and not self.esta_parado:
            self.tick_origem_animacao += 1000 / self.frequencia
            self.ind_imagem = (self.ind_imagem + 1) % len(self.sprite_sheet[self.direcao])

        self.image = self.sprite_sheet[self.direcao][self.ind_imagem]

    def cria_bomba(self, estado_jogo):
        if self.estoque_bomba > 0:
            self.estoque_bomba -= 1
            pos_x_arredondado = round(self.rect.x / self.sprite_width) * self.sprite_width
            pos_y_arredondado = round(self.rect.y / self.sprite_height) * self.sprite_height
            estado_jogo.bombas.add(Bomb(pos_x_arredondado, pos_y_arredondado, estado_jogo, self.alcance_bomba))


class PlayerWhite(Player):
    def __init__(self, estado_jogo, x, y):
        self.width, self.height = estado_jogo.sprite_size[0], estado_jogo.sprite_size[1] * 1.6
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
        
        Player.__init__(self, estado_jogo, x, y)
        estado_jogo.jogadores.add(self)


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
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_0.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_1.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_2.png'), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load('assets/PlayerPreto/PretoOeste/brancooeste_3.png'), (self.width, self.height)),
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
    def __init__(self, x, y, estado_jogo, alcance):
        pygame.sprite.Sprite.__init__(self)
        self.width = estado_jogo.sprite_size[0]
        self.height = estado_jogo.sprite_size[1]
        # Inicializa imagens da bomba
        self.sprite_sheet = [
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_0.png'), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_1.png'), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load('assets/Bomba/bomb_2.png'), (self.width, self.height)),
        ]
        self.ind_imagem = 0
        self.fase_imagem = 1
        self.image = self.sprite_sheet[self.ind_imagem]
        # Inicializa retangulo da bomba
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Inicializa parametros da bomba
        self.tick_inicial = pygame.time.get_ticks()
        self.alcance = alcance


    def update(self, estado_jogo):
        if estado_jogo.tick_atual > self.tick_inicial + 500 * self.fase_imagem:
            self.fase_imagem += 1
            self.ind_imagem = self.fase_imagem % 3
            self.image = self.sprite_sheet[self.ind_imagem]
        
        if estado_jogo.tick_atual > self.tick_inicial + 3000:
            self.explode_bomba(estado_jogo)

    def explode_bomba(self, estado_jogo):
        estado_jogo.bombas.remove(self)
        estado_jogo.jogador_um.estoque_bomba += 1
        # Constroe a explosao
        tick_inicial = pygame.time.get_ticks()
        for a in range(5):
            i = 0
            colide_parede = False
            while i < self.alcance and not colide_parede:
                i += 1
                if i == self.alcance:
                    fase = 2
                else:
                    fase = 1
                if a == 0:
                    explosao = Explosao(estado_jogo, self.rect.x, self.rect.y, 0, 'leste', tick_inicial)  # Desenha o centro da explosao
                if a == 1:
                    explosao = Explosao(estado_jogo, self.rect.x + self.width * i, self.rect.y, fase, 'leste', tick_inicial)  # ... o leste
                elif a == 2:
                    explosao = Explosao(estado_jogo, self.rect.x , self.rect.y - self.height * i, fase, 'norte', tick_inicial)  # ... o norte
                elif a == 3:
                    explosao = Explosao(estado_jogo, self.rect.x - self.width * i, self.rect.y, fase, 'oeste', tick_inicial)  # ... o oeste
                elif a == 4:
                    explosao = Explosao(estado_jogo, self.rect.x , self.rect.y + self.height * i, fase, 'sul', tick_inicial)  # ... o sul

                if len(pygame.sprite.spritecollide(explosao, estado_jogo.blocos, False)) > 0:
                    colide_parede = True
                else:
                    estado_jogo.explosoes.add(explosao)  # ... o leste
                    

class Explosao(pygame.sprite.Sprite):
    def __init__(self, estado_jogo, x, y, parte, orientacao, tick_inicial):
        pygame.sprite.Sprite.__init__(self)

        self.width = estado_jogo.sprite_size[0]
        self.height = estado_jogo.sprite_size[1]
        # Inicializa imagens da explosao
        self.sprite_sheet = [
            [pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoA/explosionA_0.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoA/explosionA_1.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoA/explosionA_2.png'), (self.width, self.height)),],
            [pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoB/explosionB_0.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoB/explosionB_1.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoB/explosionB_2.png'), (self.width, self.height)),],
            [pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoC/explosionC_0.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoC/explosionC_1.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoC/explosionC_2.png'), (self.width, self.height)),],
            [pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoD/explosionD_0.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoD/explosionD_1.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoD/explosionD_2.png'), (self.width, self.height)),],
            [pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoE/explosionE_0.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoE/explosionE_1.png'), (self.width, self.height)),
             pygame.transform.scale(pygame.image.load('assets/Explosao/ExplosaoE/explosionE_2.png'), (self.width, self.height)),],
        ]
        if orientacao == 'leste':
            self.inclinacao = 0
        if orientacao == 'norte':
            self.inclinacao = 90
        elif orientacao == 'oeste':
            self.inclinacao = 180
        elif orientacao == 'sul':
            self.inclinacao = 270
        self.ind_fase = 0
        self.ind_parte = parte
        self.image = pygame.transform.rotate(self.sprite_sheet[self.ind_fase][self.ind_parte], self.inclinacao)
        # Inicializa parametros da explosao
        self.tempo_explosao = 1000  # Tempo da explosao em milisegundos
        self.tick_inicial = tick_inicial
        self.ind_fase = 0
        self.contador = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, estado_jogo):  # Consertar a animaacao
        if self.contador < 5:
            if estado_jogo.tick_atual > self.tick_inicial + self.tempo_explosao * self.contador / 10:
                self.ind_fase += 1
                self.contador += 1
                self.image = pygame.transform.rotate(self.sprite_sheet[self.ind_fase][self.ind_parte], self.inclinacao)
        elif self.contador < 10:
            if estado_jogo.tick_atual > self.tick_inicial + self.tempo_explosao * self.contador / 10:
                self.ind_fase -= 1
                self.contador += 1
                self.image = pygame.transform.rotate(self.sprite_sheet[self.ind_fase][self.ind_parte], self.inclinacao)
        else:
            estado_jogo.explosoes.remove(self)  # Remove a explosao