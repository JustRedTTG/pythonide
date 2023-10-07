class Language:
    top_panel_texts: tuple[str, ...] = ("File", "Edit")
    top_sub_panel_texts: dict[str, tuple[str, ...]] = {
        "file":("New Project...", "New...", "Open...", '_%_', "Settings"),
        "edit":("Undo", "Redo", '_%_', "Cut", "Copy", "Paste")
    }


languages: dict[str, Language] = {
    "en": Language(),
}