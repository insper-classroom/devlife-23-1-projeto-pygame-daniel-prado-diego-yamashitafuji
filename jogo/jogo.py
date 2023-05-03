import pygame
from telas import *
from telajogo import TelaJogo


class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_janela = 1920
        self.altura_janela = 1080
        self.window = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        self.melhor_de_ = 0  # esta variavel é referente modalidade do jogo, melhor de 1, 3 ou 5
        self.vitorias_branco = 0
        self.vitorias_preto = 0

    def roda(self):
        tela_atual = TelaJogo(self.largura_janela, self.altura_janela)

        rodando = True
        while rodando:
            tela_atual = tela_atual.atualiza()
            if tela_atual == 'exit':
                rodando = False
                pygame.quit()
            else:
                tela_atual.desenha(self.window)


if True:
    Jogo().roda()