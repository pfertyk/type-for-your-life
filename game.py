import pygame
import random
from main import PhrasesHolder

WIDTH = 1280
FPS = 30


class PygamePhraseHolder:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

        available_phrases = [
            'How big?',
            'That is my fish!',
            'Nooo way...',
            'Are you still there?',
            'Gordon\'s ALIVE!',
        ]

        self.stream = []
        self.phrase_to_stream = {}

        self.phrase_holder = PhrasesHolder(self.reject_char, self.accept_char)

        while len(self.phrase_holder.phrases) != 2:
            phrase = random.choice(available_phrases)

            try:
                self.phrase_holder.add_phrase(phrase)
                self.add_to_stream(phrase)
            except ValueError:
                print('Adding a new phrase failed, retrying')

        self.done = False

    def add_to_stream(self, phrase):
        if self.stream:
            offset = self.stream[-1][2][1]
        else:
            offset = WIDTH//2

        background_text = self.font.render(phrase, 1, (127, 127, 127))
        text = self.font.render(phrase, 1, (0, 0, 0))

        topleft = (offset, 300)

        item = [background_text, text, topleft]
        self.phrase_to_stream[phrase] = item

        self.stream.append(item)

    def accept_char(self, char, phrase, phrase_left):
        item = self.phrase_to_stream[phrase]
        item[1] = self.font.render(phrase_left, 1, (0, 0, 0))
        if not phrase_left:
            self.stream.remove(item)
        if not self.stream:
            self.done = True

    def reject_char(self, char):
        print('Rejected', char)

    def draw(self, background):
        for item in self.stream:
            phrase, phrase_left, topleft = item
            background.blit(phrase, topleft)
            rect0 = phrase.get_rect(topleft=topleft)
            rect = phrase_left.get_rect(topright=rect0.topright)
            background.blit(phrase_left, rect)

            item[2] = (topleft[0] - 1, topleft[1])

            if item[2][0] < 0:
                print('Sorry, you lost!')
                self.done = True
                break


pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, 720))
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
    clock.tick(FPS)
