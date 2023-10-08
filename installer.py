import os
import config_manager as cfg_mngr
import atexit
import hashlib
from common import APP_VERSION, APP_NAME

print(f"Initializing {APP_NAME} configuration")
config = cfg_mngr.initialize()

INSTALL_DIR = os.path.join(config.data_folder, 'application', APP_VERSION)
HASH_FILE_PATH = os.path.join(INSTALL_DIR, 'hash_list.txt')
VERSION_FILE_PATH = os.path.join(config.data_folder, 'version.txt')

os.makedirs(INSTALL_DIR, exist_ok=True)

if os.path.exists(HASH_FILE_PATH):
    os.remove(HASH_FILE_PATH)
    print("Removing old hash file - reinstall")

hash_file = open(HASH_FILE_PATH, 'a')


def close_hash_file():
    hash_file.close()
    print("Closing hash file")

def yes_no(question):
    while True:
        answer = input(f"{question} (y/N): ").strip().lower()
        if not answer:
            return False
        if answer in ['y', 'n', 'yes', 'no']:
            return answer == 'y' or answer == 'yes'
        print("Invalid input, try again")

def write_version():
    if os.path.exists(VERSION_FILE_PATH):
        print("Checking old version file")
        with open(VERSION_FILE_PATH, 'r') as f:
            old_version = f.read()

        if old_version != APP_VERSION:
            print('\n===> CONFLICTING LAUNCHER VERSIONS <===')
            print(f"Currently installed version exists: {old_version}")
            print(f"Current installation package version: {APP_VERSION}")
            if not yes_no("Do you want to overwrite the current installation package version?"):
                return

    with open(VERSION_FILE_PATH, 'w') as f:
        f.write(APP_VERSION)
        print("Writing version file")

atexit.register(write_version)
atexit.register(close_hash_file)

files = [
    'common.py',
    'config_manager.py',
    'editor.py',
    'languages.py',
    'events_manager.py',
    'text_manager.py',
    'style_manager.py',
    'project_manager.py',
    'launcher.py'
]

for file in os.listdir('pythonize_types'):
    if file.endswith('.py'):
        files.append(os.path.join('pythonize_types', file))

print(f"Installing {APP_NAME} version {APP_VERSION}...")
for file in files:
    folder, filename = os.path.dirname(file), os.path.basename(file)
    os.makedirs(os.path.join(INSTALL_DIR, folder), exist_ok=True)
    if file == 'launcher.py':
        with open(os.path.join(config.data_folder, filename), 'wb') as f:
            f.write(open(file, 'rb').read())
            print("Update to latest launcher")
        continue
    with open(os.path.join(INSTALL_DIR, folder, filename), 'wb') as f:
        f.write(data := open(file, 'rb').read())
        hash_file.write(f'{file}={(hashed_data := hashlib.sha256(data).hexdigest())}\n')
        print(f"COPY {filename} {hashed_data}")
    if file == 'editor.py':
        with open(os.path.join(INSTALL_DIR, folder, f'{filename}w'), 'wb') as f:
            f.write(data)
            hash_file.write(f'{file}w={hashed_data}\n')
            print("DUPLICATE editor.py AS editor.pyw for no console")
