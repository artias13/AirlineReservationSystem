# auth.py

from src.models import Admin, Passenger
from src.utils import ascii_art, validate_inputs

def auth_action(action, db_client):
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
    ascii_art.ascii_admin_login()
    name = input("Enter admin name: ")
    password = input("Enter admin password: ")

    if not name or not password:
        print("Invalid credentials")
        return False, None, None, None, None

    cursor = db_client.execute("SELECT * FROM users WHERE name = ? AND is_admin = 1", (name,))
    admin_data = cursor.fetchone()

    if admin_data:
        # Assuming the order is: id, name, age, email, password, phone_number, is_admin
        admin = Admin(admin_data[1], admin_data[4])  # Using name and password from DB
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
        print("Admin registered successfully")
    except Exception as e:
        db_client.rollback()
        print(f"Error registering admin: {str(e)}")

def login_as_passenger(db_client):
    ascii_art.ascii_customer_login()
    name = input("Enter passenger name: ")
    password = input("Enter passenger password: ")

    if not name or not password:
        print("Invalid credentials")
        return False, None, None, None, None

    cursor = db_client.execute("SELECT * FROM users WHERE name = ?", (name,))
    passenger_data = cursor.fetchone()
    print(passenger_data)

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
            print("Passenger logged in successfully")
            return True, passenger_data[0], passenger_data[1], passenger_data[3], passenger_data[6]
        else:
            print("Invalid credentials")
            return False, None, None, None, None
    else:
        print("No passenger found with that name")
        return False, None, None, None, None

def register_as_passenger(db_client):
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
        print("Passenger registered successfully")
    except Exception as e:
        db_client.rollback()
        print(f"Error registering passenger: {str(e)}")