import pygame

pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode((400, 300))
done = False
font_color = (0, 0, 0)
background_color = (255, 255, 255)

phrase = 'Hello world!'

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(background_color)

font = pygame.font.Font(None, 36)
text = font.render(phrase, 1, font_color)
background.blit(text, text.get_rect())

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(background, (0, 0))
    pygame.display.flip()
