import json
from pygameextra import colors
from common import if_joined_does_not_exist_make_it, join_exists
from Config import Config
from Style import from_pallet, from_json

# Load in the themes
built_in_themes = {
    "light": from_pallet((255, 238, 238), (255, 246, 234), (247, 233, 215), (235, 216, 195), colors.verydarkgray,
                         colors.white),
    "dark": from_pallet((33, 33, 33), (50, 50, 50), (13, 115, 119), (77, 122, 119)),
    "pastel_light": from_pallet((177, 178, 255), (170, 196, 255), (210, 218, 255), (238, 241, 255), colors.verydarkgray,
                                colors.white),
    "pastel_dark": from_pallet((57, 55, 91), (116, 92, 151), (213, 151, 206), (245, 176, 203))
}


def get_style(config: Config):
    if config.theme in built_in_themes:
        config.style = built_in_themes[config.theme]
        return
    if_joined_does_not_exist_make_it(config.data_folder, "Themes")
    if theme_path := join_exists(config.data_folder, "Themes", config.theme):
        with open(theme_path, 'r') as theme_file:
            # Read and create theme from json
            config.style = from_json(json.loads(theme_file.read()))
