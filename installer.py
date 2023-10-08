import os
import config_manager as cfg_mngr
import atexit
from common import APP_VERSION

config = cfg_mngr.initialize()

INSTALL_DIR = os.path.join(config.data_folder, 'application', APP_VERSION)
HASH_FILE_PATH = os.path.join(INSTALL_DIR, 'hash_list.txt')

os.makedirs(INSTALL_DIR, exist_ok=True)

if os.path.exists(HASH_FILE_PATH):
    os.remove(HASH_FILE_PATH)

hash_file = open(HASH_FILE_PATH, 'a')
atexit.register(hash_file.close)

files = [
    'common.py',
    'config_manager.py',
    'editor.py',
    'languages.py',
    'events_manager.py',
    'text_manager.py',
    'style_manager.py',
    'project_manager.py',
]

for file in os.listdir('pythonize_types'):
    if file.endswith('.py'):
        files.append(os.path.join('pythonize_types', file))

for file in files:
    folder, filename = os.path.dirname(file), os.path.basename(file)
    os.makedirs(os.path.join(INSTALL_DIR, folder), exist_ok=True)
    with open(os.path.join(INSTALL_DIR, folder, filename), 'w') as f:
        f.write(data := open(file).read())
        hash_file.write(f'{filename}={hash(data)}\n')
    if filename == 'editor.py':
        with open(os.path.join(INSTALL_DIR, folder, f'{filename}w'), 'w') as f:
            f.write(data)
            hash_file.write(f'{filename}w={hash(data)}\n')
