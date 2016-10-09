class PhrasesHolder:
    def __init__(
        self, rejected_char_callback=None, accepted_char_callback=None
    ):
        self.phrases = set()
        self.current_phrase = None
        self.current_phrase_left = None

        self.rejected_char_callback = rejected_char_callback
        self.accepted_char_callback = accepted_char_callback

    def add_phrase(self, phrase):
        if phrase in (phrase for phrase in self.phrases):
            raise ValueError('You cannot add the same phrase twice')
        if phrase[0] in (phrase[0] for phrase in self.phrases):
            raise ValueError('First letter of a new phrase must be unique')
        self.phrases.add(phrase)

    def send_char(self, char):
        if len(char) != 1:
            raise ValueError('Char must have exactly 1 character')

        if not self.current_phrase:
            for phrase in self.phrases:
                if phrase.startswith(char):
                    self.current_phrase = phrase
                    self.current_phrase_left = phrase
                    self._accept_char(char)
                    break
            else:
                self._reject_char(char)
        else:
            if self.current_phrase_left.startswith(char):
                self._accept_char(char)
            else:
                self._reject_char(char)

    def _reject_char(self, char):
        if self.rejected_char_callback:
            self.rejected_char_callback(char)

    def _accept_char(self, char):
        self.current_phrase_left = self.current_phrase_left[1:]

        if self.accepted_char_callback:
            self.accepted_char_callback(
                char, self.current_phrase, self.current_phrase_left
            )

        if not self.current_phrase_left:
            self.phrases.remove(self.current_phrase)
            self.current_phrase = None
            self.current_phrase_left = None
