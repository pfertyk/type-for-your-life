import pygame
from main import PhrasesHolder


pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode((400, 300))
done = False
font_color = (0, 0, 0)
font_color_finished = (0, 0, 255)
background_color = (255, 255, 255)

phrase = 'Hello world!'
phrase_left = phrase


def accept_char(char, phrase_, phrase_left_):
    global phrase_left
    phrase_left = phrase_left_
    if not phrase_left_:
        global done
        done = True


def reject_char(char):
    print('Rejected', char)


phrase_holder = PhrasesHolder(reject_char, accept_char)
phrase_holder.add_phrase(phrase)

background = pygame.Surface(screen.get_size())
background = background.convert()

font = pygame.font.Font(None, 36)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.unicode:
                phrase_holder.send_char(event.unicode)

    background.fill(background_color)

    text = font.render(phrase, 1, font_color_finished)
    background.blit(text, text.get_rect())

    text_left = font.render(phrase_left, 1, font_color)
    text_left_pos = text_left.get_rect()
    text_left_pos.topright = text.get_rect().topright
    background.blit(text_left, text_left_pos)

    screen.blit(background, (0, 0))
    pygame.display.flip()
