import pygame
import random
from main import PhrasesHolder


class PygamePhraseHolder:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

        self.abc = {}

        available_phrases = [
            'How big?',
            'That is my fish!',
            'Nooo way...',
            'Are you still there?',
            'Gordon\'s ALIVE!',
        ]

        self.phrase_holder = PhrasesHolder(self.reject_char, self.accept_char)

        while len(self.phrase_holder.phrases) != 4:
            phrase = random.choice(available_phrases)

            try:
                self.phrase_holder.add_phrase(phrase)
                self.abc[phrase] = phrase
            except ValueError:
                print('Adding a new phrase failed, retrying')

        self.done = False

    def accept_char(self, char, phrase, phrase_left):
        self.abc[phrase] = phrase_left
        if not phrase_left:
            self.abc.pop(phrase)
        if not self.abc:
            self.done = True

    def reject_char(self, char):
        print('Rejected', char)

    def draw(self, background):
        for i, phrase in enumerate(self.abc.keys()):
            if phrase == self.phrase_holder.current_phrase:
                background_color = (255, 180, 0)
            else:
                background_color = None
            text = self.font.render(phrase, 1, (0, 222, 255), background_color)
            text_pos = text.get_rect()
            text_pos.topleft = (0, i * 40)
            background.blit(text, text_pos)

            text_left = self.font.render(self.abc[phrase], 1, (0, 0, 0))
            text_left_pos = text_left.get_rect()
            text_left_pos.topright = text_pos.topright
            background.blit(text_left, text_left_pos)


pygame.init()
pygame.mixer.quit()

screen = pygame.display.set_mode((400, 300))
background_color = (255, 255, 255)

background = pygame.Surface(screen.get_size())
background = background.convert()

pygame_phrase_holder = PygamePhraseHolder()

done = False

while not done:
    if pygame_phrase_holder.done:
        done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.unicode:
            pygame_phrase_holder.phrase_holder.send_char(event.unicode)

    background.fill(background_color)
    pygame_phrase_holder.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.flip()
