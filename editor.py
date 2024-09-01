import time

import pygameextra as pe

import common
from managers import config_manager as cfg_mngr
from itertools import zip_longest
from pygameextra.fpslogger import Logger
from managers.events_manager import handle_events, other_events
from managers.project_manager import load_project, load_selected_file
from managers.text_manager import configure_texts, configure_file_panel_texts
from managers.draggables_manager import configure_draggables
from common import create_title, mouse_rect, surface_rect, file_name, cursor_index, custom_split
from pythonide_types.Texts import Texts
import pythonide_types.Strings as Strings

pe.init()

logger = Logger()
config = cfg_mngr.initialize()
load_project(config)
configure_texts(config)
configure_draggables(config)
pe.settings.hover_lock_enabled = False


def top_panel():
    global config

    # Sub panel logic
    if config.top_sub_panel_surface:  # it exists
        # Check if the mouse is within it, quit the checks below for top panel to prevent close
        if mouse_rect(False).colliderect(surface_rect(config.top_sub_panel_surface)):
            top_sub_panel(config.top_sub_panel_x, config.top_sub_panel_identifier)
            return
        elif not config.top_sub_panel_active:  # Disable sub panel is unactivated
            config.top_sub_panel_surface = None
        # Inactivate it to see if it will be reactivated from hover code below
        config.top_sub_panel_active = False

    if config.top_panel_active:  # Top panel is active
        pe.fill.full(config.style.background, config.top_panel_surface)  # Fill with background

        # Check if mouse is below top panel and close it
        if pe.mouse.pos()[1] > config.top_panel_text_height or not config.top_panel_surface:
            config.top_panel_active = False
            config.top_sub_panel_surface = None
            # The following removes any button hover by spoofing the mouse
            pe.settings.spoof_mouse_position = (0, config.top_panel_text_height + 2)
        context = pe.display.display_reference  # Save display backup
        pe.display.context(config.top_panel_surface)  # Set the context to top panel
        x = 0
        for i, text in enumerate(config.top_panel_texts):
            # Display buttons
            pe.button.rect((x, 0,
                            text.rect[2] + config.style.top_panel_button_padding_horizontal,
                            config.top_panel_text_height),
                           config.style.background, config.style.button_select,
                           text, hover_action=top_sub_panel, hover_data=(x, Strings.top_panel_identifiers[i]))
            x += text.rect[2] + config.style.top_panel_button_padding_horizontal
        pe.display.context(context)  # Return display context
        pe.draw.line(config.style.background_shadow,
                     (0, config.top_panel_text_height),
                     (config.window_width, config.top_panel_text_height),
                     3, config.top_panel_surface)
        if pe.mouse.pos()[1] > config.top_panel_text_height or not config.top_panel_surface:
            pe.settings.spoof_mouse_position = None  # Reset the spoof
    elif mouse_y := pe.mouse.pos()[1] <= config.top_panel_text_height and pe.mouse.clicked()[
        0] or not config.top_panel_surface:
        # Activate the panel
        config.top_panel_active = True
        if not config.top_panel_surface:
            pe.settings.spoof_mouse_position = (0, config.window_height * 10)
        config.top_panel_surface = pe.Surface((config.window_width, config.top_panel_text_height))


def on_top_panel(identifier, sub):
    config.top_sub_panel_surface = None
    config.top_sub_panel_active = False
    config.top_panel_active = True


