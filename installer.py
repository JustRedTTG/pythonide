import os
import platform
import subprocess
from shutil import rmtree
import atexit
import hashlib

print("Ensure directory is correct...")
os.chdir(script_dir := os.path.dirname(os.path.abspath(__file__)))

import config_manager as cfg_mngr
from common import APP_VERSION, APP_NAME

print(f"Initializing {APP_NAME} configuration")
config = cfg_mngr.initialize()

INSTALL_DIR = os.path.join(config.data_folder, 'application', APP_VERSION)
VENV_DIR = os.path.join(INSTALL_DIR, 'venv')
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
        answer = input(f"{question} (Y/n): ").strip().lower()
        if not answer:
            return True
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

            old_path = os.path.join(config.data_folder, 'application', old_version)
            if os.path.isdir(old_path):
                if yes_no("Do you want to delete the previous version installation?"):
                    rmtree(old_path)

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

print("Checking virtual environment...")

if platform.system() == "Windows":
    pip_script = os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
else:
    pip_script = os.path.join(VENV_DIR, 'bin', 'pip')
if not os.path.exists(pip_script):
    subprocess.run(['python', '-m', 'venv', VENV_DIR])

subprocess.run([pip_script, 'install', '-r', os.path.join(os.getcwd(), 'requirements.txt')])

print(f"Installing {APP_NAME} version {APP_VERSION}...")
for file in files:
    folder, filename = os.path.dirname(file), os.path.basename(file)
    os.makedirs(os.path.join(INSTALL_DIR, folder), exist_ok=True)
    if file == 'launcher.py':
        with open(os.path.join(config.data_folder, filename), 'wb') as f:
            f.write(open(file, 'rb').read())
        with open(os.path.join(config.data_folder, f'{filename}w'), 'wb') as f:
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
