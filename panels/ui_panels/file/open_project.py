import pygameextra as pe

from panels.ui_panels.common.tree_view import TreeView, TreeNode
from pythonide_types.Config import Config


def init_open_project_panel(config: Config, data):
    data['tree'] = TreeView(0, 0, config, TreeNode.create_directory_tree("C:\\Users\\Lenovo\\Nextcloud\\Documents\\PPG\\pythonide\\panels"))


def handle_open_project_panel(config: Config, data, new: bool = False):
    if new:
        init_open_project_panel(config, data)
        return

    data['tree']()
