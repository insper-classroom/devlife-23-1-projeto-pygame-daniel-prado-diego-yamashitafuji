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

        self.font = 'jogo/img/fonte.ttf'

        self.BATTLE = pygame.font.Font(self.font, 60).render('BATTLE MODE', True, 	(255, 140, 0))
        self.CREDITS = pygame.font.Font(self.font, 60).render('CREDITS', True, 	(255, 140, 0))
        self.EXIT = pygame.font.Font(self.font, 60).render('EXIT', True, 	(255, 140, 0))
        #self.BATTLE_w, self.BATTLE_h = self.BATTLE.get_size()
        self.rect_BATTLE = self.BATTLE.get_rect()
        self.rect_BATTLE.x = 300
        self.rect_BATTLE.y = 360
        #self.BATTLE_x, self.BATTLE_y = 300 , self.altura_janela / 2
        #self.CREDITS_w, self.CREDITS_h = self.CREDITS.get_size()
        self.rect_CREDITS = self.CREDITS.get_rect()
        self.rect_CREDITS.x = 300
        self.rect_CREDITS.y = 460
        #self.EXIT_w, self.EXIT_h = self.EXIT.get_size()
        #self.EXIT_x, self.EXIT_y = 300, 200 + self.altura_janela / 2
        self.rect_EXIT = self.EXIT.get_rect()
        self.rect_EXIT.x = 300
        self.rect_EXIT.y = 560

    def desenha(self, window):
        window.fill((0, 0, 255))
        window.blit(self.TITLE, (self.TITLE_x, 20))
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
                return -1
    
            if mouse_point.colliderect(self.rect_BATTLE):
                self.BATTLE = pygame.font.Font(self.font, 70).render('BATTLE MODE', True, 		(255, 255, 0))
            if not mouse_point.colliderect(self.rect_BATTLE):
                self.BATTLE = pygame.font.Font(self.font, 60).render('BATTLE MODE', True, 	(255, 140, 0))
            if mouse_point.colliderect(self.rect_CREDITS):
                self.CREDITS = pygame.font.Font(self.font, 70).render('CREDITS', True, 	(255, 255, 0))
            if not mouse_point.colliderect(self.rect_CREDITS):
                self.CREDITS = pygame.font.Font(self.font, 60).render('CREDITS', True, 	(255, 140, 0))
            if mouse_point.colliderect(self.rect_EXIT):
                self.EXIT = pygame.font.Font(self.font, 70).render('EXIT', True, 	(255, 255, 0))
            if not mouse_point.colliderect(self.rect_EXIT):
                self.EXIT = pygame.font.Font(self.font, 60).render('EXIT', True, 	(255, 140, 0))
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if mouse_point.colliderect(self.rect_BATTLE):
                    som_inicial.play()
                    #return 1
                if mouse_point.colliderect(self.rect_CREDITS):
                    som_inicial.play()
                    #return 2
                if mouse_point.colliderect(self.rect_EXIT):
                    return -1
        return 0
    
class TelaJogo:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.bloco_inquebravel = pygame.image.load('assets/bloco_inquebravel.png')
        self.bloco_quebravel = pygame.image.load('assets/bloco_quebravel.png')


        self.blocks = pygame.sprite.Group()

        self.sprite_w, self.sprite_h = 50, 50  # Tamanho horizontal e vertical em pixels das sprites, lembrando que as sprites sao quadrados
    
        self.unbreakblock_img = pygame.transform.scale(pygame.image.load('assets/blocoinquebravel.png'), (self.sprite_w, self.sprite_h))
        self.breakblock_img = pygame.transform.scale(pygame.image.load('assets/blocoquebravel.png'), (self.sprite_w, self.sprite_h))

        self.origin_x, self.origin_y = (largura_janela - self.sprite_w * 13) / 2, (altura_janela - self.sprite_h * 13) / 2

        self.gera_paredes_inquebraveis()
        
        self.gera_paredes_quebraveis(40)  # Deve ser menor que 90
        
    def desenha(self, window):
        window.fill((0,100,0))
        self.blocks.draw(window)
        pygame.display.update()

    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
        return 1


    def gera_paredes_inquebraveis(self):
        for blocks in range(13):  # Desenha os blocos inquebraveis ao norte
            x = self.origin_x + self.sprite_w * blocks

            y = self.origin_y
            self.blocks.add(UnbreakBlock(x, y, self.unbreakblock_img))

        for blocks in range(1, 12):  # ... ao oeste
            x = self.origin_x
            y = self.origin_y + self.sprite_h * blocks

            self.blocks.add(UnbreakBlock(x, y, self.unbreakblock_img))

        for blocks in range(1, 12):  # ... ao leste
            x = self.origin_x + self.sprite_w * 12
            y = self.origin_y + self.sprite_h * blocks

            self.blocks.add(UnbreakBlock(x, y, self.unbreakblock_img))
        
        for blocks in range(13):  # ... ao sul
            x = self.origin_x + self.sprite_w * blocks

            y = self.origin_y + self.sprite_h * 12
            self.blocks.add(UnbreakBlock(x, y ,self.unbreakblock_img))

        for y in range(2, 11, 2):
            for x in range(2, 11, 2):
                self.blocks.add(UnbreakBlock(self.origin_x + x * self.sprite_w, self.origin_y + y * self.sprite_h, self.unbreakblock_img))


    def gera_paredes_quebraveis(self, n_paredes):
        for blocks in range(n_paredes):
            bool = True
            while bool:
                x_unit = random.randint(1, 11)
                y_unit = random.randint(1, 11)
                block = BreakBlock(self.origin_x + x_unit * self.sprite_w, self.origin_y + y_unit * self.sprite_h, self.breakblock_img)

                if len(pygame.sprite.spritecollide(block, self.blocks, False)) == 0:
                    bool = False
            self.blocks.add(block)