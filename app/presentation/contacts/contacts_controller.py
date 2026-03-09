from prompt_toolkit import choice
from .contacts_search_controller import find, show_all
from .contacts_management_controller import manage, add
from ...core.contacts_book.contacts_book import ContactsBook

contacts_book = ContactsBook.load_data()


def contacts_book_main_menu(prev):
    result = choice(
        message="Address Book",
        options=[
            ("add_record", "Add record"),
            ("find_record", "Find record"),
            ("show_all", "Show All"),
            ("exit", "Back")
        ])

    def current_step(): return contacts_book_main_menu(prev)
    def manage_func(x): return manage(current_step, x, contacts_book)

    match result:
        case "add_record": add(current_step, contacts_book)
        case "find_record": find(current_step, manage_func, contacts_book)
        case "show_all": show_all(current_step, manage_func, contacts_book)
        case _: prev()
