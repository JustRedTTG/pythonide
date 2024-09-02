from copy import copy

import pygameextra as pe
from common import mouse_rect, surface_rect
from panels.ui_panels import create_ui_panel
from pythonide_types import Strings
from pythonide_types.Config import Config


def top_panel(config: Config):
    # Sub panel logic
    if config.top_sub_panel_surface:  # it exists
        # Check if the mouse is within it, quit the checks below for top panel to prevent close
        if mouse_rect().colliderect(surface_rect(config.top_sub_panel_surface)):
            sub_panel_collide = True
            top_sub_panel(config)
            return
        elif not config.top_sub_panel_active:  # Disable sub panel is unactivated
            config.top_sub_panel_surface = None
            config.top_sub_panel_identifier = None
        # Inactivate it to see if it will be reactivated from hover code below
        config.top_sub_panel_active = False

    if config.top_panel_active:  # Top panel is active
        # Check if mouse is below top panel and close it
        with config.top_panel_surface:
            in_top = pe.mouse.pos()[1] < config.top_panel_text_height
            if not in_top or not config.mouse_moved:
                config.top_panel_active = False

            pe.fill.full(config.style.background)  # Fill with background
            x = 0
            for i, text in enumerate(config.top_panel_texts):
                # Display buttons
                width = text.rect[2] + config.style.top_panel_button_padding_horizontal
                rect = (x, 0,
                        width,
                        config.top_panel_text_height)
                if x <= pe.mouse.pos()[0] <= x+width and config.top_sub_panel_identifier == Strings.top_panel_identifiers[i] and in_top:
                    pe.draw.rect(config.style.button_select, rect, 0)  # Highlight selected
                    text.display()
                    top_sub_panel(config, x, config.top_sub_panel_identifier)
                else:
                    pe.button.rect(rect,  # Draw button
                                   config.style.background, config.style.button_select if config.mouse_moved else config.style.background,
                                   text, hover_action=top_sub_panel,
                                   hover_data=(config, copy(x), Strings.top_panel_identifiers[i]), name=f'top_panel_{i}_active')
                x += width
            pe.draw.line(config.style.background_shadow,
                         (0, config.top_panel_text_height),
                         (config.window_width, config.top_panel_text_height),
                         3)
    elif mouse_y := pe.mouse.pos()[1] <= config.top_panel_text_height and \
                    pe.mouse.clicked()[0] or not config.top_panel_surface:
        # Activate the panel
        config.top_panel_active = config.mouse_moved or config.top_panel_surface is None
        config.top_panel_surface = pe.Surface((config.window_width, config.top_panel_text_height))
    elif config.top_panel_soiled or config.mouse_moved and config.previous_mouse_pos[1] <= config.top_panel_text_height:
        # Do only a little hover effect on the buttons
        x = 0

        with pe.mouse.Offset((0, pe.display.get_height()-pe.mouse.pos()[1])):
            config.top_panel_active = True
            top_panel(config)
            config.top_panel_active = False
            config.top_panel_soiled = False

        def hover_action(x):
            pe.draw.line(
                config.style.background_shadow,
                (x, config.top_panel_text_height),
                (x + width, config.top_panel_text_height), config.style.file_panel_selected_size
            )
            config.top_panel_soiled = True

        with config.top_panel_surface:
            for i, text in enumerate(config.top_panel_texts):
                # Display buttons
                width = text.rect[2] + config.style.top_panel_button_padding_horizontal
                pe.button.rect((x, 0,
                                width,
                                config.top_panel_text_height),
                               (0, 0, 0, 0), (0, 0, 0, 0),
                               None, hover_action=hover_action,
                               hover_data=x, name=f'top_panel_{i}_soiled')
                x += width



def on_top_panel(config: Config, identifier, sub):
    config.top_sub_panel_surface = None
    # config.top_sub_panel_identifier = None
    config.top_sub_panel_active = False
    config.top_panel_active = True
    # print(identifier, sub)

    if identifier == 'file':
        if sub in ('new', 'open'):
            create_ui_panel(config, f'file_{sub}', ensure_one=True)
        else:
            create_ui_panel(config, sub, ensure_one=True)



def top_sub_panel(config: Config, x=None, identifier=None):
    if not config.mouse_moved:
        return
    if x is None:
        x = config.top_sub_panel_x
    if identifier is None:
        identifier = config.top_sub_panel_identifier

    if not config.top_sub_panel_surface or identifier != config.top_sub_panel_identifier:
        config.top_sub_panel_surface = pe.Surface((
            config.top_sub_panel_width[identifier],
            config.top_sub_panel_height[identifier]
        ))  # Create surface

    # Set position and activate
    config.top_sub_panel_surface.pos = (x, config.top_panel_text_height - 1)
    config.top_sub_panel_surface.last_blit_pos = config.top_sub_panel_surface.pos
    config.top_sub_panel_active = True

    with config.top_sub_panel_surface:
        pe.fill.full(config.style.background)

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
            rect_text = (0, y, button_end,
                         config.top_panel_text_height)
            rect_padding = (button_end, y,
                            config.top_sub_panel_width[identifier] - button_end,
                            config.top_panel_text_height)
            pe.button.rect(rect_padding,
                           config.style.background, config.style.button_select,
                           hover_draw_action=pe.draw.rect,
                           hover_draw_data=(config.style.button_select,
                                       rect_text, 0
                                       ), action=on_top_panel, data=(config, identifier, button_identifier),
                           name=f'top_sub_panel_{i}_front')
            pe.button.rect(rect_text,
                           (0, 0, 0, 0), config.style.button_select,
                           text, hover_draw_action=pe.draw.rect,
                           hover_draw_data=(config.style.button_select,
                                       rect_padding, 0
                                       ), action=on_top_panel, data=(config, identifier, button_identifier),
                           name=f'top_sub_panel_{i}_end')
            if not config.top_sub_panel_active:
                return

            y += text.rect[3] + config.style.top_sub_panel_button_padding_vertical
        pe.draw.rect(config.style.background_shadow,  # Shadow
                     (0, 0, *config.top_sub_panel_surface.size), 1,
                     config.top_sub_panel_surface)

    config.top_sub_panel_x, config.top_sub_panel_identifier = x, identifier
