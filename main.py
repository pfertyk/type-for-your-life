class PhrasesHolder:
    def __init__(self):
        self.phrases = []

    def add_phrase(self, phrase):
        if phrase.lower() in (phrase.lower() for phrase in self.phrases):
            raise Exception('You cannot add the same phrase twice')
        self.phrases.append(phrase)
