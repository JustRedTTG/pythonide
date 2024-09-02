import pygameextra as pe

from panels.ui_panels.file.new_project import handle_new_project_panel
from panels.ui_panels.file.settings import handle_settings_panel
from pythonide_types.Config import Config

PANEL_TYPES = {
    'new_project': handle_new_project_panel,
    'settings': handle_settings_panel,
    'file_new': handle_settings_panel,  # TODO: Implement
    'file_open': handle_settings_panel,  # TODO: Implement
}


def handle_ui_panels(config: Config):
    for ui_panel_surface in config.ui_panel_surfaces:
        data = config.ui_panel_data[id(ui_panel_surface)]
        moving, pos = data['draggable'].check()
        data['pos'] = [
            pos[0],
            pos[1] + config.ui_panel_text_height,
        ]
        ui_panel_surface.pos = data['pos']
        ui_panel_surface.last_blit_pos = data['pos']
        if moving:
            return
        with ui_panel_surface:
            pe.fill.full(config.style.background)
            PANEL_TYPES[data['type']](config, data)
            pe.draw.rect(config.style.background_shadow, (0, 0, *ui_panel_surface.size), 1)


def close_ui_panel(config: Config, ui_panel_surface: pe.Surface):
    config.ui_panel_surfaces.remove(ui_panel_surface)
    del config.ui_panel_data[id(ui_panel_surface)]


def draw_ui_panel_extra(config: Config, ui_panel_surface: pe.Surface):
    rect = pe.Rect(*ui_panel_surface.pos, *ui_panel_surface.size)
    data = config.ui_panel_data[id(ui_panel_surface)]

    rect.height += config.ui_panel_text_height
    rect.y -= config.ui_panel_text_height
    header_rect = rect.copy()
    header_rect.height = config.ui_panel_text_height
    header_rect.bottomleft = ui_panel_surface.pos
    # Shadow outline
    rect.inflate_ip(7, 7)
    pe.draw.rect((*pe.colors.black, 50), rect, 7)

    # Header outline
    pe.draw.rect(config.style.background, header_rect)
    header_rect.height += 1  # Fix double outline
    pe.draw.rect(config.style.background_shadow, header_rect, 1)

    # Header text
    config.ui_panel_texts[data['type']].rect.midleft = header_rect.midleft
    config.ui_panel_texts[data['type']].rect.x += config.style.ui_panel_button_padding_horizontal
    config.ui_panel_texts[data['type']].display()

    # Close button
    close_rect = header_rect.copy()
    close_text = config.ui_panel_texts['close']
    close_rect.width = close_text.rect.width
    close_rect.topright = header_rect.topright
    close_text.rect.center = close_rect.center

    pe.draw.line(config.style.background_shadow, close_rect.topleft, close_rect.bottomleft, 1)
    pe.button.rect(
        close_rect,
        (0, 0, 0, 0), config.style.button_select,
        action=close_ui_panel, data=(config, ui_panel_surface)
    )
    close_text.display()


def get_ui_panel_size(config: Config, panel_type: str):
    return 550, 300


def create_ui_panel(config: Config, panel_type: str, panel_data: dict = None, ensure_one=False):
    if ensure_one:
        for data in config.ui_panel_data.values():
            if data['type'] == panel_type:
                return
    if panel_data is None:
        panel_data = {}

    panel_size = get_ui_panel_size(config, panel_type)
    config.ui_panel_surfaces.append(pe.Surface(panel_size))

    position = panel_data.get('pos', tuple(c // 2 - s // 2 for c, s in zip(config.window_size(), panel_size)))

    config.ui_panel_data[id(config.ui_panel_surfaces[-1])] = {
        'type': panel_type,
        # The draggable is the header, has to be above the position
        'draggable': pe.Draggable(
            (position[0], position[1] - config.ui_panel_text_height),
            (panel_size[0]-config.ui_panel_texts['close'].rect.width, config.ui_panel_text_height)
        ),
        'pos': position,
        **panel_data
    }
