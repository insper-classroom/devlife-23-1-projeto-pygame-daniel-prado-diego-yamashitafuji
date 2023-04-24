import pygame
from telas import *


class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_janela = 1280
        self.altura_janela = 720
        self.window = pygame.display.set_mode((self.largura_janela, self.altura_janela))

        self.telas = [TelaMenu(self.largura_janela,self.altura_janela)]
        self.ind_tela_atual = 0


    def roda(self):

        tela_atual = self.telas[self.ind_tela_atual]

        while tela_atual.atualiza():
            tela_atual.desenha(self.window)

        pygame.quit()

if True:
    Jogo().roda()