import pygame

class TelaMenu:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.TITLE = pygame.image.load('assets/bomber_title.png')
        self.TITLE_w, self.TITLE_h = self.TITLE.get_size()
        self.TITLE_x, self.TITLE_y = (self.largura_janela - self.TITLE_w) / 2, 0

        self.font = pygame.font.get_default_font()

        self.START = pygame.font.Font(self.font, 60).render('START', True, (255, 255, 255))
        self.START_w, self.START_h = self.START.get_size()
        self.START_x, self.START_y = (self.largura_janela - self.START.get_width()) / 2, self.altura_janela / 2

    def desenha(self, window):
        window.fill((0, 100, 0))
        window.blit(self.TITLE, (self.TITLE_x, self.TITLE_y))
        window.blit(self.START, (self.START_x, self.START_y))
        pygame.display.update()

    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.START_x < mouse_x < self.START_x + self.START_w and self.START_y < mouse_y < self.START_y + self.START_h:
                    return 1
        return 0
    
class TelaJogo:
    def __init__(self, largura_janela, altura_janela):
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

        self.bloco_inquebravel = pygame.image.load('assets/bloco_inquebravel.png')
        self.bloco_quebravel = pygame.image.load('assets/bloco_quebravel.png')
    