def top_sub_panel(x, identifier):
    global config

    # Disable button locking and align mouse
    pe.settings.spoof_mouse_position = pe.mouse.pos()
    pe.settings.spoof_mouse_position = (
        pe.settings.spoof_mouse_position[0] - x,
        pe.settings.spoof_mouse_position[1] - config.top_panel_text_height,
    )

    if not config.top_sub_panel_surface or identifier != config.top_sub_panel_identifier:
        config.top_sub_panel_surface = pe.Surface((
            config.top_sub_panel_width[identifier],
            config.top_sub_panel_height[identifier]
        ))  # Create surface

    # Set position and activate
    config.top_sub_panel_surface.pos = (x, config.top_panel_text_height - 1)
    pe.fill.full(config.style.background, config.top_sub_panel_surface)
    config.top_sub_panel_active = True

    context = pe.display.display_reference  # Save display backup
    pe.display.context(config.top_sub_panel_surface)  # Set the context to top panel

    # Render options
    y = 0
    for i, (text, button_identifier) in enumerate(zip(config.top_sub_panel_texts[identifier],
                                                      Strings.top_sub_panel_identifiers[identifier])):
        if button_identifier == '_%_':
            # y +=
            pe.draw.line(config.style.background_shadow, (0, y),
                         (config.top_sub_panel_width[identifier], y), 1)
            y += 1
            continue
        button_end = text.rect[2] + config.style.top_sub_panel_button_padding_horizontal
        pe.button.rect((button_end, y,
                        config.top_sub_panel_width[identifier] - button_end,
                        config.top_panel_text_height),
                       config.style.background, config.style.button_select,
                       hover_action=pe.draw.rect,
                       hover_data=(config.style.button_select,
                                   (0, y, button_end, config.top_panel_text_height), 0
                                   ), action=on_top_panel, data=(identifier, button_identifier))
        pe.button.rect((0, y, button_end,
                        config.top_panel_text_height),
                       (0, 0, 0, 0), config.style.button_select,
                       text, hover_action=pe.draw.rect,
                       hover_data=(config.style.button_select,
                        (button_end, y,
                         config.top_sub_panel_width[identifier] - button_end,
                         config.top_panel_text_height), 0
                        ), action=on_top_panel, data=(identifier, button_identifier))
        if not config.top_sub_panel_active:
            pe.display.context(context)
            return

        y += text.rect[3] + config.style.top_sub_panel_button_padding_vertical
    pe.draw.rect(config.style.background_shadow,  # Shadow
                 (0, 0, *config.top_sub_panel_surface.size), 1,
                 config.top_sub_panel_surface)
    pe.display.context(context)  # Return display context
    config.top_sub_panel_x, config.top_sub_panel_identifier = x, identifier
    pe.settings.spoof_mouse_position = None  # Reset mouse spoof


def left_panel():
    global config
    if config.left_panel_active and not config.top_sub_panel_active:
        pe.fill.full(config.style.background, config.left_panel_surface)  # Fill with background
        pe.draw.line(config.style.background_shadow,
                     (config.current_project.left_panel_size, 0),
                     (config.current_project.left_panel_size,
                      config.window_height - config.top_panel_text_height),
                     3, config.left_panel_surface)
    elif not config.left_panel_surface:
        config.left_panel_surface = pe.Surface((
            config.current_project.left_panel_size,
            config.window_height - config.top_panel_text_height
        ))
        config.left_panel_surface.pos = (0, config.top_panel_text_height)
        config.left_panel_active = True


def file_panel():  # Opened files, not the left panel
    global config
    if config.file_panel_active and not config.top_sub_panel_active:
        pe.fill.full(config.style.background, config.file_panel_surface)  # Fill with background
        context = pe.display.display_reference  # Save display backup
        pe.display.context(config.file_panel_surface)  # Set the context to top panel
        pe.settings.spoof_mouse_position = pe.mouse.pos()
        pe.settings.spoof_mouse_position = (
            pe.settings.spoof_mouse_position[0] - config.current_project.left_panel_size,
            pe.settings.spoof_mouse_position[1] - config.top_panel_text_height,
        )
        x = 0

        for i, (file, text) in enumerate(zip(config.current_project.files_opened,
                                             config.file_panel_texts)):
            selected = text.text == file_name(config.current_project.file_selected)
            pe.button.rect((x, 0,
                            text.rect[2] + config.style.file_panel_button_padding_horizontal,
                            config.file_panel_text_height),
                           *(config.style.background, config.style.button_select) if not selected else
                           (config.style.code, config.style.code),
                           text, action=config.current_project.set_selected_file,
                           data=(file, config))
            x += text.rect[2] + config.style.file_panel_button_padding_horizontal
        pe.display.context(context)
        pe.draw.line(config.style.background_shadow,
                     (0, config.top_panel_text_height),
                     (config.window_width - config.current_project.left_panel_size,
                      config.top_panel_text_height),
                     3, config.file_panel_surface)
        x = 0
        for text in config.file_panel_texts:
            x_add = text.rect[2] + config.style.file_panel_button_padding_horizontal
            if text.text == file_name(config.current_project.file_selected):
                pe.draw.line(config.style.button_select,
                             (x, config.top_panel_text_height),
                             (x + x_add - 1,
                              config.top_panel_text_height),
                             config.style.file_panel_selected_size, config.file_panel_surface)
            x += x_add
        pe.settings.spoof_mouse_position = None
    elif not config.file_panel_surface:
        config.file_panel_surface = pe.Surface((
            config.window_width - config.current_project.left_panel_size,
            config.file_panel_text_height
        ))
        config.file_panel_surface.pos = (config.current_project.left_panel_size, config.top_panel_text_height)
        config.file_panel_active = True


