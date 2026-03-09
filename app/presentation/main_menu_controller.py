from prompt_toolkit import choice
from .contacts.contacts_controller import contacts_book_main_menu
from .notes.notes_controller import notepad_main_menu


def main_menu():
    result = choice(
        message="Personal Assistant",
        options=[
            ("address_book", "Address Book"),
            ("notes", "Notes"),
            ("exit", "Exit")
        ],)

    if (result == "address_book"):
        contacts_book_main_menu(main_menu)
    elif (result == "notes"):
        notepad_main_menu(main_menu)
