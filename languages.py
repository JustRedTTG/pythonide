from typing import Tuple, Dict


class Language:
    top_panel_texts: Tuple[str, ...] = ("File", "Edit")
    top_sub_panel_texts: Dict[str, str] = {
        "new_project": "New Project...",
        "new": "New...",
        "open": "Open...",
        "settings": "Settings",
        "undo": "Undo",
        "redo": "Redo",
        "cut": "Cut",
        "copy": "Copy",
        "paste": "Paste",
        "delete": "Delete",
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
