from prompt_toolkit import choice, prompt
from ...core.notes.notepad import Notepad, Note
from ..promt_helpers import promt_yes_no
from ..infrastructure.decorators.input_error import handle_input_error_and_repeat


def manage(prev, note, notepad: Notepad):
    result = choice(
        message="Manage a Note:",
        options=[
            ("delete", "Delete"),
            ("edit", "Edit"),
            ("back", "Back")
        ])

    match result:
        case "delete": delete(prev, note, notepad)
        case "edit": update(lambda: manage(prev, note, notepad), note, notepad)
        case _: prev()


def delete(prev, note: Note, notepad: Notepad):
    notepad.delete(note.id)
    notepad.save_data()
    prompt(
        f"Note was deleted. Press enter to return to main menu")
    prev()


def update(prev, note: Note, notepad: Notepad):
    result = choice(
        message="Choose a property to update:",
        options=[
            ("text", "Text"),
            ("tags", "Tags"),
            ("back", "Back")
        ])

    match result:
        case "text": update_text(note)
        case "tags": update_tags(note)
        case "back":
            prev()
            return

    notepad.save_data()

    prompt(
        f"Note was updated. Press any button")
    update(prev, note, notepad)


def add(prev, notepad: Notepad):
    text = prompt("Enter note text (leave empty to exit): ")
    if (text == ""):
        prev()

    record = Note(text)
    update_tags(record)

    notepad.add_note(record)

    if (promt_yes_no("Save note?")):
        notepad.save_data()

    prev()


@handle_input_error_and_repeat
def update_text(note: Note):
    text = prompt("Enter note text (leave empty to exit): ", default=note.text)
    if text:
        note.update_note(text)


@handle_input_error_and_repeat
def update_tags(note: Note):
    options = [(x, x) for x in note.tags]
    options.append(("", "Add Tag"))
    options.append(("back", "Back"))
    update_choice = choice(
        message="Tags: ",
        options=options
    )

    if (update_choice == "back"):
        return

    new_tag = prompt("Enter tag: ", default=update_choice)
    existing_tag = next(filter(lambda x: x == update_choice, note.tags), None)

    if existing_tag == None:
        note.add_tag(new_tag)
    else:
        note.remove_tag(existing_tag)
        note.add_tag(new_tag)
