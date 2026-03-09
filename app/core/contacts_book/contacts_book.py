from collections import UserList
from datetime import datetime
from ..exceptions import InvalidPhoneFormat, InvalidEmail, InvalidDateFormat, MissingValueException
from collections.abc import Callable
from ..base.models.field import Field
from ..base.stateful_service import StatefullService
import re


class Name(Field):
    def __init__(self, value):
        if (not value):
            raise MissingValueException("Name is not provided")

        super().__init__(value)


class Phone(Field):
    PHONE_LENGTH = 10

    def validate(self, value):
        if (len(value) != self.PHONE_LENGTH or not value.isdigit()):
            raise InvalidPhoneFormat("Phone must contain 10 digits")

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def set_value(self, value):
        self.validate(value)
        self.value = value


class Birthday(Field):
    FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, self.FORMAT))
        except ValueError as e:
            raise InvalidDateFormat("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime(self.FORMAT)


class Address(Field):
    pass


class Email(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"

        if (re.fullmatch(email_pattern, value) == None):
            raise InvalidEmail("Invalid email")


class Record:
    CURRENT_ID = 0

    def __init__(self, name):
        self.id = self.CURRENT_ID
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

        self.CURRENT_ID += 1

    def __str__(self):
        result = f"Id: {self.id}"
        result += f", Name: {self.name.value}"

        if (self.birthday):
            result += f", Birthday: {self.birthday}"

        if (self.email):
            result += f", Email: {self.email}"

        if (self.address):
            result += f", Address: {self.address}"

        if (self.phones):
            result += f", Phones: {'; '.join(p.value for p in self.phones)}"

        return result

    def update_name(self, name):
        self.name = Name(name)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def remove_phone(self, phone):
        record_phone = self.find_phone(phone)

        if (record_phone):
            self.phones.remove(record_phone)

    def edit_phone(self, phone, new_phone):
        record_phone = self.find_phone(phone)
        if (record_phone):
            record_phone.value = new_phone

    def find_phone(self, phone):
        return next(
            filter(lambda x: x.value == phone, self.phones), None)


class ContactsBook(UserList, StatefullService):
    def add_record(self, record: Record):
        self.data.append(record)

    def get_list(self, predicate: Callable[[Record], bool] = None):
        if (not predicate):
            return self.data

        return list(filter(predicate, self.data))

    def delete(self, record: Record):
        self.data.remove(record)

    def get_list_by_next_birthday(self, start_date: datetime, end_date: datetime):
        now = datetime.now()

        def get_next_birthday(birthday: datetime):
            current_year_birthday = birthday.replace(year=now.year)
            next_birthday = current_year_birthday if current_year_birthday > now else birthday.replace(
                year=now.year + 1)

            return next_birthday

        def is_date_in_range(birthday: datetime):
            return birthday >= start_date and birthday <= end_date

        filtered_records = filter(
            lambda x: x.birthday != None, self.data)
        filtered_records = filter(
            lambda x: is_date_in_range(get_next_birthday(x.birthday.value)), filtered_records)

        return list(filtered_records)

    @staticmethod
    def load_data():
        book = StatefullService.load_data("contactsbook.pkl", ContactsBook)
        Record.CURRENT_ID = max(
            [x.id for x in book.data]) + 1 if book.data else 0
        return book

    def save_data(self):
        return super().save_data("contactsbook.pkl")
