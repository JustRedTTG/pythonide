from pygameextra import colors
from common import darken


class Style:
    # Colors
    background: tuple[int, int, int]
    background_darker: tuple[int, int, int]
    background_shadow: tuple[int, int, int]
    button_select: tuple[int, int, int]
    text_color: tuple[int, int, int]
    reversed_text_color: tuple[int, int, int]
    code: tuple[int, int, int]
    code_cursor_select: tuple[int, int, int]

    # Text
    top_panel_button_padding_horizontal: int = 30
    top_panel_button_padding_vertical: int = 10

    top_sub_panel_button_padding_horizontal: int = 10
    top_sub_panel_button_padding_vertical: int = 10

    file_panel_button_padding_horizontal: int = 30
    file_panel_button_padding_vertical: int = 10
    file_panel_selected_size: int = 10

    code_panel_padding: int = 5

    # other
    code_sub_panel_width: int = 30
    code_cursor_width: int = 1

    # Font style
    top_panel_font_size: int = 12
    top_sub_panel_font_size: int = top_panel_font_size
    file_panel_font_size: int = 12
    code_panel_font_size: int = 12
    code_sub_panel_font_size: int = 12
    text_spacing: int  # Set using space char

    syntax_colors: dict[str, tuple[int, int, int]] = {
        '^': (20, 20, 20)
    }
    syntax_color_lock: dict[str, bool] = {
        '^': True
    }


def from_pallet(darkest_color: tuple[int, int, int],
                washed_dark_color: tuple[int, int, int],
                light_color: tuple[int, int, int],
                washed_light_color: tuple[int, int, int],
                text_color: tuple[int, int, int] = colors.white,
                reversed_text_color: tuple[int, int, int] = colors.black):
    style = Style()

    style.background = washed_dark_color
    style.background_darker = darken(washed_dark_color, 10, 10, 10)
    style.background_shadow = light_color
    style.button_select = washed_light_color
    style.text_color = text_color
    style.reversed_text_color = reversed_text_color
    style.code = darkest_color
    style.code_cursor_select = text_color

    return style


def from_json(json: dict):
    # TODO: add json compatability for themes
    pass
