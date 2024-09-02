import pygameextra as pe
from editor import PythonideEditor, handle_events, other_events
from editor import loop as pythonide_loop
import managers.events_manager as pythonide_events_manager

pe.init()


class PythonideContext(pe.Context):
    AREA = (800, 600)

    def __init__(self):
        super().__init__()
        self.pythonide_instance = PythonideEditor()
        pythonide_events_manager.resize_event(self.pythonide_instance.config, self.AREA)

    def handle_event(self, e):
        pythonide_events_manager.handle_event(e, self.pythonide_instance.config)

    def events(self):
        other_events(self.pythonide_instance.config)

    def loop(self):
        pythonide_loop(self.pythonide_instance)


class Main(pe.GameContext):
    AREA = (800, 600)
    MODE = pe.display.DISPLAY_MODE_RESIZABLE
    FPS = 60

    def __init__(self):
        super().__init__()
        self.pythonide = PythonideContext()

    def handle_event(self, e):
        super().handle_event(e)

    def loop(self):
        self.pythonide()

    def post_loop(self):
        super().post_loop()

main = Main()

while True:
    main()
