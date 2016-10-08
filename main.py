class TextHolder:
    def __init__(self):
        self.texts = []

    def add_text(self, text):
        if text.lower() in (text.lower() for text in self.texts):
            raise Exception('You cannot add the same text twice')
        self.texts.append(text)
