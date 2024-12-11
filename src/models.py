from abc import ABC, abstractmethod
from src.utils import ascii_art

class User(ABC):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @abstractmethod
    def authenticate(self, password):
        pass

class Admin(User):
    def __init__(self, _id, name, age, email, password=None, phone_number=None):
        super().__init__(name, password)
        self.id = _id
        self.age = age
        self.email = email
        self.phone_number = phone_number

    def authenticate(self, password):
        return self.password == password

class Passenger(User):
    def __init__(self, _id, name, age, email, password=None, phone_number=None):
        super().__init__(name, password)
        self.id = _id
        self.age = age
        self.email = email
        self.phone_number = phone_number
    
    def authenticate(self, password):
        return self.password == password

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Age": self.age,
            "Email": self.email,
            "Phone Number": self.phone_number
        }

class Flight:
    def __init__(self, flight_number, departure, arrival, capacity):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.capacity = capacity


# menus.py

class MenuItem:
    def __init__(self, label, action):
        self.label = label
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)

class Menu:
    def __init__(self, title, items):
        self.title = title
        self.items = items

    def display(self):
        if self.title == 'Main Menu':
            #print(f"Количество опций: {len(self.items)}")
            ascii_art.ascii_main_menu()
        print(f"\n{self.title}\n{'-' * len(self.title)}")
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item.label}")
            #print(f"{i} - {item.action}")

    def execute(self, db_client=None):
        while True:
            choice = input("\nEnter your choice: ")
            print(f"User input: {choice}")  # Debug print statement
            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(self.items):
                    selected_item = self.items[choice_index]
                    selected_item(db_client)
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
            except Exception as e:
                print(f"Error executing menu item: {str(e)}")

class MenuSystem:
    def __init__(self):
        self.menus = {}
        self.current_menu = 'main'
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_email = None
        self.current_user_role = None

    def add_menu(self, menu_name, menu):
        self.menus[menu_name] = menu

    def run_menu(self, menu_name, db_client):
        if menu_name not in self.menus:
            print("Menu not found")
            return

        if self.current_user_email is None and menu_name != 'main':
            print("Please log in first")
            return

        self.menus[menu_name].display()
        self.menus[menu_name].execute(db_client)

    def logout(self):
        self.current_menu = 'main'
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_email = None
        self.current_user_role = None

        