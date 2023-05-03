import pygame
import random
from sprites import *


class TelaMenu:
    def __init__(self, largura_janela, altura_janela):
        # Inicializa parametros da tela
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        # Inicializa sons de interacao
        self.som = pygame.mixer.Sound('jogo/img/som_inicial.wav')
        # Inicializa fonte dos icones
        self.font = 'jogo/img/fonte.ttf'
        # Inicializa icones da tela
        self.TITLE = pygame.image.load('assets/bomber_title.png')
        self.TITLE_w, self.TITLE_h = self.TITLE.get_size()
        self.TITLE_x, self.TITLE_y = ((self.largura_janela - self.TITLE_w) / 2, 0)    
        self.BOMB_INICIAL = pygame.image.load('jogo/img/bomb_inicial.png')
        self.BOMB_INICIAL_SCALE = pygame.transform.scale(self.BOMB_INICIAL, (275,275))
        self.BATTLE = pygame.font.Font(self.font, 40).render('BATTLE MODE', True, 	(255, 140, 0))
        self.CREDITS = pygame.font.Font(self.font, 40).render('CREDITS', True, 	(255, 140, 0))
        self.EXIT = pygame.font.Font(self.font, 40).render('EXIT', True, 	(255, 140, 0))
        
        self.rect_BATTLE = self.BATTLE.get_rect()
        self.rect_BATTLE.x = 300
        self.rect_BATTLE.y = 360
        
        self.rect_CREDITS = self.CREDITS.get_rect()
        self.rect_CREDITS.x = 300
        self.rect_CREDITS.y = 460
        
        self.rect_EXIT = self.EXIT.get_rect()
        self.rect_EXIT.x = 300
        self.rect_EXIT.y = 560

    def desenha(self, window):
        window.fill((0, 0, 255))
        window.blit(self.TITLE, (self.TITLE_x, 20))
        window.blit(self.BOMB_INICIAL_SCALE, (5, 340))
        window.blit(self.BATTLE, (300, 360))
        window.blit(self.CREDITS, (300, 460))
        window.blit(self.EXIT, (300, 560))

        pygame.display.update()

    def atualiza(self, jogo):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            # Analisa a posicao do mouse
            if mouse_point.colliderect(self.rect_BATTLE):
                self.BATTLE = pygame.font.Font(self.font, 50).render('BATTLE MODE', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_BATTLE):
                self.BATTLE = pygame.font.Font(self.font, 40).render('BATTLE MODE', True, (255, 140, 0))
            if mouse_point.colliderect(self.rect_CREDITS):
                self.CREDITS = pygame.font.Font(self.font, 50).render('CREDITS', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_CREDITS):
                self.CREDITS = pygame.font.Font(self.font, 40).render('CREDITS', True, (255, 140, 0))
            if mouse_point.colliderect(self.rect_EXIT):
                self.EXIT = pygame.font.Font(self.font, 50).render('EXIT', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_EXIT):
                self.EXIT = pygame.font.Font(self.font, 40).render('EXIT', True, (255, 140, 0))
            # Analiza o clique do mouse
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_BATTLE):
                    self.som.play()
                    return TelaOpções(self.largura_janela, self.altura_janela)
                elif mouse_point.colliderect(self.rect_CREDITS):
                    self.som.play()
                    return TelasCredito(self.largura_janela, self.altura_janela)
                elif mouse_point.colliderect(self.rect_EXIT):
                    return 'exit'
        return self
    

class TelasCredito:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        

        self.IMAGEM_ICON = pygame.image.load('jogo/img/bomberman-icon.png')
        self.IMAGEM_ICON_SCALE = pygame.transform.scale(self.IMAGEM_ICON, (45,45))

        self.BOMB_FINAL = pygame.image.load('jogo/img/bomb_credits.png')
        self.font = 'jogo/img/fonte.ttf'

        

        self.GRUPO = pygame.font.Font(self.font, 50).render('GRUPO', True, (255, 140, 0))
        self.DANIEL = pygame.font.Font(self.font, 35).render('DANIEL', True, (255, 140, 0))
        self.DIEGO = pygame.font.Font(self.font, 35).render('DIEGO ', True, (255, 140, 0))
        self.VOLTAR = pygame.font.Font(self.font, 35).render('VOLTAR ', True, (255, 140, 0))

        self.rect_VOLTAR = self.VOLTAR.get_rect()
        self.rect_VOLTAR.x = 50
        self.rect_VOLTAR.y = 50

    def desenha(self, window):
        window.fill((0, 0, 255))
        window.blit(self.IMAGEM_ICON_SCALE, (60,450))
        window.blit(self.IMAGEM_ICON_SCALE, (60,550))
        window.blit(self.BOMB_FINAL, (360,20))
        window.blit(self.GRUPO, (50, 370))
        window.blit(self.DANIEL, (120, 460))
        window.blit(self.DIEGO, (120, 560))
        window.blit(self.VOLTAR, (50, 50))

        pygame.display.update()

    
    def atualiza(self, jogo):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
            if mouse_point.colliderect(self.rect_VOLTAR):
                self.VOLTAR = pygame.font.Font(self.font, 40).render('VOLTAR', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_VOLTAR):
                self.VOLTAR = pygame.font.Font(self.font, 35).render('VOLTAR', True, (255, 140, 0))

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_VOLTAR):
                    return TelaMenu(self.largura_janela, self.altura_janela)
        return self
    

