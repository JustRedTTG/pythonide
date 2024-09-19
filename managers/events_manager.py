import time
import pygameextra as pe
from managers.config_manager import Config
from common import cursor_index, custom_split
from panels.ui_panels import create_ui_panel


def get_cursor_line(config: Config):
    return cursor_index(config.cursor_location, config.code)[0]


def move_cursor_line(amount: int, config: Config):
    current_line = get_cursor_line(config)
    new_line = max(0, min(current_line + amount, len(config.code) - 1))  # CAP
    index_new_line = sum([len(line) for line in config.code[0:new_line]])
    max_line_index = len(config.code[new_line]) - (1 if new_line < len(config.code) - 1 else 0)
    config.cursor_location = index_new_line + min(
        max_line_index, config.cursor_up_down_max)
    config.current_project.set_cursor_location(config)


def move_cursor_index(amount: int, config: Config):
    config.cursor_up_down_max = 0
    config.cursor_location += amount
    config.current_project.set_cursor_location(config)
    config.cursor_blink_state = time.time() + .1


def delete_character(config: Config, line_index, character_index):
    l = list(config.code[line_index])
    if character_index >= len(l):
        if line_index < len(config.code) - 1:
            return
        elif character_index >= len(l) + 1:
            return
    if character_index < 1:  # Beginning of the line
        if line_index == 0: return  # First line
        config.code[line_index - 1] = config.code[line_index - 1].rstrip('\n') + config.code[line_index]
        del config.code[line_index]
        del config.code_hashes[line_index]
        del config.code_texts[line_index]
        config.code_sub_panel_active = True
    else:
        word, _ = cursor_index(character_index, custom_split(config.code[line_index]))
        old = l.copy()
        del l[character_index - 1]  # delete character
        if len(custom_split(''.join(old))) != len(custom_split(''.join(l))):
            index = len(''.join(l[:character_index - 2]).split())
            del config.code_texts[line_index].texts[index]
        config.code[line_index] = ''.join(l)


def back(config: Config):
    line_index, character_index = cursor_index(
        config.cursor_location, config.code)
    delete_character(config, line_index, character_index)
    move_cursor_index(-1, config)


def delete(config: Config):
    line_index, character_index = cursor_index(
        config.cursor_location, config.code)
    if line_index < len(config.code) - 1 and character_index + 1 >= len(config.code[line_index]):
        delete_character(config, line_index + 1, -1)
    else:
        delete_character(config, line_index, character_index + 1)
    # move_cursor_index(1, config)


def new_line(config: Config):
    line, index = cursor_index(config.cursor_location, config.code)
    before, after = config.code[line][:index], config.code[line][index:]
    config.code[line] = before + '\n'
    config.code_texts[line] = None
    config.code.insert(line + 1, after)
    config.code_texts.insert(line + 1, None)
    config.code_hashes.insert(line + 1, None)
    move_cursor_index(1, config)
    config.code_sub_panel_active = True


def resize_event(config: Config, size=None):
    config.window_width, config.window_height = pe.display.get_size() if size is None else size
    config.top_panel_surface = None
    config.top_sub_panel_surface = None
    config.code_panel_surface = None
    config.code_sub_panel_surface = None
    config.file_panel_surface = None
    config.left_panel_surface = None
    config.top_panel_active = False
    config.mouse_moved = False
    config.ui_panel_surfaces.clear()
    all_data = list(config.ui_panel_data.values())
    config.ui_panel_data.clear()
    for i, data in enumerate(all_data):
        create_ui_panel(config, data['type'], data)


    config.top_sub_panel_active = False
    config.left_panel_active = False
    config.file_panel_active = False
    config.code_panel_active = False
    config.code_sub_panel_active = False

