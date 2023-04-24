import pygame
import os

pygame.init()

pygame.display.set_caption('Bomberman')

cor_fundo = (255,255,255)
comprimento = 1280
altura = 720
fps = 60

window = pygame.display.set_mode((comprimento,altura))
fundo_imagem = pygame.image.load('jogo/img/fundo.png')
window.blit(fundo_imagem, (0,0))
pygame.display.update()


def main(window):
    clock = pygame.time.Clock()

    game = True
    while game:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break
      

    pygame.quit()
    quit()
   
    
if __name__ == "__main__":
    main(window)
