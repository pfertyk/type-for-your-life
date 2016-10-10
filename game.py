import pygame
import random
from main import PhrasesHolder


class PygamePhraseHolder:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

        available_phrases = ['How big?', 'That is my fish!', 'Nooo way...']
        self.phrase_holder = PhrasesHolder(self.reject_char, self.accept_char)
        phrase = random.choice(available_phrases)
        self.phrase_holder.add_phrase(phrase)

        self.phrase = self.phrase_left = phrase

        self.done = False

    def accept_char(self, char, phrase, phrase_left):
        self.phrase_left = phrase_left
        if not phrase_left:
            self.done = True

    def reject_char(self, char):
        print('Rejected', char)

    def draw(self, background):
        text = self.font.render(self.phrase, 1, (0, 0, 255))
        background.blit(text, text.get_rect())

        text_left = self.font.render(self.phrase_left, 1, (0, 0, 0))
        text_left_pos = text_left.get_rect()
        text_left_pos.topright = text.get_rect().topright
        background.blit(text_left, text_left_pos)


pygame.init()
pygame.mixer.quit()

screen = pygame.display.set_mode((400, 300))
background_color = (255, 255, 255)

background = pygame.Surface(screen.get_size())
background = background.convert()

pygame_phrase_holder = PygamePhraseHolder()

while not pygame_phrase_holder.done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.unicode:
            pygame_phrase_holder.phrase_holder.send_char(event.unicode)

    background.fill(background_color)
    pygame_phrase_holder.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.flip()