def handle_event(event: pe.pygame.event.Event, config: Config):
    if pe.event.resizeCheck():
        resize_event(config)

    if pe.event.key_DOWN(pe.pygame.K_LEFT):
        prev = get_cursor_line(config)
        move_cursor_index(-1, config)
        if not prev == get_cursor_line(config):
            config.code_sub_panel_active = True
        config.cursor_hold_left = time.time()
    elif pe.event.key_UP(pe.pygame.K_LEFT):
        config.cursor_hold_left = 0

    if pe.event.key_DOWN(pe.pygame.K_RIGHT):
        prev = get_cursor_line(config)
        move_cursor_index(1, config)
        if not prev == get_cursor_line(config):
            config.code_sub_panel_active = True
        config.cursor_hold_right = time.time()
    elif pe.event.key_UP(pe.pygame.K_RIGHT):
        config.cursor_hold_right = 0

    if config.cursor_up_down_max == 0 and (pe.event.key_DOWN(pe.pygame.K_DOWN) or \
                                           pe.event.key_DOWN(pe.pygame.K_UP)):
        config.cursor_up_down_max = cursor_index(
            config.cursor_location, config.code
        )[1]

    if pe.event.key_DOWN(pe.pygame.K_DOWN):
        move_cursor_line(1, config)
        config.code_sub_panel_active = True
        config.cursor_hold_down = time.time()
    elif pe.event.key_UP(pe.pygame.K_DOWN):
        config.cursor_hold_down = 0

    if pe.event.key_DOWN(pe.pygame.K_UP):
        move_cursor_line(-1, config)
        config.code_sub_panel_active = True
        config.cursor_hold_up = time.time()
    elif pe.event.key_UP(pe.pygame.K_UP):
        config.cursor_hold_up = 0

    if pe.event.key_DOWN(pe.pygame.K_BACKSPACE):
        back(config)
        config.cursor_hold_back = time.time()
    elif pe.event.key_UP(pe.pygame.K_BACKSPACE):
        config.cursor_hold_back = 0

    if pe.event.key_DOWN(pe.pygame.K_DELETE):
        delete(config)
        config.cursor_hold_delete = time.time()
    elif pe.event.key_UP(pe.pygame.K_DELETE):
        config.cursor_hold_delete = 0
    if pe.event.key_DOWN(pe.pygame.K_RETURN):
        new_line(config)
        config.cursor_hold_return = time.time()
    elif pe.event.key_UP(pe.pygame.K_RETURN):
        config.cursor_hold_return = 0

    if pe.event.key_DOWN(pe.pygame.K_END):
        line, index = cursor_index(config.cursor_location, config.code)
        if line >= len(config.code) - 1:
            line_length = len(config.code[line])
        else:
            line_length = len(config.code[line]) - 1
        config.cursor_location += line_length - index

    if pe.event.key_DOWN(pe.pygame.K_HOME):
        line, index = cursor_index(config.cursor_location, config.code)
        config.cursor_location -= index
        config.cursor_blink_state = time.time() + .1

    if event.type == pe.pygame.KEYDOWN:
        u: str = event.unicode
        if u and u.isprintable():
            line, index = cursor_index(config.cursor_location, config.code)
            config.code[line] = config.code[line][:index] + u + config.code[line][index:]
            move_cursor_index(1, config)

    if pe.event.quitCheck():
        config.save()
        pe.pge_quit()


handle_events = lambda config: [handle_event(pe.event.c, config) for pe.event.c in pe.event.get()]


def other_events(config):

    if config.cursor_hold_right and \
            time.time() - config.cursor_hold_right >= config.cursor_start_delay:
        prev = get_cursor_line(config)
        move_cursor_index(1, config)
        if not prev == get_cursor_line(config):
            config.code_sub_panel_active = True
        config.cursor_hold_right += config.cursor_hold_delay

    if config.cursor_hold_left and \
            time.time() - config.cursor_hold_left >= config.cursor_start_delay:
        prev = get_cursor_line(config)
        move_cursor_index(-1, config)
        if not prev == get_cursor_line(config):
            config.code_sub_panel_active = True
        config.cursor_hold_left += config.cursor_hold_delay

    if config.cursor_hold_up and \
            time.time() - config.cursor_hold_up >= config.cursor_start_delay:
        move_cursor_line(-1, config)
        config.code_sub_panel_active = True
        config.cursor_hold_up += config.cursor_hold_delay

    if config.cursor_hold_down and \
            time.time() - config.cursor_hold_down >= config.cursor_start_delay:
        move_cursor_line(1, config)
        config.code_sub_panel_active = True
        config.cursor_hold_down += config.cursor_hold_delay

    if config.cursor_hold_back and \
            time.time() - config.cursor_hold_back >= config.cursor_start_delay:
        back(config)
        config.cursor_hold_back += config.cursor_hold_delay

    if config.cursor_hold_delete and \
            time.time() - config.cursor_hold_delete >= config.cursor_start_delay:
        delete(config)
        config.cursor_hold_delete += config.cursor_hold_delay

    if config.cursor_hold_return and \
            time.time() - config.cursor_hold_return >= config.cursor_start_delay:
        new_line(config)
        config.cursor_hold_return += config.cursor_hold_delay

    config.cursor_location = min(
        max(0, config.cursor_location),
        sum([len(line) for line in config.code])
    )  # Cap cursor location

    if time.time() - config.cursor_blink_state >= \
            config.cursor_blink_time_in + config.cursor_blink_time_out or \
            config.cursor_hold_left or config.cursor_hold_right or \
            config.cursor_hold_up or config.cursor_hold_down:
        config.cursor_blink_state = time.time()
