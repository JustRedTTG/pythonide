import os.path
import appdirs
from hexicapi.save import load
from common import APP_NAME, APP_AUTHOR, APP_CHANNEL, APP_EXTENSION, if_it_does_not_exist_make_it, join_exists
from pythonize_types.Config import Config
from pythonize_types.Project import Project
from pythonize_types.Fonts import Fonts
from .style_manager import get_style


def initialize() -> Config:
    # Load app folders
    config_folder = appdirs.user_config_dir(APP_NAME, APP_AUTHOR, APP_CHANNEL, True)
    data_folder = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_CHANNEL, True)
    cache_folder = appdirs.user_cache_dir(APP_NAME, APP_AUTHOR, APP_CHANNEL, True)

    # Ensure app folders are available
    if_it_does_not_exist_make_it(config_folder)
    if_it_does_not_exist_make_it(data_folder)
    if_it_does_not_exist_make_it(cache_folder)

    if config_filepath := join_exists(config_folder, f'config.{APP_EXTENSION}'):
        # Load available config file
        config: Config = load(config_filepath)[0]
    else:
        # Create a first run
        config: Config = Config()
        config.first_run = True

    # Insert temporary data
    # App folders
    config.config_folder = config_folder
    config.config_filepath = config_filepath or os.path.join(config_folder, f'config.{APP_EXTENSION}')
    config.data_folder = data_folder
    config.cache_folder = cache_folder

    # Color information
    get_style(config)

    # Fonts
    if_it_does_not_exist_make_it(os.path.join(data_folder, 'fonts'))
    config.font_filepaths = Fonts()
    config.font_filepaths.regular = os.path.join(data_folder, 'fonts', config.font_filepaths.regular)
    config.font_filepaths.regular_italic = os.path.join(data_folder, 'fonts', config.font_filepaths.regular_italic)

    config.font_filepaths.bold = os.path.join(data_folder, 'fonts', config.font_filepaths.bold)
    config.font_filepaths.bold_italic = os.path.join(data_folder, 'fonts', config.font_filepaths.bold_italic)

    config.font_filepaths.thin = os.path.join(data_folder, 'fonts', config.font_filepaths.thin)
    config.font_filepaths.thin_italic = os.path.join(data_folder, 'fonts', config.font_filepaths.thin_italic)

    config.font_filepaths.health_check()

    return config


def get_projects(config: Config) -> list[Project, ...]:
    if config_filepath := join_exists(config.config_folder, f'projects.{APP_EXTENSION}'):
        # Load projects
        return load(config_filepath)
    return []
