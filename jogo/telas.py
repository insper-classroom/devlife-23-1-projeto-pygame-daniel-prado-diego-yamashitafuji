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
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bombas = pygame.sprite.Group()  # Tamanho horizontal e vertical em pixels das sprites
        self.sprite_size = [50, 50]
        #  Inicializa parametros do mapa
        self.n_blocos_internos_x, self.n_blocos_internos_y = 6, 5
        self.mapa = Mapa((self.n_blocos_internos_x * 2 + 3) * self.sprite_size[0], (self.n_blocos_internos_y * 2 + 3) * self.sprite_size[1])
        self.gera_paredes_inquebraveis(self.n_blocos_internos_x, self.n_blocos_internos_y)
        
        self.gera_paredes_quebraveis(0, self.n_blocos_internos_x, self.n_blocos_internos_y)  # Caso a quantidade exeda o limite, o jogo quebra

        self.gera_jogadores()
        
    def desenha(self, window):
        window.fill((0, 0 ,0))
        self.mapa.fill((0,100,0))
        # Desenha os blocos
        self.bombas.draw(self.mapa)
        self.blocks.draw(self.mapa)
        # Desenha os players
        for player in self.players.sprites():
            self.mapa.blit(player.image, (player.rect.x, player.rect.y - (player.height - self.sprite_size[1])))
        window.blit(self.mapa, ((self.largura_janela - self.mapa.width) / 2, (self.altura_janela - self.mapa.height) / 2))
        pygame.display.update()


    def atualiza(self):
        self.tick_atual = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player_um.direcao = 'norte'
                    self.player_um.esta_movendo = True
                elif event.key == pygame.K_a:
                    self.player_um.direcao = 'oeste'
                    self.player_um.esta_movendo = True
                elif event.key == pygame.K_s:
                    self.player_um.direcao = 'sul'
                    self.player_um.esta_movendo = True
                elif event.key == pygame.K_d:
                    self.player_um.direcao = 'leste'
                    self.player_um.esta_movendo = True
                elif event.key == pygame.K_SPACE:
                    self.bombas.add(Bomb(self.player_um.rect.x, self.player_um.rect.y, self.sprite_s))

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w and self.player_um.direcao == 'norte':
                    self.player_um.esta_movendo = False
                elif event.key == pygame.K_a and self.player_um.direcao == 'oeste':
                    self.player_um.esta_movendo = False
                elif event.key == pygame.K_s and self.player_um.direcao == 'sul':
                    self.player_um.esta_movendo = False
                elif event.key == pygame.K_d and self.player_um.direcao == 'leste':
                    self.player_um.esta_movendo = False
                    
        self.players.update(self.tick_atual)
        self.bombas.update(self.tick_atual)
        return self


    def gera_paredes_inquebraveis(self, n_blocos_internos_x, n_blocos_internos_y):
        for blocks in range(3 + 2 * n_blocos_internos_x):  # Desenha os blocos inquebraveis ao norte
            x = self.sprite_size[0] * blocks
            y = 0
            self.blocks.add(UnbreakBlock(x, y, self.sprite_size))
        for blocks in range(1, 2 + 2 * n_blocos_internos_y):  # ... ao oeste
            x = 0
            y = self.sprite_size[1] * blocks
            self.blocks.add(UnbreakBlock(x, y, self.sprite_size))
        for blocks in range(1, 2 + 2 * n_blocos_internos_y):  # ... ao leste
            x = self.sprite_size[0] * (n_blocos_internos_x * 2 + 2)
            y = self.sprite_size[1] * blocks
            self.blocks.add(UnbreakBlock(x, y, self.sprite_size))
        for blocks in range(3 + 2 * n_blocos_internos_x):  # ... ao sul
            x = self.sprite_size[0] * blocks
            y = self.sprite_size[1] * (n_blocos_internos_y * 2 + 2)
            self.blocks.add(UnbreakBlock(x, y, self.sprite_size))
        for y_unidade in range(2, 1 + n_blocos_internos_y * 2, 2):  # ... internos
            y = y_unidade * self.sprite_size[1]
            for x_unidade in range(2, 1 + n_blocos_internos_x * 2, 2):
                x = x_unidade * self.sprite_size[0]
                self.blocks.add(UnbreakBlock(x, y, self.sprite_size))


    def gera_paredes_quebraveis(self, n_paredes, n_blocos_internos_x, n_blocos_internos_y):
        for blocks in range(n_paredes):
            bool = True
            while bool:
                x_unidade = random.randint(1, 1 + 2 * n_blocos_internos_x)
                if x_unidade == 1:
                    y_unidade = random.randint(3, 2 * n_blocos_internos_y - 1)
                elif x_unidade == 2:
                    y_unidade = random.randint(2, 2 * n_blocos_internos_y)
                elif x_unidade == 2 * n_blocos_internos_x:
                    y_unidade = random.randint(1, 2 * n_blocos_internos_y)
                elif x_unidade == 2 * n_blocos_internos_x + 1:
                    y_unidade = random.randint(1, 2 * n_blocos_internos_y - 1)
                else:
                    y_unidade = random.randint(1, 11)
                x = x_unidade * self.sprite_size[0]
                y = y_unidade * self.sprite_size[1]

                block = BreakBlock(x, y, self.sprite_size)

                if len(pygame.sprite.spritecollide(block, self.blocks, False)) == 0:
                    bool = False
            self.blocks.add(block)


    def gera_jogadores(self):
        self.player_um = PlayerWhite(self.sprite_size[0], self.sprite_size[1], self.sprite_size, self.blocks)
        self.players.add(self.player_um)
        

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
        self.DIEGO = pygame.font.Font(self.font, 35).render('DIEGO', True, (255, 140, 0))


    def desenha(self, window):
        window.fill((0, 0, 255))
        window.blit(self.IMAGEM_ICON_SCALE, (60,450))
        window.blit(self.IMAGEM_ICON_SCALE, (60,550))
        window.blit(self.BOMB_FINAL, (360,20))
        window.blit(self.GRUPO, (50, 370))
        window.blit(self.DANIEL, (120, 460))
        window.blit(self.DIEGO, (120, 560))

        pygame.display.update()


    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
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
    
    

    
