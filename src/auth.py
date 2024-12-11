# auth.py

from src.models import Admin, Passenger
from src.utils import ascii_art, validate_inputs

def auth_action(action, db_client):
    """
    Handles authentication actions based on the given action string.

    Args:
        action (str): The action to perform (e.g., "login_as_admin", "register_as_admin", etc.)
        db_client: The database client instance.

    Raises:
        ValueError: If an unknown action is provided.

    Returns:
        The result of the performed action (varies depending on the action).
    """
    if action == "login_as_admin":
        return login_as_admin(db_client)
    elif action == "register_as_admin":
        register_as_admin(db_client)
    elif action == "login_as_passenger":
        return login_as_passenger(db_client)
    elif action == "register_as_passenger":
        register_as_passenger(db_client)
    else:
        raise ValueError("Unknown action")

def login_as_admin(db_client):
    """
    Attempts to log in an admin user.

    Prompts the user for email and password, checks against the database,
    and returns success status along with admin details if authenticated.

    Args:
        db_client: The database client instance.

    Returns:
        tuple: (success_status, id, name, email, is_admin)
    """
    ascii_art.ascii_admin_login()
    email = validate_inputs.validate_email(input("Enter the admin's email: "))
    password = validate_inputs.validate_password(input("Enter the admin's password: "))

    if not email or not password:
        print("Invalid credentials")
        return False, None, None, None, None

    cursor = db_client.execute("SELECT * FROM users WHERE email = ? AND is_admin = 1", (email,))
    admin_data = cursor.fetchone()

    if admin_data:
        admin = Admin(admin_data[0], admin_data[1], admin_data[2], admin_data[3], admin_data[4], admin_data[5])
        if admin.authenticate(password):
            print(f"Admin {admin_data[3]} logged in successfully")
            return True, admin_data[0], admin_data[1], admin_data[3], admin_data[6]
        else:
            print("Invalid credentials")
            return False, None, None, None, None
    else:
        print("No admin found with that name")
        return False, None, None, None, None

def register_as_admin(db_client):
    """
    Registers a new admin user in the system.

    Prompts the user for admin details, validates inputs, and inserts the data into the database.

    Args:
        db_client: The database client instance.

    Returns:
        None
    """
    ascii_art.ascii_admin_signup()
    name = validate_inputs.validate_non_empty_string(input("Enter the admin's name: "), "Name")
    age = validate_inputs.validate_positive_integer(input("Enter the admin's's age: "), "Age")
    email = validate_inputs.validate_email(input("Enter the admin's email: "))
    password = validate_inputs.validate_password(input("Enter the admin's password: "))
    phone_number = validate_inputs.validate_phone_number(input("Enter the admin's phone number: "))

    try:
        db_client.execute("""
            INSERT INTO users (name, age, email, password, phone_number, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, email, password, phone_number, True))
        
        db_client.commit()
        print(f"Admin {email} registered successfully")
    except Exception as e:
        db_client.rollback()
        print(f"Error registering admin: {str(e)}")

def login_as_passenger(db_client):
    """
    Attempts to log in a passenger user.

    Prompts the user for email and password, checks against the database,
    and returns success status along with passenger details if authenticated.

    Args:
        db_client: The database client instance.

    Returns:
        tuple: (success_status, id, name, email, is_admin)
    """
    ascii_art.ascii_customer_login()
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    password = validate_inputs.validate_password(input("Enter the passenger password: "))

    if not email or not password:
        print("Invalid credentials")
        return False, None, None, None, None

    cursor = db_client.execute("SELECT * FROM users WHERE email = ?", (email,))
    passenger_data = cursor.fetchone()
    #print(passenger_data)

    if passenger_data:
        passenger = Passenger(
            passenger_data[0],
            passenger_data[1],
            passenger_data[2],
            passenger_data[3],
            passenger_data[4],
            passenger_data[5]
        )
        if passenger.authenticate(password):
            print(f"Passenger {passenger_data[3]} logged in successfully")
            return True, passenger_data[0], passenger_data[1], passenger_data[3], passenger_data[6]
        else:
            print("Invalid credentials")
            return False, None, None, None, None
    else:
        print("No passenger found with that name")
        return False, None, None, None, None

def register_as_passenger(db_client):
    """
    Registers a new passenger user in the system.

    Prompts the user for passenger details, validates inputs, and inserts the data into the database.

    Args:
        db_client: The database client instance.

    Returns:
        None
    """
    ascii_art.ascii_customer_signup()
    name = validate_inputs.validate_non_empty_string(input("Enter the passenger name: "), "Name")
    age = validate_inputs.validate_positive_integer(input("Enter the passenger's age: "), "Age")
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    password = validate_inputs.validate_password(input("Enter the passenger password: "))
    phone_number = validate_inputs.validate_phone_number(input("Enter the passenger phone number: "))

    try:
        db_client.execute("""
            INSERT INTO users (name, age, email, password, phone_number, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, email, password, phone_number, False))
        db_client.commit()
        print(f"Passenger {email} registered successfully")
    except Exception as e:
        db_client.rollback()
        print(f"Error registering passenger: {str(e)}")