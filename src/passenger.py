from src.models import Admin, Passenger
from src.utils import ascii_art, validate_inputs
import logging
import datetime
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def passenger_action(action, db_client, flight_generator, menu_system):
    """
    Handles passenger actions based on the given action string.

    Args:
        action (str): The action to perform (e.g., "book_flight", "update_personal_data", etc.)
        db_client: The database client instance.
        flight_generator: An instance of the flight generator class.
        menu_system: The current menu system instance.

    Raises:
        ValueError: If an unknown action is provided.

    Returns:
        str: "deleted" if the delete_account action is performed successfully, otherwise None.
    """
    logging.debug(f"Passenger action called with action: {action}")

    if action == "book_flight":
        book_flight(db_client, flight_generator, menu_system)
    elif action == "update_personal_data":
        update_personal_data(db_client, menu_system)
    elif action == "delete_account":
        return delete_account(db_client, menu_system)
    elif action == "display_flight_schedule":
        display_flight_schedule(db_client, flight_generator)
    elif action == "cancel_booking":
        cancel_booking(db_client, menu_system)
    elif action == "view_my_bookings":
        view_my_bookings(db_client, menu_system)
    else:
        raise ValueError("Unknown action")


def book_flight(db_client, flight_generator, menu_system):
    """
    Books a flight for the current passenger.

    Args:
        db_client: The database client instance.
        flight_generator: An instance of the flight generator class.
        menu_system: The current menu system instance.

    Returns:
        None
    """
    ascii_art.ascii_customer_book_flight()
    
    try:
        # fetch all flights and print them
        flights = db_client.execute("SELECT * FROM flights").fetchall()
        flight_generator.print_flights(flights)
        flight_no = validate_inputs.validate_non_empty_string(input("Enter the flight number: "), "Flight Number")
        tickets_required = validate_inputs.validate_positive_integer(input("Enter the number of tickets required: "), "Number of tickets")

        # check if the flight exists
        flight = db_client.execute("SELECT * FROM flights WHERE flight_number = ?", (flight_no,)).fetchone()
        if flight is None:
            print("Flight not found.")
            return

        # check if there are enough seats available
        available_seats = flight[3]
        if tickets_required > available_seats:
            print("Not enough seats available.")
            return

        # book the flight
        db_client.execute("UPDATE flights SET available_seats = available_seats - ? WHERE flight_number = ?", (tickets_required, flight_no))

        # get the flight id by flight number
        flight_id = db_client.execute("SELECT id FROM flights WHERE flight_number = ?", (flight_no,)).fetchone()[0]

        # add the booking to the database
        db_client.execute("INSERT INTO bookings (user_id, flight_id, tickets, booking_date) VALUES (?, ?, ?, ?)", (menu_system.current_user_id, flight_id, tickets_required, datetime.date.today().isoformat()))
       
        db_client.commit()
        print(f"Successfully booked {tickets_required} seat(s) on flight {flight_no}.")
    except Exception as e:
        db_client.rollback()
        print(f"Error booking flight: {str(e)}")


def update_personal_data(db_client, menu_system):
    """
    Updates the personal data of the current passenger.

    Args:
        db_client: The database client instance.
        menu_system: The current menu system instance.

    Returns:
        None
    """
    ascii_art.ascii_customer_edit_info()
    name = validate_inputs.validate_non_empty_string(input("Enter new passenger name: "), "Name")
    age = validate_inputs.validate_positive_integer(input("Enter the passenger's age: "), "Age")
    email = validate_inputs.validate_email(input("Enter new passenger email: "))
    phone_number = validate_inputs.validate_phone_number(input("Enter the passenger phone number: "))

    try:
        db_client.execute("UPDATE users SET name = ?, age = ?, email = ?, phone_number = ? WHERE id = ?", (name, age, email, phone_number, menu_system.current_user_id))
        db_client.commit()
        print("Personal data updated successfully.")
    except Exception as e:
        db_client.rollback()
        print(f"Error updating personal data: {str(e)}")

