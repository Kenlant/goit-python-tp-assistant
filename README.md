# Personal Assistant CLI

A command-line personal assistant application built with Python. It provides two core modules: an **Address Book** for managing contacts and a **Notepad** for managing notes. All data is persisted locally between sessions.

## Features

### Address Book

- Add, edit, and delete contacts
- Contact fields: **name**, **phone** (10-digit), **email**, **birthday** (DD.MM.YYYY), **address**
- Search contacts by: name, phone, email, address, birthday
- Find contacts with **upcoming birthdays** within a specified number of days

### Notepad

- Add, edit, and delete notes
- Note fields: **text**, **tags**
- Search notes by: text content, tag

## Project Structure

```
goit-python-tp-assistant/
├── main.py                         # Entry point
├── requirements.txt
└── app/
    ├── core/                       # Business logic
    │   ├── base/
    │   │   ├── models/field.py     # Base field model
    │   │   └── stateful_service.py # Pickle-based persistence
    │   ├── contacts_book/
    │   │   └── contacts_book.py    # Contact & AddressBook models
    │   ├── notes/
    │   │   └── notepad.py          # Note & Notepad models
    │   └── exceptions.py           # Custom exceptions
    └── presentation/               # CLI controllers
        ├── main_menu_controller.py
        ├── contacts/
        │   ├── contacts_controller.py
        │   ├── contacts_management_controller.py
        │   └── contacts_search_controller.py
        └── notes/
            ├── notes_controller.py
            ├── notes_management_controller.py
            └── notes_search_controller.py
```

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd goit-python-tp-assistant
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python main.py
```

You will be presented with an interactive menu to navigate between the **Address Book** and **Notepad** modules. Use arrow keys to navigate options and Enter to select.

## Data Persistence

Data is automatically saved to pickle files in the project root:

- `contactsbook.pkl` — stores address book data
- `notepad.pkl` — stores notepad data

These files are created automatically on first save and loaded on startup.
