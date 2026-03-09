from prompt_toolkit import choice, prompt
from ...core.contacts_book.contacts_book import Record, ContactsBook
from ..promt_helpers import promt_yes_no
from ..infrastructure.decorators.input_error import handle_input_error_and_repeat


def manage(prev, contact, contacts_book: ContactsBook):
    result = choice(
        message="Manage a contact:",
        options=[
            ("delete", "Delete"),
            ("edit", "Edit"),
            ("back", "Back")
        ])

    match result:
        case "delete": delete(prev, contact, contacts_book)
        case "edit": update(lambda: manage(prev, contact, contacts_book), contact, contacts_book)
        case _: prev()


def delete(prev, contact: Record, contacts_book: ContactsBook):
    contacts_book.delete(contact)
    contacts_book.save_data()
    prompt(
        f"Contact {contact.name} was deleted. Press enter to return to main menu")
    prev()


def update(prev, contact: Record, contact_book: ContactsBook):
    result = choice(
        message="Choose a property to update:",
        options=[
            ("name", "Name"),
            ("address", "Address"),
            ("phone", "Phone"),
            ("email", "Email"),
            ("birthday", "Birthday"),
            ("back", "Back")
        ])

    match result:
        case "name": update_name(contact)
        case "address": update_address(contact)
        case "email": update_email(contact)
        case "phone": update_phone(contact)
        case "birthday": update_birthday(contact)
        case "back":
            prev()
            return

    contact_book.save_data()

    prompt(
        f"Contact {contact.name} was updated. Press any button")
    update(prev, contact, contact_book)


def add(prev, contacts_book: ContactsBook):
    name = prompt("Enter a name (leave empty to exit): ")
    if (name == ""):
        prev()

    record = Record(name)

    update_address(record)
    update_birthday(record)
    update_email(record)
    update_phone(record)

    contacts_book.add_record(record)

    if (promt_yes_no("Save record?")):
        contacts_book.save_data()

    prev()


@handle_input_error_and_repeat
def update_name(contact: Record):
    new_name = prompt("Enter name: ", default=contact.name.value)
    if new_name:
        contact.update_name(new_name)


@handle_input_error_and_repeat
def update_address(contact: Record):
    default_value = contact.address.value if contact.address else ""
    new_address = prompt(
        "Enter address (Leave empty to skip): ", default=default_value)
    if (new_address):
        contact.add_address(new_address)


@handle_input_error_and_repeat
def update_birthday(contact: Record):
    default_value = str(contact.birthdays) if contact.birthday else ""
    new_birthday = prompt(
        "Enter birthday in DD.MM.YYYY format (Leave empty to skip): ", default=default_value)
    if (new_birthday):
        contact.add_birthday(new_birthday)


@handle_input_error_and_repeat
def update_email(contact: Record):
    default_value = contact.email.value if contact.email else ""
    new_email = prompt("Enter email (Leave empty to skip): ",
                       default=default_value)
    if new_email:
        contact.add_email(new_email)


@handle_input_error_and_repeat
def update_phone(contact: Record):
    options = [(x.value, x.value) for x in contact.phones]
    options.append(("", "Add Phone"))
    options.append(("back", "Back"))
    update_choice = choice(
        message="Phones: ",
        options=options
    )

    if (update_choice == "back"):
        return

    new_phone_number = prompt("Enter phone: ", default=update_choice)
    phone_record = next(filter(lambda x: x.value ==
                               update_choice, contact.phones), None)

    if phone_record == None:
        contact.add_phone(new_phone_number)
    else:
        phone_record.value = new_phone_number
