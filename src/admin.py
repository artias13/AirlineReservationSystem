from src.models import Admin, Passenger
from src.utils import ascii_art, validate_inputs
import logging
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def admin_action(action, db_client, flight_generator, menu_system):
    logging.debug(f"Admin action called with action: {action}")
    
    if action == "add_new_passenger":
        add_new_passenger(db_client)
    elif action == "search_for_passenger":
        search_for_passenger(db_client)
    elif action == "update_passenger_data":
        update_passenger_data(db_client)
    elif action == "delete_passenger":
        delete_passenger(db_client)
    elif action == "display_all_passengers":
        display_all_passengers(db_client)
    elif action == "display_all_flights_registered_by_passenger":
        display_all_flights_registered_by_passenger(db_client, flight_generator)
    elif action == "display_registered_passengers_for_flight":
        display_registered_passengers_for_flight(db_client)
    elif action == "delete_flight":
        delete_flight(db_client)
    else:
        raise ValueError("Unknown action")

def add_new_passenger(db_client):
    ascii_art.ascii_admin_add_new_passenger()

    name = validate_inputs.validate_non_empty_string(input("Enter the passenger name: "), "Name")
    age = validate_inputs.validate_positive_integer(input("Enter the passenger's age: "), "Age")
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    password = validate_inputs.validate_password(input("Enter the passenger password: "))
    phone_number = validate_inputs.validate_phone_number(input("Enter the passenger phone number: "))

    if not password or not phone_number:
        print("Invalid input")
        return

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


def search_for_passenger(db_client):
    ascii_art.ascii_admin_search_for_passenger()
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    cursor = db_client.execute("SELECT * FROM users WHERE email = ?", (email,))
    passenger_data = cursor.fetchone()

    if passenger_data:
        passenger = Passenger(
                passenger_data[0],
                passenger_data[1],
                passenger_data[2],
                passenger_data[3],
                passenger_data[4],
                passenger_data[5]
            ) 
        headers = ["ID", "Name", "Age", "Email", "Phone Number"]
        print(tabulate([
        [passenger.id, passenger.name, passenger.age, passenger.email, passenger.phone_number]
    ], headers=headers, tablefmt="grid", colalign=("center",) * len(headers)))
        
    else:
        print("No passenger found with that email")

def update_passenger_data(db_client):
    ascii_art.ascii_admin_update_passenger_data()
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    cursor = db_client.execute("SELECT * FROM users WHERE email = ?", (email,))
    passenger_data = cursor.fetchone()

    if passenger_data:
        passenger = Passenger(
                passenger_data[0],
                passenger_data[1],
                passenger_data[2],
                passenger_data[3],
                passenger_data[4],
                passenger_data[5]
            ) 
        headers = ["ID","Name", "Age", "Email", "Phone Number"]
        print(tabulate([
        [passenger.id, passenger.name, passenger.age, passenger.email, passenger.phone_number]
    ], headers=headers, tablefmt="grid", colalign=("center",) * len(headers)))

        new_name = validate_inputs.validate_non_empty_string(input("Enter new passenger name: "), "Name")
        new_age = validate_inputs.validate_positive_integer(input("Enter new passenger's age: "), "Age")
        new_email = validate_inputs.validate_email(input("Enter new passenger email: "))
        new_password = validate_inputs.validate_password(input("Enter new passenger password: "))
        new_phone_number = validate_inputs.validate_phone_number(input("Enter new passenger phone number: "))

        if not new_password or not new_phone_number:
            print("Invalid input")
            return

        try:
            db_client.execute("""
                UPDATE users
                SET name = ?, age = ?, email = ?, password = ?, phone_number = ?
                WHERE email = ?
            """, (new_name, new_age, new_email, new_password, new_phone_number, email))

            db_client.commit()
            print("Passenger data updated successfully")
        except Exception as e:
            db_client.rollback()
            print(f"Error updating passenger data: {str(e)}")
    else:
        print("No passenger found with that email")

