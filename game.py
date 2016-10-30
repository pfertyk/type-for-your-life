import pygame
import random

import colors
import settings
from core import PhrasesHolder


class Phrase:
    def __init__(self, phrase, midleft):
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

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
            self.full_phrase.get_width() + 2 * settings.PHRASE_PADDING,
            self.full_phrase.get_height() + 2 * settings.PHRASE_PADDING
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
        pygame.draw.rect(
            background, frame_color, self.frame, settings.PHRASE_FRAME_WIDTH
        )

        topleft = (
            self.topleft[0] + settings.PHRASE_PADDING,
            self.topleft[1] + settings.PHRASE_PADDING
        )

        background.blit(self.full_phrase, topleft)
        rect0 = self.full_phrase.get_rect(topleft=topleft)
        rect = self.remaining_phrase.get_rect(topright=rect0.topright)
        background.blit(self.remaining_phrase, rect)

    def get_rect(self):
        return self.frame


class PygamePhraseHolder:
    def __init__(self):
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

        self.available_phrases = list(set(settings.AVAILABLE_PHRASES))
        random.shuffle(self.available_phrases)

        self.phrase_count = 0
        self.remaining_phrases_count = settings.MAX_PHRASES
        self.last_phrase_time = None
        self.phrase_interval = 4000

        self.stream = []
        self.phrase_to_stream = {}

        self.phrase_holder = PhrasesHolder(self.reject_char, self.accept_char)

        self.done = False

    def choose_new_word(self):
        if self.phrase_count == settings.MAX_PHRASES:
            return

        if self.last_phrase_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_phrase_time < self.phrase_interval:
                return

        available_midleft = None

        for _ in range(10):
            available_midleft = (settings.WIDTH, random.randint(
                settings.NEW_PHRASE_SAFE_SPACE//2,
                settings.NEW_PHRASE_MAX_AVAILABLE_HEIGHT -
                settings.NEW_PHRASE_SAFE_SPACE//2
            ))

            rect = pygame.Rect(
                0,
                0,
                settings.NEW_PHRASE_SAFE_SPACE,
                settings.NEW_PHRASE_SAFE_SPACE
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
            phrase = self.available_phrases.pop(0)

            try:
                self.phrase_holder.add_phrase(phrase)

                item = Phrase(phrase, available_midleft)

                self.stream.append(item)
                self.phrase_to_stream[phrase] = item
                self.phrase_count += 1
                self.last_phrase_time = pygame.time.get_ticks()
                break
            except ValueError:
                print('Adding a new phrase failed, retrying')
                self.available_phrases.append(phrase)

    def accept_char(self, char, phrase, phrase_left):
        item = self.phrase_to_stream[phrase]
        item.update(phrase_left)

        if not phrase_left:
            self.stream.remove(item)
            self.remaining_phrases_count -= 1
        if not self.stream and not self.remaining_phrases_count:
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

        self._draw_status(background)

    def _draw_status(self, background):
        text_remaining = self.font.render(
            'Remaining: {}'.format(self.remaining_phrases_count),
            1,
            colors.STATUS_FONT
        )
        background.blit(
            text_remaining, (0, settings.NEW_PHRASE_MAX_AVAILABLE_HEIGHT)
        )
