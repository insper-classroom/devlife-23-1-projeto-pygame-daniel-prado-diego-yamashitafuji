import pygame
import random
from sprites import *
from jogo.telajogo import TelaJogo

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
                    return TelaOpções(self.largura_janela, self.altura_janela)
                if mouse_point.colliderect(self.rect_CREDITS):
                    som_inicial.play()
                    return TelasCredito(self.largura_janela, self.altura_janela)
                if mouse_point.colliderect(self.rect_EXIT):
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

    
    def atualiza(self):
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
    
class TelaOpções:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.TITLE = pygame.image.load('assets/bomber_title.png')
        self.TITLE_w, self.TITLE_h = self.TITLE.get_size()
        self.TITLE_x, self.TITLE_y = ((self.largura_janela - self.TITLE_w) / 2, 0)

        self.font = 'jogo/img/fonte.ttf'

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

    def atualiza(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_point = pygame.Rect(mouse_x, mouse_y, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            
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



        return self
    

class TelaVicWhite:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.VICWHITE = pygame.image.load('jogo/img/vic_white.jpg')


    def desenha(self, window):
        window.fill((0, 0, 0))
        window.blit(self.VICWHITE, (340, 100))
        pygame.display.update()


    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
        return self
            
class TelaVicBlack:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.VICBLACK = pygame.image.load('jogo/img/vic_black.jpg')


    def desenha(self, window):
        window.fill((0, 0, 0))
        window.blit(self.VICBLACK, (340, 100))
        pygame.display.update()


    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
        return self