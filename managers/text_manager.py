from common import file_name
from pygameextra.text import Text
from languages import languages
from pythonide_types.Config import Config
import pythonide_types.Strings as Strings


def configure_top_panel_texts(config: Config):
    config.top_panel_texts = []
    config.top_sub_panel_texts = {}
    config.top_sub_panel_width = {}
    config.top_sub_panel_height = {}

    for i, (identifier, text) in enumerate(zip(Strings.top_panel_identifiers,
                                               languages[config.language].top_panel_texts)):
        config.top_panel_texts.append(Text(text,
                                           config.font_filepaths.thin,
                                           config.style.top_panel_font_size,
                                           colors=(config.style.text_color, None)
                                           ))
    configure_top_sub_panel_texts(config)
    config.top_panel_text_height = config.top_panel_texts[0].rect[3] + config.style.top_panel_button_padding_vertical


def configure_file_panel_texts(config: Config):
    config.file_panel_texts = []
    for text in [file_name(path) for path in config.current_project.files_opened] + ['No files opened']:
        config.file_panel_texts.append(Text(text,
                                            config.font_filepaths.regular,
                                            config.style.file_panel_font_size,
                                            colors=(config.style.text_color, None)
                                            ))
    config.file_panel_text_height = config.file_panel_texts[0].rect[3] + config.style.file_panel_button_padding_vertical


def configure_top_sub_panel_texts(config):
    for i, identifier in enumerate(Strings.top_panel_identifiers):
        config.top_sub_panel_texts[identifier] = []
        config.top_sub_panel_width[identifier] = config.top_panel_texts[i].rect[2] + \
                                                 config.style.top_panel_button_padding_horizontal
        config.top_sub_panel_height[identifier] = 0
        for sub_identifier in Strings.top_sub_panel_identifiers[identifier]:
            if sub_identifier.startswith('_') and sub_identifier.endswith('_'):
                config.top_sub_panel_texts[identifier].append(None)
                continue
            text = languages[config.language].top_sub_panel_texts[sub_identifier]
            config.top_sub_panel_texts[identifier].append(Text(text,
                                                               config.font_filepaths.thin,
                                                               config.style.top_sub_panel_font_size,
                                                               colors=(config.style.text_color, None)
                                                               ))

            config.top_sub_panel_width[identifier] = max(
                config.top_sub_panel_width[identifier],
                config.top_sub_panel_texts[identifier][-1].rect[2] +
                config.style.top_sub_panel_button_padding_horizontal
            )
            config.top_sub_panel_height[identifier] += \
                config.top_sub_panel_texts[identifier][-1].rect[3] + \
                config.style.top_sub_panel_button_padding_vertical


def configure_ui_panel_texts(config: Config):
    for key, text in languages[config.language].ui_panel_texts.items():
        config.ui_panel_texts[key] = Text(
            text,
            config.font_filepaths.regular,
            config.style.ui_panel_font_size,
            colors=(config.style.text_color, None)
        )
    config.ui_panel_text_height = config.ui_panel_texts[key].rect[3] + config.style.ui_panel_button_padding_vertical


def configure_texts(config: Config):
    configure_top_panel_texts(config)
    configure_file_panel_texts(config)
    configure_ui_panel_texts(config)
    config.style.text_spacing = Text(' ', config.font_filepaths.regular, config.style.code_panel_font_size).rect[2]
