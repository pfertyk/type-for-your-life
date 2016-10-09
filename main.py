class PhrasesHolder:
    def __init__(self, rejected_char_callback=None):
        self.phrases = set()
        self.current_phrase = None
        self.current_phrase_left = None

        def empty_rcc_callback(char):
            pass

        if not rejected_char_callback:
            rejected_char_callback = empty_rcc_callback
        self.rejected_char_callback = rejected_char_callback

    def add_phrase(self, phrase):
        if phrase.lower() in (phrase.lower() for phrase in self.phrases):
            raise ValueError('You cannot add the same phrase twice')
        if phrase[0].lower() in (phrase[0].lower() for phrase in self.phrases):
            raise ValueError('First letter of a new phrase must be unique')
        self.phrases.add(phrase)

    def send_char(self, char):
        if not char or len(char) > 1:
            raise ValueError('Char must have exactly 1 character')
        if not self.current_phrase:
            for phrase in self.phrases:
                if phrase.lower().startswith(char.lower()):
                    self.current_phrase = phrase
                    self.current_phrase_left = phrase[1:]
                    break
            else:
                self.rejected_char_callback(char)
        else:
            if self.current_phrase_left.startswith(char):
                self.current_phrase_left = self.current_phrase_left[1:]
                if not self.current_phrase_left:
                    self.phrases.remove(self.current_phrase)
                    self.current_phrase = None
                    self.current_phrase_left = None