class TelaOpções:  # Tela de selecao da partida (melhor de ...)
    def __init__(self, largura_janela, altura_janela):
        # Inicializa parametros da tlea
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        # Inicializa som de interacao
        self.som = pygame.mixer.Sound('jogo/img/som_inicial.wav')
        # Inicializa fonte dos icones
        self.font = 'jogo/img/fonte.ttf'

        self.TITLE = pygame.image.load('assets/bomber_title.png')
        self.TITLE_w, self.TITLE_h = self.TITLE.get_size()
        self.TITLE_x, self.TITLE_y = ((self.largura_janela - self.TITLE_w) / 2, 0)

        self.um = pygame.font.Font(self.font, 40).render('MELHOR DE UM', True, (255, 140, 0))
        self.tres = pygame.font.Font(self.font, 40).render('MELHOR DE TRÊS', True, (255, 140, 0))
        self.cinco = pygame.font.Font(self.font, 40).render('MELHOR DE CINCO', True, (255, 140, 0))


        self.rect_um = self.um.get_rect()
        self.rect_um.x = largura_janela/2
        self.rect_um.y = 360

        self.rect_tres = self.um.get_rect()
        self.rect_tres.x = largura_janela/2
        self.rect_tres.y = 460

        self.rect_cinco = self.um.get_rect()
        self.rect_cinco.x = largura_janela/2
        self.rect_cinco.y = 560


    def desenha(self, window):
        window.fill((0, 0, 255))
        window.blit(self.TITLE, (self.TITLE_x, 20))
        window.blit(self.um, ((self.largura_janela - self.um.get_width()) / 2, 360))
        window.blit(self.tres, ((self.largura_janela - self.tres.get_width()) / 2, 460))
        window.blit(self.cinco, ((self.largura_janela - self.cinco.get_width()) / 2, 560))

        pygame.display.update()

    def atualiza(self, jogo):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            # Analisa a posicao do mouse
            if mouse_point.colliderect(self.rect_um):
                self.um = pygame.font.Font(self.font, 50).render('MELHOR DE UM', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_um):
                self.um = pygame.font.Font(self.font, 40).render('MELHOR DE UM', True, (255, 140, 0))
            if mouse_point.colliderect(self.rect_tres):
                self.tres = pygame.font.Font(self.font, 50).render('MELHOR DE TRÊS', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_tres):
                self.tres = pygame.font.Font(self.font, 40).render('MELHOR DE TRÊS', True, (255, 140, 0))
            if mouse_point.colliderect(self.rect_cinco):
                self.cinco = pygame.font.Font(self.font, 50).render('MELHOR DE CINCO', True, (255, 255, 0))
            if not mouse_point.colliderect(self.rect_cinco):
                self.cinco = pygame.font.Font(self.font, 40).render('MELHOR DE CINCO', True, (255, 140, 0))
            # Analisa clique do mouse
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_um):
                    self.som.play()
                    jogo.melhor_de_ = 1
                    return TelaJogo(self.largura_janela, self.altura_janela)
                elif mouse_point.colliderect(self.rect_tres):
                    self.som.play()
                    jogo.melhor_de_ = 3
                    return TelaJogo(self.largura_janela, self.altura_janela)
                elif mouse_point.colliderect(self.rect_cinco):
                    self.som.play()
                    jogo.melhor_de_ = 5
                    return TelaJogo(self.largura_janela, self.altura_janela)

        return self


