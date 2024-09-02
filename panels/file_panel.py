import pygameextra as pe

from common import file_name
from pythonide_types.Config import Config


def file_panel(config: Config):  # Opened files, not the left panel
    if config.file_panel_active and not config.top_sub_panel_active:

        with config.file_panel_surface:
            if len(config.current_project.files_opened) == 0:
                pe.fill.full(config.style.code)
                return
            else:
                pe.fill.full(config.style.background)
            x = 0
            for i, (file, text) in enumerate(zip(config.current_project.files_opened,
                                                 config.file_panel_texts)):
                selected = text.text == file_name(config.current_project.file_selected)
                pe.button.rect((x, 0,
                                text.rect[2] + config.style.file_panel_button_padding_horizontal,
                                config.file_panel_text_height),
                               *(config.style.background, config.style.button_select) if not selected else
                               (config.style.code, config.style.code),
                               text, action=config.current_project.set_selected_file,
                               data=(file, config))
                x += text.rect[2] + config.style.file_panel_button_padding_horizontal
        pe.draw.line(config.style.background_shadow,
                     (0, config.top_panel_text_height),
                     (config.window_width - config.current_project.left_panel_size,
                      config.top_panel_text_height),
                     3, config.file_panel_surface)
        x = 0
        for i, file in enumerate(config.current_project.files_opened):
            text = config.file_panel_texts[i]
            x_add = text.rect[2] + config.style.file_panel_button_padding_horizontal
            if text.text == file_name(config.current_project.file_selected):
                pe.draw.line(config.style.button_select,
                             (x, config.top_panel_text_height),
                             (x + x_add - 1,
                              config.top_panel_text_height),
                             config.style.file_panel_selected_size, config.file_panel_surface)
            x += x_add
    elif not config.file_panel_surface:
        config.file_panel_surface = pe.Surface((
            config.window_width - config.current_project.left_panel_size,
            config.file_panel_text_height
        ))
        config.file_panel_surface.pos = (config.current_project.left_panel_size, config.top_panel_text_height)
        config.file_panel_active = True