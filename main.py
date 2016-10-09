class PhrasesHolder:
    def __init__(self):
        self.phrases = set()
        self.current_phrase = None
        self.current_phrase_left = None

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
        else:
            if self.current_phrase_left.startswith(char):
                self.current_phrase_left = self.current_phrase_left[1:]
                if not self.current_phrase_left:
                    self.phrases.remove(self.current_phrase)