class TelaJogo:
    def __init__(self, largura_janela, altura_janela):
        #  Inicializa parametros da tela
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        #  Inicializa parametros de sprites
        self.blocos = pygame.sprite.Group()
        self.bombas = pygame.sprite.Group()
        self.explosoes = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.jogadores = pygame.sprite.Group()
        self.sprite_size = [50, 50]  # Tamanho horizontal e vertical em pixels das sprites
        #  Inicializa parametros do mapa
        self.n_blocos_internos = [6, 5]  # N horizontal e N vertical
        self.n_blocos_quebraveis = 60
        self.n_estoque_pu = 8
        self.n_explosao_pu = 8
        self.n_velocidade_pu = 4
        self.n_chute_pu = 2
        self.largura_mapa = (self.n_blocos_internos[0] * 2 + 3) * self.sprite_size[0]
        self.altura_mapa = (self.n_blocos_internos[1] * 2 + 3) * self.sprite_size[1]
        self.mapa = Mapa(self)
        self.gera_paredes_inquebraveis()
        self.gera_paredes_quebraveis()  # Caso a quantidade exeda o limite, o jogo quebra
        self.gera_powerups()
        self.gera_jogadores()
        

    def gera_paredes_inquebraveis(self):
        for blocks in range(3 + 2 * self.n_blocos_internos[0]):  # Desenha os blocos inquebraveis ao norte
            x = self.sprite_size[0] * blocks
            y = 0
            self.blocos.add(UnbreakBlock(self, x, y))
        for blocks in range(1, 2 + 2 * self.n_blocos_internos[1]):  # ... ao oeste
            x = 0
            y = self.sprite_size[1] * blocks
            self.blocos.add(UnbreakBlock(self, x, y))
        for blocks in range(1, 2 + 2 * self.n_blocos_internos[1]):  # ... ao leste
            x = self.sprite_size[0] * (self.n_blocos_internos[0] * 2 + 2)
            y = self.sprite_size[1] * blocks
            self.blocos.add(UnbreakBlock(self, x, y))
        for blocks in range(3 + 2 * self.n_blocos_internos[0]):  # ... ao sul
            x = self.sprite_size[0] * blocks
            y = self.sprite_size[1] * (self.n_blocos_internos[1] * 2 + 2)
            self.blocos.add(UnbreakBlock(self, x, y))
        for y_unidade in range(2, 1 + self.n_blocos_internos[1] * 2, 2):  # ... internos
            y = y_unidade * self.sprite_size[1]
            for x_unidade in range(2, 1 + self.n_blocos_internos[0] * 2, 2):
                x = x_unidade * self.sprite_size[0]
                self.blocos.add(UnbreakBlock(self, x, y))


    def gera_paredes_quebraveis(self):
        for i in range(self.n_blocos_quebraveis):
            bool = True
            while bool:
                x_unidade = random.randint(1, 1 + 2 * self.n_blocos_internos[0])
                if x_unidade == 1:
                    y_unidade = random.randint(3, 2 * self.n_blocos_internos[1] - 1)
                elif x_unidade == 2:
                    y_unidade = random.randint(2, 2 * self.n_blocos_internos[1])
                elif x_unidade == 2 * self.n_blocos_internos[0]:
                    y_unidade = random.randint(1, 2 * self.n_blocos_internos[1])
                elif x_unidade == 2 * self.n_blocos_internos[0] + 1:
                    y_unidade = random.randint(1, 2 * self.n_blocos_internos[1] - 1)
                else:
                    y_unidade = random.randint(1, self.n_blocos_internos[1] * 2 + 1)
                x = x_unidade * self.sprite_size[0]
                y = y_unidade * self.sprite_size[1]

                bloco = BreakBlock(self, x, y)

                if len(pygame.sprite.spritecollide(bloco, self.blocos, False)) == 0:
                    bool = False
            self.blocos.add(bloco)

    def gera_powerups(self):
        for a in range(4):
            if a == 0:
                tipo = 'estoque'
                quantidade = self.n_estoque_pu
            elif a == 1:
                tipo = 'explosao'
                quantidade = self.n_explosao_pu
            elif a == 2:
                tipo = 'velocidade'
                quantidade = self.n_velocidade_pu
            elif a == 3:
                tipo = 'chute'
                quantidade = self.n_chute_pu
            for i in range(quantidade):
                bool = True
                while bool:
                    x_unidade = random.randint(1, 1 + 2 * self.n_blocos_internos[0])
                    y_unidade = random.randint(1, 1 + 2 * self.n_blocos_internos[1])

                    x = x_unidade * self.sprite_size[0]
                    y = y_unidade * self.sprite_size[1]

                    powerup = PowerUp(self, x, y, tipo)

                    if len(pygame.sprite.spritecollide(powerup, self.powerups, False)) == 0 and len(pygame.sprite.spritecollide(powerup, self.blocos, False)) > 0:
                        if pygame.sprite.spritecollide(powerup, self.blocos, False)[0].eh_quebravel:
                            bool = False
                self.powerups.add(powerup)
        
    def gera_jogadores(self):
        self.jogador_um = PlayerWhite(self, self.sprite_size[0], self.sprite_size[1])
        self.jogadores.add(self.jogador_um)
        self.jogador_dois = PlayerBlack(self, (self.n_blocos_internos[0] * 2 + 1) * self.sprite_size[0], (self.n_blocos_internos[1] * 2 + 1) * self.sprite_size[1])
        self.jogadores.add(self.jogador_dois)

    def desenha(self, window):
        window.fill((0, 0 ,0))
        self.mapa.fill((0,100,0))
        # Desenha os grupos
        self.powerups.draw(self.mapa)
        self.blocos.draw(self.mapa)
        self.bombas.draw(self.mapa)
        self.explosoes.draw(self.mapa)
        # Desenha os players
        jogadores = self.jogadores.sprites()
        while len(jogadores) > 0:
            menor_y = float('inf')
            for player in jogadores:
                if player.rect.y < menor_y:
                    menor_y = player.rect.y
                    player_atras = player
            self.mapa.blit(player_atras.image, (player_atras.rect.x, player_atras.rect.y - (player_atras.height - self.sprite_size[1])))
            jogadores.remove(player_atras)
        window.blit(self.mapa, ((self.largura_janela - self.mapa.width) / 2, (self.altura_janela - self.mapa.height) / 2))
        pygame.display.update()


    def atualiza(self, jogo):
        if len(self.jogadores.sprites()) < 2:
            if len(self.jogadores.sprites()) > 0:
                if self.jogadores.sprites()[0].cor == 'white':
                    jogo.vitorias_branco += 1
                    return TelaScore(self.largura_janela, self.altura_janela)
                elif self.jogadores.sprites()[0].cor == 'black':
                    jogo.vitorias_preto += 1
                    return TelaScore(self.largura_janela, self.altura_janela)
            else:
                return TelaScore(self.largura_janela, self.altura_janela)
        self.tick_atual = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
            elif event.type == pygame.KEYDOWN:
                # Jogador 1
                if event.key == pygame.K_w and self.jogador_um.estado[0] != 'morte':
                    self.jogador_um.estado = ['norte', True]
                elif event.key == pygame.K_a and self.jogador_um.estado[0] != 'morte':
                    self.jogador_um.estado = ['oeste', True]
                elif event.key == pygame.K_s and self.jogador_um.estado[0] != 'morte':
                    self.jogador_um.estado = ['sul', True]
                elif event.key == pygame.K_d and self.jogador_um.estado[0] != 'morte':
                    self.jogador_um.estado = ['leste', True]
                elif event.key == pygame.K_SPACE and self.jogador_um.estado[0] != 'morte':
                    self.jogador_um.flag_bomba = False
                    self.jogador_um.cria_bomba(self)
                # Jogador 2
                elif event.key == pygame.K_UP and self.jogador_dois.estado[0] != 'morte':
                    self.jogador_dois.estado = ['norte', True]
                elif event.key == pygame.K_LEFT and self.jogador_dois.estado[0] != 'morte':
                    self.jogador_dois.estado = ['oeste', True]
                elif event.key == pygame.K_DOWN and self.jogador_dois.estado[0] != 'morte':
                    self.jogador_dois.estado = ['sul', True]
                elif event.key == pygame.K_RIGHT and self.jogador_dois.estado[0] != 'morte':
                    self.jogador_dois.estado = ['leste', True]
                elif event.key == pygame.K_RSHIFT and self.jogador_dois.estado[0] != 'morte':
                    self.jogador_dois.flag_bomba = False
                    self.jogador_dois.cria_bomba(self)

            elif event.type == pygame.KEYUP:
                # Jogador1
                if event.key == pygame.K_w and self.jogador_um.estado[0] == 'norte':
                    self.jogador_um.estado[1] = False
                elif event.key == pygame.K_a and self.jogador_um.estado[0] == 'oeste':
                    self.jogador_um.estado[1] = False
                elif event.key == pygame.K_s and self.jogador_um.estado[0] == 'sul':
                    self.jogador_um.estado[1] = False
                elif event.key == pygame.K_d and self.jogador_um.estado[0] == 'leste':
                    self.jogador_um.estado[1] = False
                # Jogador 2
                if event.key == pygame.K_UP and self.jogador_dois.estado[0] == 'norte':
                    self.jogador_dois.estado[1] = False
                elif event.key == pygame.K_LEFT and self.jogador_dois.estado[0] == 'oeste':
                    self.jogador_dois.estado[1] = False
                elif event.key == pygame.K_DOWN and self.jogador_dois.estado[0] == 'sul':
                    self.jogador_dois.estado[1] = False
                elif event.key == pygame.K_RIGHT and self.jogador_dois.estado[0] == 'leste':
                    self.jogador_dois.estado[1] = False
                    
        self.jogadores.update(self)
        self.bombas.update(self)
        self.explosoes.update(self)
        self.blocos.update(self)

        return self


