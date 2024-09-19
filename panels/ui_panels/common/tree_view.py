import os
from collections.abc import Iterable, Generator
from typing import Union

import jaraco.path
import pygameextra as pe

from panels.ui_panels.common import Module
from pythonide_types.Config import Config


class TreeNode:
    def __init__(self, name: str, children: Union["TreeDataType", None], expanded: bool = False, click_tag: str = None):
        self.name = name
        self.expanded = expanded
        self.children_ready = False if isinstance(children, Generator) else True
        self._children_available = []
        self.children = children
        self.click_tag = click_tag
        self.has_children = True
        if not self.children_ready:
            try:
                self._children_available.append(next(self.children))
            except StopIteration:
                self.has_children = False
                self.children = None
        else:
            self.has_children = children is not None and len(children) > 0

    def toggle(self):
        self.expanded = not self.expanded

    def get(self):
        if self.children is None:
            return None
        if isinstance(self.children, Generator):
            if not self.children_ready:
                try:
                    self._children_available.append(next(self.children))
                except StopIteration:
                    self.children_ready = True
            return self._children_available
        return self.children

    @classmethod
    def create_directory_tree(cls, tree_path: str = None) -> "TreeDataType":
        if not tree_path:
            tree_path = os.path.abspath(os.sep)

        def generator(path: str):
            directories = []
            files = []
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    directories.append(item)
                else:
                    files.append(item)
            for item in directories:
                if not jaraco.path.is_hidden(joined := os.path.join(path, item)):
                    yield cls(item, generator(joined))
            for item in reversed(files):
                yield cls(item, None, click_tag=os.path.join(path, item))

        return (cls(tree_path, generator(tree_path)),)


TreeDataType = Iterable[TreeNode]


class TreeView(Module):
    def __init__(self, x: int, y: int, config: Config, tree: TreeDataType):
        super().__init__(x, y, config)
        self.tree = tree
        self.texts = {}
        if x > 0 or y > 0:
            self.tree_surface = pe.Surface(self.rect.size)
        else:
            self.tree_surface = None

    def draw_node(self, node: TreeNode, depth: int, rect: pe.Rect, root_point: tuple = None):
        my_rect: pe.Rect = rect.copy()
        my_rect.left += 10
        line_color = self.config.style.background_shadow
        # if not depth == 0:
        #     pe.draw.line(line_color, my_rect.topleft, (my_rect.left, my_rect.centery), 1)
        line_left = my_rect.left

        if root_point:
            if node.has_children or node.expanded:
                pe.draw.line(line_color, my_rect.midleft, (root_point[0], my_rect.centery), 1)
            pe.draw.line(line_color, (root_point[0], my_rect.centery), root_point, 1)

        root_point = my_rect.midleft

        my_rect.left += 30
        # pe.draw.line(line_color, (line_left, my_rect.centery), (my_rect.left, my_rect.centery), 1)

        if node.name not in self.texts:
            self.texts[node.name] = pe.Text(
                node.name, self.config.font_filepaths.thin,
                20, colors=(self.config.style.text_color, None)
            )

        if node.has_children:
            icon_rect = pe.Rect(0, 0, my_rect.height, my_rect.height)
            icon_rect.midright = my_rect.midleft
            icon_rect.scale_by_ip(.5, .5)
            name = 'arrow_down' if node.expanded else 'arrow_right'
            self.config.icon_filepaths[name].resize = icon_rect.size
            self.config.icon_filepaths[name].display(icon_rect.topleft)

        if node.has_children or node.click_tag:
            button_rect = my_rect.copy()
            button_rect.width = self.surface.width
            button_rect.x = 0
            pe.button.rect(
                button_rect, (0, 0, 0, 0), (255, 255, 255, 50),
                action=node.toggle, name=f'tree_view_long[{self.id}]_{id(node)}>'
            )

        self.texts[node.name].rect.topleft = my_rect.topleft
        self.texts[node.name].display()

        my_rect.top = my_rect.bottom

        if node.has_children:
            if node.expanded:
                # pe.draw.line(line_color, (line_left, my_rect.top-my_rect.height//2), (line_left, my_rect.top), 1)
                # pe.draw.line(pe.colors.red, (line_left+length / 2, my_rect.top), (my_rect.left+10, my_rect.top), 1)
                for child in node.get():
                    self.draw_node(child, depth + 1, my_rect, root_point)

        rect.top = my_rect.top

    def loop(self):
        rect = pe.Rect(0, 0, pe.display.get_width(), 30)
        for node in self.tree:
            self.draw_node(node, 0, rect)

    def __call__(self, *args, **kwargs):
        if self.tree_surface:
            with self.tree_surface:
                self.loop(*args, **kwargs)
            pe.display.blit(self.tree_surface, (self.x, self.y))
            return
        self.loop(*args, **kwargs)