def delete_passenger(db_client):
    ascii_art.ascii_admin_delete_passenger()
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    cursor = db_client.execute("SELECT * FROM users WHERE email = ?", (email,))
    passenger_data = cursor.fetchone()

    if passenger_data:
        # Create a Passenger object with the fetched data
        passenger = Passenger(
                passenger_data[0],
                passenger_data[1],
                passenger_data[2],
                passenger_data[3],
                passenger_data[4],
                passenger_data[5]
            ) 
        headers = ["ID", "Name", "Age", "Email", "Phone Number"]
        print(tabulate([
        [passenger.id, passenger.name, passenger.age, passenger.email, passenger.phone_number]
    ], headers=headers, tablefmt="grid", colalign=("center",) * len(headers)))

        confirmation = input("Are you sure you want to delete this passenger? (yes/no): ")
        if confirmation.lower() == "yes":
            try:
                db_client.execute("DELETE FROM users WHERE email = ?", (email,))
                db_client.commit()
                print("Passenger deleted successfully")
            except Exception as e:
                db_client.rollback()
                print(f"Error deleting passenger: {str(e)}")
        else:
            print("Passenger deletion cancelled")
    else:
        print("No passenger found with that name")

def display_all_passengers(db_client):
    ascii_art.ascii_admin_display_all_passengers()
    cursor = db_client.execute("SELECT * FROM users WHERE is_admin = 0")
    passengers = cursor.fetchall()

    if passengers:
        passenger_list = [
            Passenger(
                passenger_data[0],
                passenger_data[1],
                passenger_data[2],
                passenger_data[3],
                passenger_data[4],
                passenger_data[5]
            ) for passenger_data in passengers
        ]
        headers = ["ID", "Name", "Age", "Email", "Phone Number"]
        print(tabulate([passenger.to_dict().values() for passenger in passenger_list],
        headers=headers, tablefmt="grid", colalign=("center",) * len(headers)))
    else:
        print("No passengers found")

def display_all_flights_registered_by_passenger(db_client, flight_generator):
    ascii_art.ascii_admin_display_flights_by_passenger()
    
    email = validate_inputs.validate_email(input("Enter the passenger email: "))
    cursor = db_client.execute("SELECT * FROM users WHERE email = ?", (email,))
    passenger_data = cursor.fetchone()

    if passenger_data:
        passenger = Passenger(
                passenger_data[0],
                passenger_data[1],
                passenger_data[2],
                passenger_data[3],
                passenger_data[4],
                passenger_data[5]
            ) 

        # search for flights
        flights = db_client.execute("SELECT * FROM flights WHERE id IN (SELECT flight_id FROM bookings WHERE user_id = ?)", (passenger.id,)).fetchall()
        print(f"Flights registered by {passenger.name}:")
        flight_generator.print_flights(flights)

    else:
        print("No passenger found with that email")

def display_registered_passengers_for_flight(db_client):
    ascii_art.ascii_admin_display_registered_passengers_for_flight()
    
    flight_number = validate_inputs.validate_non_empty_string(input("Enter the flight number: "), "Flight Number")
    
    cursor = db_client.execute(
        """
        SELECT users.*, bookings.*
        FROM flights
        INNER JOIN bookings ON flights.id = bookings.flight_id
        INNER JOIN users ON bookings.user_id = users.id
        WHERE flights.flight_number = ?
        """,
        (flight_number,)
    )
    
    passengers = cursor.fetchall()
    
    if passengers:
        print(f"Registered passengers for Flight {flight_number}:")
        
        first_5_elements = []
        
        for passenger in passengers:
            first_5 = [passenger[i] for i in range(6)] 
            first_5_elements.append(first_5)
        
        headers = ["ID", "Name", "Age", "Email", "Password", "Phone Number"]
        print(tabulate(first_5_elements, headers=headers, tablefmt="grid"))
        
    else:
        print(f"No registered passengers found for Flight {flight_number}")

def delete_flight(db_client):
    ascii_art.ascii_admin_delete_flight()
    
    flight_number = validate_inputs.validate_non_empty_string(input("Enter the flight number: "), "Flight Number")
    
    try:
        db_client.execute("DELETE FROM flights WHERE flight_number = ?", (flight_number,))
        db_client.commit()
        print(f"Flight {flight_number} deleted successfully")
    except Exception as e:
        db_client.rollback()
        print(f"Error deleting flight: {str(e)}")
