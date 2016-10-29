import pygame
import random

from main import PhrasesHolder
import colors

WIDTH = 1280
HEIGHT = 720
FPS = 30

MAX_PHRASES = 4
FONT_SIZE = 36

NEW_PHRASE_MAX_AVAILABLE_HEIGHT = 80
NEW_PHRASE_SAFE_SPACE = 64


class Phrase:
    def __init__(self, phrase, midleft):
        self.padding = 10
        self.frame_width = 4  # TODO: extract to settings?
        self.font = pygame.font.Font(None, FONT_SIZE)

        self.full_phrase = self.font.render(
            phrase,
            1,
            colors.PHRASE_FONT_COMPLETED,
            colors.PHRASE_BACKGROUND
        )

        self.remaining_phrase = self.font.render(
            phrase, 1, colors.PHRASE_FONT_REMAINING
        )

        phrase_size = (
            self.full_phrase.get_width() + 2 * self.padding,
            self.full_phrase.get_height() + 2 * self.padding
        )

        self.frame = pygame.Rect((0, 0), phrase_size)
        self.frame.midleft = midleft

        self.topleft = self.frame.topleft
        self.text = phrase

    def update(self, phrase_left):
        self.remaining_phrase = self.font.render(
            phrase_left, 1, colors.PHRASE_FONT_REMAINING
        )

    def move(self):
        self.topleft = (self.topleft[0] - 1, self.topleft[1])
        self.frame.topleft = self.topleft

    def draw(self, background, is_active):
        if is_active:
            frame_color = colors.PHRASE_FRAME_ACTIVE
        else:
            frame_color = colors.PHRASE_FRAME_NORMAL

        pygame.draw.rect(background, colors.PHRASE_BACKGROUND, self.frame)
        pygame.draw.rect(background, frame_color, self.frame, self.frame_width)

        topleft = (
            self.topleft[0] + self.padding, self.topleft[1] + self.padding
        )

        background.blit(self.full_phrase, topleft)
        rect0 = self.full_phrase.get_rect(topleft=topleft)
        rect = self.remaining_phrase.get_rect(topright=rect0.topright)
        background.blit(self.remaining_phrase, rect)

    def get_rect(self):
        return self.frame


class PygamePhraseHolder:
    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)

        self.available_phrases = [
            'How big?',
            'That is my fish!',
            'Nooo way...',
            'Are you still there?',
            'Gordon\'s ALIVE!',
        ]

        self.phrase_count = 0
        self.used_phrases = set()
        self.last_phrase_time = None
        self.phrase_interval = 4000

        self.stream = []
        self.phrase_to_stream = {}

        self.phrase_holder = PhrasesHolder(self.reject_char, self.accept_char)

        self.done = False

    def choose_new_word(self):
        if self.phrase_count == MAX_PHRASES:
            return

        if self.last_phrase_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_phrase_time < self.phrase_interval:
                return

        available_midleft = None

        for _ in range(10):
            available_midleft = (WIDTH, random.randint(
                NEW_PHRASE_SAFE_SPACE//2,
                NEW_PHRASE_MAX_AVAILABLE_HEIGHT - NEW_PHRASE_SAFE_SPACE//2
            ))

            rect = pygame.Rect(
                0, 0, NEW_PHRASE_SAFE_SPACE, NEW_PHRASE_SAFE_SPACE
            )
            rect.center = available_midleft

            for item in self.stream:
                if rect.colliderect(item.get_rect()):
                    break
            else:
                break
        else:
            return

        while True:
            phrase = random.choice(self.available_phrases)
            if phrase in self.used_phrases:
                print('Phrase was already used, retrying')
                continue

            try:
                self.phrase_holder.add_phrase(phrase)
                self.used_phrases.add(phrase)

                item = Phrase(phrase, available_midleft)

                self.stream.append(item)
                self.phrase_to_stream[phrase] = item
                self.phrase_count += 1
                self.last_phrase_time = pygame.time.get_ticks()
                break
            except ValueError:
                print('Adding a new phrase failed, retrying')

    def accept_char(self, char, phrase, phrase_left):
        item = self.phrase_to_stream[phrase]
        item.update(phrase_left)

        if not phrase_left:
            self.stream.remove(item)
        if not self.stream and self.phrase_count == MAX_PHRASES:
            print('Congratulations, you won!')
            self.done = True

    def reject_char(self, char):
        print('Rejected', char)

    def draw(self, background):
        self.choose_new_word()

        for item in self.stream:
            item.draw(
                background, self.phrase_holder.current_phrase == item.text
            )
            item.move()

            if item.topleft[0] < 0:
                print('Sorry, you lost!')
                self.done = True
                break


pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

    background.fill(colors.GAME_BACKGROUND)
    pygame_phrase_holder.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
