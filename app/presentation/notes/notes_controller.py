from prompt_toolkit import choice
from .notes_search_controller import show_all, find
from .notes_management_controller import add, manage
from ...core.notes.notepad import Notepad

notepad = Notepad.load_data()


def notepad_main_menu(prev):
    result = choice(
        message="Notepad",
        options=[
            ("add_note", "Add Note"),
            ("find_note", "Find Note"),
            ("show_all", "Show All"),
            ("back", "Back")
        ])

    def current_step(): return notepad_main_menu(prev)
    def manage_func(x): return manage(current_step, x, notepad)

    match result:
        case "add_note": add(current_step, notepad)
        case "find_note": find(current_step, manage_func, notepad)
        case "show_all": show_all(current_step, manage_func, notepad)
        case _: prev()