def make_word(word, i=None, i2=None):
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


def code_panel():
    global config
    rerun = False
    if config.code_panel_active and not config.top_sub_panel_active:
        pe.fill.full(config.style.code, config.code_panel_surface)  # Fill with background
        context = pe.display.display_reference  # Save display backup
        pe.display.context(config.code_panel_surface)  # Set the context to top panel
        pe.settings.spoof_mouse_position = pe.mouse.pos()
        pe.settings.spoof_mouse_position = (
            pe.settings.spoof_mouse_position[0] - config.current_project.left_panel_size,
            pe.settings.spoof_mouse_position[1] - (config.top_panel_text_height + config.file_panel_text_height),
        )
        #
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
                    config.code_texts[i].texts.append(make_word(word))
            if check_for_changes:
                config.code_hashes[i] = hash(line)
                just_go = False
                for i2, (word, old) in enumerate(zip_longest(custom_split(line), [
                    text.text for text in config.code_texts[i].texts
                ])):
                    if word is None: continue
                    if old is None:
                        config.code_texts[i].texts.insert(i2, make_word(word, i, i2))
                    elif (word != old) or just_go:
                        config.code_texts[i].texts[i2] = make_word(word, i, i2)
                        if config.style.syntax_color_lock.get(old): just_go = True
                if not config.code_text_height:
                    config.code_text_height = config.code_texts[i].texts[0].rect[3]
                config.code_texts[i].combine(config.style.text_spacing, config.code_text_height)
        y = 0
        for linei, texts in enumerate(config.code_texts):
            if texts.combined:
                pe.display.blit(texts.combined, [v+o for v, o in zip((x, y), config.code_panel_surface_offset)])
            else:
                texts.combine(config.style.text_spacing, config.code_text_height)
            y += texts.combined.size[1]
            if cursor_line == linei and time.time() - config.cursor_blink_state < config.cursor_blink_time_in:
                pe.draw.line(config.style.code_cursor_select, [v+o for v, o in zip((cursor_x, y), config.code_panel_surface_offset)], [v+o for v, o in zip((cursor_x, y - texts.combined.size[1]), config.code_panel_surface_offset)],
                             config.style.code_cursor_width)

        #
        pe.display.context(context)
        pe.settings.spoof_mouse_position = None
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
        code_panel()


def code_sub_panel():
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


print(
    f"{common.APP_NAME} by "
    f"{common.APP_AUTHOR} version "
    f"{common.APP_VERSION} {common.APP_CHANNEL} "
    f"running on PGE version {pe.__version__}"
)
pe.display.make(config.window_size(), create_title(config), pe.display.DISPLAY_MODE_RESIZABLE)
while True:
    handle_events(config)
    other_events(config)

    top_panel()  # File, edit, so on
    left_panel()  # Files tree view
    file_panel()  # files select
    code_sub_panel()  # Code line numbers
    code_panel()  # Code editor

    pe.display.blit(config.code_panel_surface, config.code_panel_surface.pos)
    pe.display.blit(config.code_sub_panel_surface, config.code_panel_surface.pos)
    pe.display.blit(config.file_panel_surface, config.file_panel_surface.pos)
    pe.display.blit(config.left_panel_surface, config.left_panel_surface.pos)
    pe.display.blit(config.top_panel_surface)

    # Display dialogs above all else
    if config.top_sub_panel_surface:
        pe.display.blit(config.top_sub_panel_surface, config.top_sub_panel_surface.pos)

    # logger.render()
    pe.display.update(60)
