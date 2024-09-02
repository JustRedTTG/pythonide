import pygameextra as pe

from pythonide_types.Config import Config


def left_panel(config: Config):
    if config.left_panel_active and not config.top_sub_panel_active:
        pe.fill.full(config.style.background, config.left_panel_surface)  # Fill with background
        pe.draw.line(config.style.background_shadow,
                     (config.current_project.left_panel_size, 0),
                     (config.current_project.left_panel_size,
                      config.window_height - config.top_panel_text_height),
                     3, config.left_panel_surface)
    elif not config.left_panel_surface:
        config.left_panel_surface = pe.Surface((
            config.current_project.left_panel_size,
            config.window_height - config.top_panel_text_height
        ))
        config.left_panel_surface.pos = (0, config.top_panel_text_height)
        config.left_panel_active = True
