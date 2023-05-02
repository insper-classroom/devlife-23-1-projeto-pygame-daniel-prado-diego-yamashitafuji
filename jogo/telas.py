import pygame
import random
from sprites import *

class TelaMenu:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.TITLE = pygame.image.load('assets/bomber_title.png')
        self.TITLE_w, self.TITLE_h = self.TITLE.get_size()
        self.TITLE_x, self.TITLE_y = ((self.largura_janela - self.TITLE_w) / 2, 0)    

        self.BOMB_INICIAL = pygame.image.load('jogo/img/bomb_inicial.png')
        self.BOMB_INICIAL_SCALE = pygame.transform.scale(self.BOMB_INICIAL, (275,275))

        self.font = 'jogo/img/fonte.ttf'

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

    def atualiza(self):
        som_inicial = pygame.mixer.Sound('jogo/img/som_inicial.wav')
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
    
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
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_BATTLE):
                    som_inicial.play()
                    return TelaJogo(self.largura_janela, self.altura_janela)
                if mouse_point.colliderect(self.rect_CREDITS):
                    som_inicial.play()
                    return TelasCredito(self.largura_janela, self.altura_janela)
                if mouse_point.colliderect(self.rect_EXIT):
                    return 'exit'
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
        self.n_blocos_quebraveis = 90
        self.n_estoque_pu = 6
        self.n_explosao_pu = 6
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


    def atualiza(self):
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
                elif event.key == pygame.K_RCTRL and self.jogador_dois.estado[0] != 'morte':
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

    
    def atualiza(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_VOLTAR):
                    return TelaMenu(self.largura_janela, self.altura_janela)
        return self
    

    

class TelaScore:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        
        self.IMG_TROFEU = pygame.image.load('jogo/img/trofeu.png')
        self.IMG_TROFEU_SCALE = pygame.transform.scale(self.IMG_TROFEU, (50,50))

        self.BOMB_SCORE = pygame.image.load('jogo/img/bomb_score.png')
        

        self.PLAYER_1_TROFEU = 3
        self.PLAYER_2_trofeu = 1

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


    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
        return self