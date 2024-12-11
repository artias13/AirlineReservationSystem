from abc import ABC, abstractmethod
from src.utils import ascii_art

class User(ABC):
    """
    Abstract base class representing a generic user.

    Attributes:
        name (str): The user's name.
        password (str): The user's password.
    """
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @abstractmethod
    def authenticate(self, password):
        """
        Authenticates the user with the given password.

        Args:
            password (str): The password to check against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        pass

class Admin(User):
    """
    Represents an administrator user.

    Attributes:
        id (int): The unique identifier for the admin.
        name (str): The admin's name.
        age (int): The admin's age.
        email (str): The admin's email address.
        password (str): The admin's password.
        phone_number (str): The admin's phone number.
    """
    def __init__(self, _id, name, age, email, password=None, phone_number=None):
        super().__init__(name, password)
        self.id = _id
        self.age = age
        self.email = email
        self.phone_number = phone_number

    def authenticate(self, password):
        """
        Authenticates the admin user with the given password.

        Args:
            password (str): The password to check against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password

class Passenger(User):
    """
    Represents a passenger user.

    Attributes:
        id (int): The unique identifier for the passenger.
        name (str): The passenger's name.
        age (int): The passenger's age.
        email (str): The passenger's email address.
        password (str): The passenger's password.
        phone_number (str): The passenger's phone number.
    """
    def __init__(self, _id, name, age, email, password=None, phone_number=None):
        super().__init__(name, password)
        self.id = _id
        self.age = age
        self.email = email
        self.phone_number = phone_number
    
    def authenticate(self, password):
        """
        Authenticates the passenger user with the given password.

        Args:
            password (str): The password to check against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password

    def to_dict(self):
        """
        Converts the Passenger object to a dictionary representation.

        Returns:
            dict: A dictionary containing the passenger's details.
        """
        return {
            "ID": self.id,
            "Name": self.name,
            "Age": self.age,
            "Email": self.email,
            "Phone Number": self.phone_number
        }

class Flight:
    """
    Represents a flight.

    Attributes:
        flight_number (str): The unique identifier for the flight.
        departure (str): The departure location.
        arrival (str): The arrival location.
        capacity (int): The maximum number of passengers the flight can accommodate.
    """
    # not used anywhere really
    def __init__(self, flight_number, departure, arrival, capacity):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.capacity = capacity


# menus

class MenuItem:
    """
    Represents a menu item with a label and associated action.

    Attributes:
        label (str): The text displayed for the menu item.
        action (function): The function to call when the item is selected.
    """
    def __init__(self, label, action):
        self.label = label
        self.action = action

    def __call__(self, *args, **kwargs):
        """
        Calls the associated menu function with the given arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of calling the action function.
        """
        return self.action(*args, **kwargs)

class Menu:
    """
    Represents a menu system with a title and items.

    Attributes:
        title (str): The title of the menu.
        items (list[MenuItem]): List of MenuItem objects.
    """
    def __init__(self, title, items):
        self.title = title
        self.items = items

    def display(self):
        """
        Displays the menu to the user.

        Prints the title and each menu item with its index.
        """
        if self.title == 'Main Menu':
            ascii_art.ascii_main_menu()
        print(f"\n{self.title}\n{'-' * len(self.title)}")
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item.label}")

    def execute(self, db_client=None):
        """
        Executes the selected menu item.

        Prompts the user for their choice, validates it, and calls the associated action function.

        Args:
            db_client: The database client instance (optional).
        """
        while True:
            choice = input("\nEnter your choice: ")
            #print(f"User input: {choice}") 
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
    """
    Manages multiple menus and keeps track of the current user session.

    Attributes:
        menus (dict[str, Menu]): Dictionary of menus keyed by menu name.
        current_menu (str): The name of the currently active menu.
        current_user_id (int): The ID of the currently logged-in user.
        current_user_name (str): The name of the currently logged-in user.
        current_user_email (str): The email of the currently logged-in user.
        current_user_role (str): The role of the currently logged-in user.
    """
    def __init__(self):
        self.menus = {}
        self.current_menu = 'main'
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_email = None
        self.current_user_role = None

    def add_menu(self, menu_name, menu):
        """
        Adds a new menu to the menu system.

        Args:
            menu_name (str): The name of the menu.
            menu (Menu): The Menu object to add.
        """
        self.menus[menu_name] = menu

    def run_menu(self, menu_name, db_client):
        """
        Runs the specified menu.

        Checks if the menu exists and if the user is logged in (for non-main menus).
        Then displays and executes the menu.

        Args:
            menu_name (str): The name of the menu to run.
            db_client: The database client instance.
        """
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

        