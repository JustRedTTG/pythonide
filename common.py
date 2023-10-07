import os.path
import pygameextra as pe
from shutil import rmtree

APP_NAME = 'OCMD Editor'
APP_AUTHOR = 'RedTTG'
APP_VERSION = '1.0'
APP_CHANNEL = 'debug'


def if_it_does_not_exist_make_it(folder_path) -> bool:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return True
    return False


def if_it_does_not_exist_remake_it(folder_path) -> None:
    if_it_does_not_exist_make_it(folder_path)
    rmtree(folder_path)
    os.makedirs(folder_path)


def join_exists(_path, *paths) -> bool: return False if not os.path.exists( joined := os.path.join(_path, *paths) ) else joined


def if_joined_does_not_exist_make_it(_path, *paths): return if_it_does_not_exist_make_it( os.path.join(_path, *paths) )


def if_joined_does_not_exist_remake_it(_path, *paths): if_it_does_not_exist_remake_it( os.path.join(_path, *paths) )


def create_title(config) -> str: return f"OCMD Editor {APP_VERSION} {APP_CHANNEL} - {config.current_project.title}"


def mouse_rect(spoof) -> pe.rect.Rect: return pe.rect.Rect(*pe.mouse.pos(spoof),1,1)


def surface_rect(surface: pe.Surface) -> pe.rect.Rect: return pe.rect.Rect(*surface.pos, *surface.size)

def file_name(path): return os.path.basename(path)


def darken(rgb, r, g, b):
    return (
        max(0, rgb[0] - r),
        max(0, rgb[1] - g),
        max(0, rgb[2] - b)
    )


def cursor_index(index, lines) -> tuple[int, int]:
    for lines_deep, line in enumerate(lines):
        if index >= len(line):
            index -= len(line)
        else: break
    else:
        index += len(line)
    return lines_deep, index


def cursor_index(index, lines) -> tuple[int, int]:
    for lines_deep, line in enumerate(lines):
        if index >= len(line):
            index -= len(line)
        else: break
    else:
        index += len(line)
    return lines_deep, index


def custom_split(text: list[str]):
    l = []
    t = []
    for v in text :
        if v == ' ':
            l.append(''.join(t))
            t.clear()
            continue
        elif not v.isprintable(): continue
        t.append(v)
    else: l.append(''.join(t))
    return l