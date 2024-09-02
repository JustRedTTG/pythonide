import time

import pygameextra as pe

import common
from managers import config_manager as cfg_mngr
from itertools import zip_longest
from pygameextra.fpslogger import Logger
from managers.events_manager import handle_events, other_events
from managers.project_manager import load_project, load_selected_file
from managers.text_manager import configure_texts, configure_file_panel_texts
from managers.draggables_manager import configure_draggables
from common import create_title, mouse_rect, surface_rect, file_name, cursor_index, custom_split
from panels.code_panel import code_sub_panel, code_panel
from panels.file_panel import file_panel
from panels.left_panel import left_panel
from panels.top_panel import top_panel
from panels.ui_panels import handle_ui_panels, draw_ui_panel_extra
from pythonide_types.Config import Config
from pygameextra import settings as s

s.raise_error_for_button_without_name = True

class PythonideEditor:
    def __init__(self):
        self.logger = Logger()
        self.config: Config = cfg_mngr.initialize()
        self.button_manager = pe.ButtonManager()
        load_project(self.config)
        configure_texts(self.config)
        configure_draggables(self.config)

    def activate(self):
        s.pythonide_config = self.config


def loop(instance: PythonideEditor):
    if instance.config.previous_mouse_pos is None:
        instance.config.previous_mouse_pos = pe.mouse.pos()

    top_panel(instance.config)  # File, edit, so on
    left_panel(instance.config)  # Files tree view
    file_panel(instance.config)  # files select
    code_sub_panel(instance.config)  # Code line numbers
    code_panel(instance.config)  # Code editor
    handle_ui_panels(instance.config)  # Menus and stuff

    pe.display.blit(instance.config.code_panel_surface, instance.config.code_panel_surface.pos)
    pe.display.blit(instance.config.code_sub_panel_surface, instance.config.code_panel_surface.pos)
    pe.display.blit(instance.config.file_panel_surface, instance.config.file_panel_surface.pos)
    pe.display.blit(instance.config.left_panel_surface, instance.config.left_panel_surface.pos)
    pe.display.blit(instance.config.top_panel_surface)
    for ui_panel_surface in instance.config.ui_panel_surfaces:
        draw_ui_panel_extra(instance.config, ui_panel_surface)
        pe.display.blit(ui_panel_surface, ui_panel_surface.pos)

    # Display dialogs above all else
    if instance.config.top_sub_panel_surface:
        pe.display.blit(instance.config.top_sub_panel_surface, instance.config.top_sub_panel_surface.pos)

    if not instance.config.mouse_moved and pe.mouse.pos() != instance.config.previous_mouse_pos:
        instance.config.mouse_moved = True

    instance.logger.render()
    instance.config.previous_mouse_pos = pe.mouse.pos()


if __name__ == "__main__":
    print(
        f"{common.APP_NAME} by "
        f"{common.APP_AUTHOR} version "
        f"{common.APP_VERSION} {common.APP_CHANNEL} "
        f"running on PGE version {pe.__version__}"
    )
    pe.init()
    instance = PythonideEditor()
    instance.activate()
    pe.display.make(instance.config.window_size(), create_title(instance.config), pe.display.DISPLAY_MODE_RESIZABLE)

    while instance.config.running:
        instance.button_manager.push_buttons()
        handle_events(instance.config)
        other_events(instance.config)
        loop(instance)
        pe.display.update(60)
        instance.button_manager.handle_buttons()
