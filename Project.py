import os.path
from pygameextra.display import set_caption
from common import if_joined_does_not_exist_remake_it, create_title


class Project:
    # Info on data structure:
    # 0 - global 1 - yes 2 - no for global / project settings (gps)

    path: str = None
    name: str = ':new'
    title: str = 'Untitled'
    files_opened: list[str, ...]
    files_cursor_locations: dict[str, int] = {}
    file_selected: str = ":new"

    # Settings & window information
    allow_multiple_commands: int = 0  # gps
    left_panel_size: int = 200

    def __repr__(self):
        return self.name

    def load(self, config):
        if not self.path:
            if_joined_does_not_exist_remake_it(config.cache_folder, "project_temp")
            self.path = os.path.join(config.cache_folder, "project_temp")
            self.files_opened = [":new"]
            self.files_cursor_locations = {os.path.join(self.path, '.new'): 999}
            return
        # TODO: add loading of project file and information

    def set_selected_file(self, file, config):
        self.file_selected = file
        config.cursor_location = self.files_cursor_locations.get(
            self.file_selected, 0
        )

    def set_cursor_location(self, config):
        self.files_cursor_locations[self.file_selected] = config.cursor_location