class TelaVicWhite:  # Tela de vitoria do player branco
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.VICWHITE = pygame.transform.scale(pygame.image.load('jogo/img/vic_white.jpg'), (800, 600))


    def desenha(self, window):
        window.fill((0, 0, 0))
        window.blit(self.VICWHITE, ((self.largura_janela - 800) / 2, (self.altura_janela - 600) / 2))
        pygame.display.update()


    def atualiza(self, jogo):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_KP_ENTER:
                    jogo.melhor_de_ = 0
                    jogo.vitorias_branco = 0
                    jogo.vitorias_preto = 0
                    return TelaMenu(self.largura_janela, self.altura_janela)
        return self
            

class TelaVicBlack:  # Tela de vitoria do player pretos
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.VICBLACK = pygame.transform.scale(pygame.image.load('jogo/img/vic_black.jpg'), (800, 600))


    def desenha(self, window):
        window.fill((0, 0, 0))
        window.blit(self.VICBLACK, ((self.largura_janela - 800) / 2, (self.altura_janela - 600) / 2))
        pygame.display.update()


    def atualiza(self, jogo):
        # Reinicia o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_KP_ENTER:
                    jogo.melhor_de_ = 0
                    jogo.vitorias_branco = 0
                    jogo.vitorias_preto = 0
                    return TelaMenu(self.largura_janela, self.altura_janela)
        return self
    