def delete_account(db_client, menu_system):
    """
    Deletes the account of the current passenger after confirmation.

    Args:
        db_client: The database client instance.
        menu_system: The current menu system instance.

    Returns:
        str: "deleted" if the account was deleted successfully, otherwise None.
    """
    ascii_art.ascii_customer_delete_account()

    confirmation = input("Are you sure you want to delete your account? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Account deletion cancelled.")
        return

    try:
        db_client.execute("DELETE FROM users WHERE id = ?", (menu_system.current_user_id,))
        db_client.commit()
        print("Account deleted successfully.")
        return "deleted"
    except Exception as e:
        db_client.rollback()
        print(f"Error deleting account: {str(e)}")

def display_flight_schedule(db_client, flight_generator):
    """
    Displays the flight schedule for the passenger.

    Args:
        db_client: The database client instance.
        flight_generator: An instance of the flight generator class.

    Returns:
        None
    """
    ascii_art.ascii_customer_flight_schedule()
    try:
        # fetch all flights and print them
        flights = db_client.execute("SELECT * FROM flights").fetchall()
        flight_generator.print_flights(flights)

    except Exception as e:

        print(f"Error displaying flight schedule: {str(e)}")


def cancel_booking(db_client, menu_system):
    """
    Cancels a booking made by the current passenger.

    Args:
        db_client: The database client instance.
        menu_system: The current menu system instance.

    Returns:
        None
    """
    ascii_art.ascii_customer_cancel_flight()
    
    try:
        # Fetch all bookings for the current user
        bookings = db_client.execute("""
            SELECT 
                b.id AS BookingID,
                b.booking_date AS BookingDate,
                f.flight_number AS FlightNumber,
                b.tickets AS BookedTickets,
                f.from_location AS FromLocation,
                f.to_location AS ToLocation,
                f.departure_time AS DepartureTime,
                f.arrival_time AS ArrivalTime,
                f.flight_time AS FlightTime,
                f.gate AS Gate,
                f.status AS Status
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.user_id = ?
        """, (menu_system.current_user_id,)).fetchall()

        # Print the bookings using tabulate
        headers = ["ID", "BookingDate", "FlightNumber", "BookedTickets", "FromLocation", "ToLocation", 
                   "DepartureTime", "ArrivalTime", "FlightTime", "Gate", "Status"]
        
        print(tabulate(bookings, headers=headers, tablefmt="grid"))

        flight_number = validate_inputs.validate_non_empty_string(input("Enter the flight number to cancel booking: "), "Flight Number")

        # check if the flight exists
        flight = db_client.execute("SELECT * FROM flights WHERE flight_number = ?", (flight_number,)).fetchone()
        if flight is None:
            print("Flight not found.")
            return

        # check if the booking exists
        booking = db_client.execute("SELECT * FROM bookings WHERE flight_id = ? AND user_id = ?", (flight[0], menu_system.current_user_id)).fetchone()
        if booking is None:
            print("Booking not found.")
            return

        # cancel the booking and update the flight availability
        db_client.execute("UPDATE flights SET available_seats = available_seats + ? WHERE id = ?", (booking[3], flight[0]))
        db_client.execute("DELETE FROM bookings WHERE id = ?", (booking[0],))
        db_client.commit()
        print("Booking canceled successfully.")


    except Exception as e:
        db_client.rollback()
        print(f"Error canceling booking: {str(e)}")

def view_my_bookings(db_client, menu_system):
    """
    Displays all bookings made by the current passenger.

    Args:
        db_client: The database client instance.
        menu_system: The current menu system instance.

    Returns:
        None
    """
    ascii_art.ascii_customer_registered_flights()

    try:
        # Fetch all bookings for the current user
        bookings = db_client.execute("""
            SELECT 
                b.id AS BookingID,
                b.booking_date AS BookingDate,
                f.flight_number AS FlightNumber,
                b.tickets AS BookedTickets,
                f.from_location AS FromLocation,
                f.to_location AS ToLocation,
                f.departure_time AS DepartureTime,
                f.arrival_time AS ArrivalTime,
                f.flight_time AS FlightTime,
                f.gate AS Gate,
                f.status AS Status
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.user_id = ?
        """, (menu_system.current_user_id,)).fetchall()

        # Print the bookings using tabulate
        headers = ["ID", "BookingDate", "FlightNumber", "BookedTickets", "FromLocation", "ToLocation", 
                   "DepartureTime", "ArrivalTime", "FlightTime", "Gate", "Status"]
        
        print(tabulate(bookings, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Error fetching bookings: {str(e)}")
