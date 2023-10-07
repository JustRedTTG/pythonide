from pygameextra.text import Text
from pygameextra.modified import Surface

class Texts:
    texts: list[Text]
    combined: Surface

    def __init__(self):
        self.texts = []
        self.combined = None

    def combine(self, text_spaces, height):
        width = max(0, self.get_width(text_spaces))
        self.combined = Surface((
            width,
            height
        ))
        x = 0
        for text in self.texts:
            self.combined.stamp(text.obj, (x, 0))
            x += text.rect[2] + text_spaces
        return self.combined

    def get_width(self, text_spaces):
        spaces = len(self.texts)-1
        width = spaces * text_spaces
        for text in self.texts:
            width += text.rect[2]
        return width

    # def __iter__(self): return [text.text for text in self.texts]
