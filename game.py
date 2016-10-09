import pygame
from main import PhrasesHolder


pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode((400, 300))
done = False
font_color = (0, 0, 0)
background_color = (255, 255, 255)

phrase = 'Hello world!'


def accept_char(char, phrase, phrase_left):
    print('Accepted', char)
    if not phrase_left:
        global done
        done = True


def reject_char(char):
    print('Rejected', char)


phrase_holder = PhrasesHolder(reject_char, accept_char)
phrase_holder.add_phrase(phrase)

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
        elif event.type == pygame.KEYDOWN:
            if event.unicode:
                phrase_holder.send_char(event.unicode)

    screen.blit(background, (0, 0))
    pygame.display.flip()
