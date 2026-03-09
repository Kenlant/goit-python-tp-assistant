from prompt_toolkit import choice, prompt
from ...core.contacts_book.contacts_book import ContactsBook, Record
from datetime import datetime, timedelta


def find(prev, success_callback, contacts_book: ContactsBook):
    func_dict = {
        "name": lambda input: lambda record: input in record.name.value,
        "address": lambda input: lambda record: record.address and input in record.address.value,
        "phone": lambda input: lambda record: record.phones and any([input.casefold() in phone.value for phone in record.phones]),
        "birthday": lambda input: lambda record: record.birthday and input in str(record.birthday),
        "email": lambda input: lambda record: record.email and input in record.email.value,
    }

    result = choice(
        message="Search a contact by:",
        options=[
            ("name", "Name"),
            ("address", "Address"),
            ("phone", "Phone"),
            ("birthday", "Birthday"),
            ("email", "Email"),
            ("upcomming_birthday", "Upcomming Birthday"),
            ("back", "Back")
        ])

    def current_step():
        return find(prev, success_callback, contacts_book)

    if result in func_dict.keys():
        contacts = search_by(current_step, contacts_book, func_dict[result])
        display_list(current_step, success_callback, contacts)
    elif result == "upcomming_birthday":
        contacts = search_by_upcoming_birthday(current_step, contacts_book)
        display_list(current_step, success_callback, contacts)
    else:
        prev()


def show_all(prev, success_callback, contacts_book: ContactsBook):
    display_list(prev, success_callback, contacts_book.data)


def display_list(prev, success_callback, contacts: list[Record]):
    message = "No contacts match criteria." if len(
        contacts) == 0 else "Choose a contact:"

    options = [(x.id, str(x)) for x in contacts]
    options.append(("back", "Back"))

    result = choice(message=message, options=options)

    if (result == "back"):
        prev()
    else:
        contact = next(filter(lambda x: x.id == result, contacts))
        success_callback(contact)


def search_by(prev, contact_book: ContactsBook, predicate):
    input = prompt("Enter a query (Leave empty to exit): ")

    if (input == ""):
        prev()
        return

    return contact_book.get_list(predicate(input))


def search_by_upcoming_birthday(prev, contact_book: ContactsBook):
    input = prompt(
        "Enter the number of days for the date range starting today (leave empty to exit): ")

    if (input == ""):
        prev()
        return

    if (not input.isdigit()):
        search_by_upcoming_birthday(prev, contact_book)
        return

    start_date = datetime.now()
    end_date = start_date + timedelta(days=float(input))

    return contact_book.get_list_by_next_birthday(start_date, end_date)
