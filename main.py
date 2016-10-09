class PhrasesHolder:
    def __init__(self):
        self.phrases = set()

    def add_phrase(self, phrase):
        if phrase.lower() in (phrase.lower() for phrase in self.phrases):
            raise ValueError('You cannot add the same phrase twice')
        self.phrases.add(phrase)
