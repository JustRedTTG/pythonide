from typing import Tuple, Dict


class Language:
    top_panel_texts: Tuple[str, ...] = ("File", "Edit")
    top_sub_panel_texts: Dict[str, tuple[str, ...]] = {
        "file": ("New Project...", "New...", "Open...", '_%_', "Settings"),
        "edit": ("Undo", "Redo", '_%_', "Cut", "Copy", "Paste")
    }
    ui_panel_texts: Dict[str, str] = {
        "close": "  X  ",
        "new_project": "New Project",
        "settings": "Settings",
        "file_new": "New file",
        "file_open": "Open file or project",
    }


languages: Dict[str, Language] = {
    "en": Language(),
}
