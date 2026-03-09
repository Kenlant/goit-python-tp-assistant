from collections import UserDict
from collections.abc import Callable
from ..base.stateful_service import StatefullService


class Note:
    CURRENT_ID = 0

    def __init__(self, text):
        self.id = self.CURRENT_ID
        self.tags = set()
        self.text = text

        self.CURRENT_ID += 1

    def update_note(self, text):
        self.text = text

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def __str__(self):
        preview_text_length = 10

        preview = self.text[:preview_text_length]
        preview = preview if len(preview) == len(
            self.text) else f"{preview}..."
        if (self.tags):
            preview += f"     Tags:{" ".join(self.tags)}"

        return preview


class Notepad(UserDict, StatefullService):
    def add_note(self, note: Note):
        self.data[note.id] = note

    def delete(self, id):
        del self[id]

    def get_list(self, predicate: Callable[[Note], bool] = None):
        if (not predicate):
            return self.data

        return list(filter(predicate, self.data.values()))

    @staticmethod
    def load_data():
        notepad = StatefullService.load_data("notepad.pkl", Notepad)
        Note.CURRENT_ID = max(
            [x.id for x in notepad.data.values()]) + 1 if notepad.data else 0
        return notepad

    def save_data(self):
        return super().save_data("notepad.pkl")
