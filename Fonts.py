import os


class Fonts:
    regular: str = 'JetBrainsMono-Regular.ttf'
    regular_italic: str = 'JetBrainsMono-Italic.ttf'

    bold: str = 'JetBrainsMono-Bold.ttf'
    bold_italic: str = 'JetBrainsMono-BoldItalic.ttf'

    thin: str = 'JetBrainsMono-Thin.ttf'
    thin_italic: str = 'JetBrainsMono-ThinItalic.ttf'

    def health_check(self):
        for font in self.__dict__.values():
            if not os.path.exists(font):
                filename = os.path.basename(font)
                if os.path.exists(data_path := os.path.join('data', 'fonts', filename)):
                    with open(font, 'wb') as f:
                        f.write(open(data_path, 'rb').read())
                        continue
                raise FileNotFoundError(f'Font file not found: {data_path}')
