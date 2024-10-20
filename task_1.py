from collections import UserDict

# Decorator for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact does not exist"
        except ValueError as err:
            return err.args[0]
        except IndexError:
            return "Enter the argument for the command"
    return inner


# Base class Field
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Class to store name
class Name(Field):
    pass


# Class for storing and validation phone number
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")


# Class for storing records
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone_number, new_phone_number):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit:
            self.phones.remove(phone_to_edit)
            self.add_phone(new_phone_number)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# Class for work with address book
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


# CLI Functions
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, address_book):
    # TODO Add the ability to set more than one phone number!
    name, phone = args

    # Our add_contact function has two purposes - adding a new contact or
    # updating the phone number for a contact that already exists in the address book.
    # if address_book.find(name):
    #     raise ValueError(f"Contact '{name}' exist in address book.")

    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact '{name}' added with phone {phone}"


@input_error
def change_contact(args, address_book):
    # TODO Add the ability to change more than one phone number!
    name, phone = args
    record = address_book.find(name)
    if record:
        # Editing only first phone!
        record.edit_phone(record.phones[0].value, phone)
        return f"Contact '{name}' updated."
    raise KeyError


@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return f"Phone for '{name}': {', '.join([p.value for p in record.phones])}"
    raise KeyError


@input_error
def show_all(address_book):
    if address_book:
        result = "\n".join([f"{name}: {', '.join([p.value for p in record.phones])}" for name, record in address_book.items()])
        return f"All contacts:\n{result}"
    return "No contacts found"


def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book))
        else:
            print("Invalid command.")


# Start the main function
if __name__ == "__main__":
    main()
