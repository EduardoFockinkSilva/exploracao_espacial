import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Teste Pygame')

executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
