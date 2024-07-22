from functools import wraps
from collections import UserDict

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Enter contact name."
        except IndexError:
            return "Check the phone number."
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for user_phone in self.phones:
            if user_phone.value == phone.value:
                self.phones.remove(user_phone)
                break

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        result = []
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result)

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, address_book):
    if len(args) != 2:
        return "Error: Please provide both name and phone number."
    name, phone = args
    if name in address_book:
        address_book[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, address_book):
    if len(args) != 2:
        return "Error: Please provide both name and new phone number."
    name, new_phone = args
    record = address_book.find(name)
    if record:
        if record.phones:
            record.edit_phone(record.phones[0], new_phone)
            return f"Contact {name}'s phone number has been changed to {new_phone}."
        else:
            return "No existing phone number to replace."
    else:
        return f"No contact found under the name {name}."

@input_error
def show_phone_number(args, address_book):
    if len(args) != 1:
        return "Please provide name only."
    name = args[0]
    record = address_book.find(name)
    if record:
        if record.phones:
            return f"{name}'s phone number is {record.phones[0]}."
        else:
            return f"No phone numbers found for {name}."
    else:
        return f"No contact found under the name {name}."

@input_error
def show_contacts(args, address_book):
    if not address_book:
        return "You have no friends."
    else:
        return str(address_book)

@input_error
def delete_friend(args, address_book):
    if len(args) != 1:
        return "Please provide name only."
    name = args[0]
    if name in address_book:
        address_book.delete(name)
        return f"{name} was removed from your contacts."
    else:
        return f"No contact found under the name {name}."

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in {"close", "exit"}:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone_number(args, address_book))
        elif command == "all":
            print(show_contacts(args, address_book))
        elif command == "delete":
            print(delete_friend(args, address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
