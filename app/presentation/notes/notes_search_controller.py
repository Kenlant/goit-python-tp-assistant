from prompt_toolkit import choice, prompt
from ...core.notes.notepad import Notepad, Note


def find(prev, success_callback, notepad: Notepad):
    func_dict = {
        "text": lambda input: lambda note: input.casefold() in note.text.casefold(),
        "tag": lambda input: lambda note:  input.casefold() in [x.casefold() for x in note.tags],
    }

    result = choice(
        message="Search a note by:",
        options=[
            ("text", "Text"),
            ("tag", "Tag"),
            ("back", "Back")
        ])

    def current_step():
        return find(prev, success_callback, notepad)

    if result in func_dict.keys():
        contacts = search_by(current_step, notepad, func_dict[result])
        display_list(current_step, success_callback, contacts)
    else:
        prev()


def show_all(prev, success_callback, notepad: Notepad):
    display_list(prev, success_callback, notepad.data.values())


def display_list(prev, success_callback, notes: list[Note]):
    message = "No notes match criteria." if len(
        notes) == 0 else "Choose a note:"

    options = [(x.id, str(x)) for x in notes]
    options.append(("back", "Back"))

    result = choice(message=message, options=options)

    if (result == "back"):
        prev()
    else:
        contact = next(filter(lambda x: x.id == result, notes))
        success_callback(contact)


def search_by(prev, notepad: Notepad, predicate):
    input = prompt("Enter a query (Leave empty to exit): ")

    if (input == ""):
        prev()
        return

    return notepad.get_list(predicate(input))
