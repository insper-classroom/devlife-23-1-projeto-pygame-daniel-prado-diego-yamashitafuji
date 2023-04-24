import pygame
from telas import *


class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_janela = 1280
        self.altura_janela = 720
        self.window = pygame.display.set_mode((self.largura_janela, self.altura_janela))

        self.telas = [TelaMenu(self.largura_janela,self.altura_janela), TelaJogo(self.largura_janela, self.altura_janela)]
        self.ind_tela_atual = 0


    def roda(self):

        rodando = True
        while rodando:
            
            tela_atual = self.telas[self.ind_tela_atual]

            self.ind_tela_atual = tela_atual.atualiza()

            if self.ind_tela_atual == -1:
                rodando = False
                pygame.quit()

            else:
                tela_atual.desenha(self.window)


if True:
    Jogo().roda()
