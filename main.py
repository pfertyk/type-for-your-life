class PhrasesHolder:
    def __init__(self):
        self.phrases = set()
        self.current_phrase = None

    def add_phrase(self, phrase):
        if phrase.lower() in (phrase.lower() for phrase in self.phrases):
            raise ValueError('You cannot add the same phrase twice')
        if phrase[0].lower() in (phrase[0].lower() for phrase in self.phrases):
            raise ValueError('First letter of a new phrase must be unique')
        self.phrases.add(phrase)

    def send_char(self, char):
        if not char:
            raise ValueError('Char must not be empty')
        if not self.current_phrase:
            for phrase in self.phrases:
                if phrase.lower().startswith(char.lower()):
                    self.current_phrase = phrase
