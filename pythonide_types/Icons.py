import os
import pygameextra as pe

script_dir = os.path.dirname(os.path.abspath(__file__))


class Icons:
    ICONS = {
        'arrow_down': 'arrow_down.png',
        'arrow_right': 'arrow_right.png'
    }

    def __init__(self, config: 'Config'):
        self.config = config
        self.map = None

    def health_check(self):
        for raw_icon in self.ICONS.values():
            for theme in 'DL':
                icon = self.map(f'{theme}_{raw_icon}')
                if not os.path.exists(icon):
                    filename = os.path.basename(icon)
                    if os.path.exists(data_path := os.path.join(script_dir, '..', 'data', 'icons', filename)):
                        with open(icon, 'wb') as f:
                            f.write(open(data_path, 'rb').read())
                            continue
                    raise FileNotFoundError(f'Icon file not found: {data_path}')

    def load_icons(self):
        theme = self.config.style.theme_type
        for raw_icon in self.ICONS.values():
            icon = self.map(f'{theme}_{raw_icon}')
            self.config.icons[raw_icon] = pe.Sprite(icon)

    def __getitem__(self, item) -> pe.Sprite:
        return self.config.icons[self.ICONS[item]]
