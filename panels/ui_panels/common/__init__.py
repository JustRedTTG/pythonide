from abc import ABC, abstractmethod
import pygameextra as pe
from pythonide_types.Config import Config


class Module(ABC):

    def __init__(self, x, y, config: Config):
        self.x, self.y = x, y
        self.config = config
        self.surface = pe.display.display_reference
        self.id = id(pe.display.display_reference)

    @property
    def data(self):
        return self.config.ui_panel_data[self.id]

    @data.setter
    def data(self, value):
        self.config.ui_panel_data[self.id] = value

    @property
    def rect(self):
        rect = pe.Rect(self.x, self.y, *self.surface.size)
        rect.width -= self.x
        rect.height -= self.y
        return rect

    @property
    def type(self):
        return self.data['type']

    @property
    def draggable(self):
        return self.data['draggable']

    @property
    def window_pos(self):
        return self.data['window_pos']

    @abstractmethod
    def loop(self):
        ...

    def __call__(self, *args, **kwargs):
        # noinspection PyArgumentList
        self.loop(*args, **kwargs)