class TelaScore:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        
        self.IMG_TROFEU = pygame.image.load('jogo/img/trofeu.png')
        self.IMG_TROFEU_SCALE = pygame.transform.scale(self.IMG_TROFEU, (50,50))

        self.BOMB_SCORE = pygame.image.load('jogo/img/bomb_score.png')
        

        self.PLAYER_1_TROFEU = 0
        self.PLAYER_2_trofeu = 0

        self.font = 'jogo/img/fonte.ttf'
        self.PLAYER1 = pygame.font.Font(self.font, 50).render('PLAYER 1: ', True, (255, 140, 0))
        self.PLAYER2 = pygame.font.Font(self.font, 50).render('PLAYER 2: ', True, (255, 140, 0))


    def desenha(self, window):
        window.fill((0, 0, 255)) 

        window.blit(self.BOMB_SCORE,(0,150))

        # desenha quantidade de troféus de cada player
        for trofeu_1 in range(self.PLAYER_1_TROFEU):
            window.blit(self.IMG_TROFEU_SCALE, (650 + (trofeu_1 * 60),30))
        for trofeu_2 in range(self.PLAYER_2_trofeu):
            window.blit(self.IMG_TROFEU_SCALE, (650 + (trofeu_2 * 60),100))

        window.blit(self.PLAYER1, (200,30))
        window.blit(self.PLAYER2, (200,100))

        pygame.display.update()


    def atualiza(self, jogo):
        self.PLAYER_1_TROFEU = jogo.vitorias_branco
        self.PLAYER_2_trofeu = jogo.vitorias_preto
        if jogo.vitorias_branco == jogo.melhor_de_ / 2 + 0.5:
            tela_atual = TelaVicWhite(self.largura_janela, self.altura_janela)
        elif jogo.vitorias_preto == jogo.melhor_de_ / 2 + 0.5:
            tela_atual = TelaVicBlack(self.largura_janela, self.altura_janela)
        else:
            tela_atual = TelaJogo(self.largura_janela, self.altura_janela)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_KP_ENTER:
                    return tela_atual
        return self