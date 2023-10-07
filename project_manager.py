import os.path
from config_manager import get_projects
from Config import Config
from Project import Project
from common import create_title
from text_manager import configure_file_panel_texts

def load_project(config: Config):
    projects: list[Project, ...] = get_projects(config)
    if config.current_project_name == ':new':
        config.current_project = Project()
    elif config.current_project_name in projects:
        config.current_project = projects[config.current_project_name]

    config.current_project.load(config)

def save_project(config: Config):
    #TODO: project saving and management
    pass


def load_selected_file(config):
    file = config.current_project.file_selected
    if file == ':new':
        file = os.path.join(config.current_project.path, '.new')
        config.current_project.files_opened[config.current_project.files_opened.index(':new')] = file
        config.current_project.file_selected = file
        with open(config.current_project.file_selected, 'w') as f:
            f.write('Hello, World')
        configure_file_panel_texts(config)
    if os.path.exists(file):
        try:
            with open(file, 'r') as f:
                config.opened_files_cache[file] = f.readlines()
        except: return False
        finally:
            return True
    return False