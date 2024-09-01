import hashlib
import os
import platform
import atexit
import time
import subprocess
import sys

HEALTH_CHECK_STRING = "Performing health check... [{0}/{1}]"


def wait():
    print("Waiting before exit...")
    try:
        time.sleep(20)
    except KeyboardInterrupt:
        return


if __file__.endswith('.py'):
    atexit.register(wait)

print("Ensure directory is correct...")
os.chdir(script_dir := os.path.dirname(os.path.abspath(__file__)))

print("Checking version file...")

if os.path.exists('version.txt'):
    version = open('version.txt', 'r').read()
else:
    exit("No version file found")

print(f"Current version: {version}")
print("Checking directories...")
if not os.path.isdir('application'):
    exit("No application directory found, ensure proper installation.")
if not os.path.isdir(app_dir := os.path.join('application', version)):
    exit(f"No directory found for version {version}, ensure proper installation.")

print("Checking hash file...")
if os.path.exists(os.path.join(app_dir, 'hash_list.txt')):
    hashes = {}
    with open(os.path.join(app_dir, 'hash_list.txt'), 'r') as hash_file:
        for item in hash_file.readlines():
            file, sha = item.rstrip('\n').split('=')
            hashes[file] = sha
    hash_file.close()
else:
    exit("No hash file found, ensure proper installation.")
for i, (file, sha) in enumerate(hashes.items()):
    print(HEALTH_CHECK_STRING.format(i + 1, len(hashes)), end='\r')
    with open(os.path.join(app_dir, file), 'rb') as f:
        new_sha = hashlib.sha256(f.read()).hexdigest()
        if new_sha != sha:
            exit(f"Hash mismatch for file {file}, please reinstall.")

print("Health check complete, no errors found.")

os.chdir(app_dir)
sys.path.append(os.getcwd())

from installation import APP_NAME

print(f"Launching {APP_NAME}...\n")

VENV_DIR = os.path.join(os.getcwd(), '.venv')

if not os.path.isdir(VENV_DIR):
    exit("No venv directory found, ensure proper installation.")

if platform.system() == "Windows":
    python_script = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
else:
    python_script = os.path.join(VENV_DIR, 'bin', 'python')

ext = __file__.rsplit('.', 1)[-1]
args = [python_script, f"editor.{ext}"]
if ext == "pyw":
    subprocess.run(args, creationflags=subprocess.CREATE_NO_WINDOW)
else:
    subprocess.run(args)

print()
