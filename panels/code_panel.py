import time
from itertools import zip_longest

import pygameextra as pe

from common import cursor_index, custom_split
from managers.project_manager import load_selected_file
from managers.text_manager import configure_file_panel_texts
from pythonide_types.Config import Config
from pythonide_types.Texts import Texts


def make_word(config: Config, word: str, i=None, i2=None):
    if i is not None and i2 is not None:
        config.syntax_color_lock = None
        for i3, item in enumerate(custom_split(config.code[i])):
            if i3 >= i2: continue
            c = config.style.syntax_colors.get(item)
            if (c is not None) and config.style.syntax_color_lock.get(item):
                config.syntax_color_lock = c

    c = config.style.syntax_colors.get(word)
    if (c is not None) and config.style.syntax_color_lock.get(word):
        config.syntax_color_lock = c
    return pe.text.Text(word, config.font_filepaths.regular,
                        config.style.code_panel_font_size,
                        colors=[((config.syntax_color_lock or c) or config.style.text_color), None])

def draw_code_panel(config: Config):
    pe.fill.full(config.style.code)
    if config.current_project.file_selected in config.opened_files_cache:
        config.code = config.opened_files_cache[config.current_project.file_selected]
    else:
        if not load_selected_file(config):
            del config.current_project.files_opened[
                config.current_project.files_opened.index(config.current_project.file_selected)
            ]
            configure_file_panel_texts(config)
        config.current_project.set_selected_file(config.current_project.files_opened[0], config)
        config.current_project.set_cursor_location(config)

        config.code = ["Loading..."]
        rerun = True

    x = config.code_sub_panel_surface.size[0] + config.style.code_panel_padding
    view_width = config.code_panel_surface.surface.get_width()
    cursor_line, cursor_indexing = cursor_index(config.cursor_location, config.code)
    cursor_x = x + config.style.text_spacing * cursor_indexing

    for i, (line, hashing, texts) in enumerate(zip_longest(config.code, config.code_hashes, config.code_texts)):
        config.syntax_color_lock = None
        check_for_changes = hash(line) != hashing
        remake = (hashing is None) or (texts is None)
        if remake:
            if len(config.code_hashes) > i: del config.code_hashes[i]
            if len(config.code_texts) > i: del config.code_texts[i]
            config.code_hashes.insert(i, hash(line))
            config.code_texts.insert(i, Texts())
            for word in custom_split(line):
                config.code_texts[i].texts.append(make_word(config, word))
        if check_for_changes:
            config.code_hashes[i] = hash(line)
            just_go = False
            for i2, (word, old) in enumerate(zip_longest(custom_split(line), [
                text.text for text in config.code_texts[i].texts
            ])):
                if word is None: continue
                if old is None:
                    config.code_texts[i].texts.insert(i2, make_word(config, word, i, i2))
                elif (word != old) or just_go:
                    config.code_texts[i].texts[i2] = make_word(config, word, i, i2)
                    if config.style.syntax_color_lock.get(old): just_go = True
            if not config.code_text_height:
                config.code_text_height = config.code_texts[i].texts[0].rect[3]
            config.code_texts[i].combine(config.style.text_spacing, config.code_text_height)
    y = 0
    for linei, texts in enumerate(config.code_texts):
        if texts.combined:
            pe.display.blit(texts.combined, [v + o for v, o in zip((x, y), config.code_panel_surface_offset)])
        else:
            texts.combine(config.style.text_spacing, config.code_text_height)
        y += texts.combined.size[1]
        if cursor_line == linei and time.time() - config.cursor_blink_state < config.cursor_blink_time_in:
            pe.draw.line(config.style.code_cursor_select,
                         [v + o for v, o in zip((cursor_x, y), config.code_panel_surface_offset)],
                         [v + o for v, o in
                          zip((cursor_x, y - texts.combined.size[1]), config.code_panel_surface_offset)],
                         config.style.code_cursor_width)


def code_panel(config: Config):
    rerun = False
    if config.code_panel_active and not config.top_sub_panel_active:
        with config.code_panel_surface:
            draw_code_panel(config)
    elif not config.code_panel_surface:
        height_offset = config.top_panel_text_height + config.file_panel_text_height
        config.code_panel_surface = pe.Surface((
            config.window_width - config.current_project.left_panel_size,
            config.window_height - height_offset
        ))
        config.code_panel_surface.pos = (
            config.current_project.left_panel_size,
            height_offset
        )
        config.code_panel_active = True
        config.on_cursor_move()
    if rerun:
        code_panel(config)


def code_sub_panel(config: Config):
    if not config.code_sub_panel_surface:
        height_offset = config.top_panel_text_height + config.file_panel_text_height
        config.code_sub_panel_surface = pe.Surface((
            config.style.code_sub_panel_width,
            config.window_height - height_offset
        ))
        config.code_sub_panel_active = True
    elif config.code_sub_panel_active:
        pe.fill.full(config.style.background_darker, config.code_sub_panel_surface)  # Fill with background
        y = 0
        line, _ = cursor_index(config.cursor_location, config.code)
        for i in range(len(config.code)):
            list_used = config.code_sub_panel_texts if i != line else config.code_sub_panel_texts_selected
            color_used = config.style.background_shadow if i != line else config.style.text_color
            font_used = config.font_filepaths.thin if i != line else config.font_filepaths.bold

            i2 = len(list_used) - 1
            while i2 <= i:
                list_used.append(
                    pe.text.Text(str(i2 + 2), font_used,
                                 config.style.code_panel_font_size,
                                 colors=[color_used, None])
                )
                i2 += 1
            config.code_sub_panel_surface.stamp(
                list_used[i].obj,
                (config.style.code_panel_padding, y)
            )
            y += config.code_text_height or 1
        pe.draw.line(config.style.background_shadow,
                     (config.style.code_sub_panel_width, 0),
                     (config.style.code_sub_panel_width, config.code_sub_panel_surface.size[1]),
                     3, config.code_sub_panel_surface
                     )
        config.code_sub_panel_active = False
