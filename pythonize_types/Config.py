from pygameextra import Surface
from pygameextra.text import Text
from hexicapi.save import save
from copy import copy as duplicate
from .Style import Style
from .Project import Project
from .Fonts import Fonts
from .Texts import Texts


class Config:
    # Info on data structure:
    # 0 - global 1 - yes 2 - no for global / project settings (gps)

    # Switch data
    first_run: bool = False

    # Customization data
    theme: str = "dark"
    language: str = "en"
    global_allow_multiple_commands: bool = True  # gps
    window_width: int = 700
    window_height: int = 500
    cursor_hold_delay: float = .05
    cursor_start_delay: float = .2
    cursor_blink_time_in: float = .5
    cursor_blink_time_out: float = .7

    # Project data
    current_project: Project
    current_project_name: str = ':new'
    current_project_loaded: bool = False

    # Temporary paths
    config_folder: str
    config_filepath: str
    data_folder: str
    cache_folder: str
    font_filepaths: Fonts

    # Temporary surfaces
    left_panel_surface: Surface = None
    file_panel_surface: Surface = None
    top_panel_surface: Surface = None
    top_sub_panel_surface: Surface = None
    code_panel_surface: Surface = None
    code_sub_panel_surface: Surface = None

    # Temporary switches
    top_panel_active: bool = False
    top_sub_panel_active: bool = False
    left_panel_active: bool = False
    file_panel_active: bool = False
    code_panel_active: bool = False
    code_sub_panel_active: bool = False
    syntax_color_lock: tuple[int, int, int] = None
    cursor_hold_left: int = 0
    cursor_hold_right: int = 0
    cursor_hold_down: int = 0
    cursor_hold_up: int = 0
    cursor_hold_back: int = 0
    cursor_hold_delete: int = 0
    cursor_hold_return: int = 0
    cursor_blink_state: float = 0

    # Temporary text data
    top_panel_texts: list[Text, ...]
    file_panel_texts: list[Text, ...]
    top_sub_panel_texts: dict[str, list[Text, ...]]
    code_sub_panel_texts: list[Text, ...] = []
    code_sub_panel_texts_selected: list[Text, ...] = []

    # Temporary coordination data
    top_panel_text_height: int
    file_panel_text_height: int
    top_sub_panel_height: dict[str, int]
    top_sub_panel_width: dict[str, int]
    top_sub_panel_identifier: str
    top_sub_panel_x: int
    code_text_height: int = None

    # Temporary file data
    opened_files_cache: dict[str, str] = {}

    # Cache
    style: Style
    code: list[str] = ['']
    code_texts: list[Texts, ...] = []
    code_hashes: list[int, ...] = []
    cursor_location: int = 0
    cursor_up_down_max: int = 0

    def save(self):
        clone = duplicate(self)
        save(self.config_filepath, clone)

    def __copy__(self):
        new_copy = Config()
        # Copy switches
        # ...

        # Copy customization data
        new_copy.theme = self.theme
        new_copy.language = self.language
        new_copy.global_allow_multiple_commands = self.global_allow_multiple_commands
        new_copy.window_width = self.window_width
        new_copy.window_height = self.window_height
        new_copy.cursor_hold_delay = self.cursor_hold_delay
        new_copy.cursor_start_delay = self.cursor_start_delay
        new_copy.cursor_blink_time_in = self.cursor_blink_time_in
        new_copy.cursor_blink_time_out = self.cursor_blink_time_out

        # Copy current project information
        new_copy.current_project = self.current_project

        return new_copy

    def window_size(self):
        return self.window_width, self.window_height
