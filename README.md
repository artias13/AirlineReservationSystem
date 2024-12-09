# AirLine Reservation System

This is a CLI **AirLine Reservation System** built using Python. It has 3 menus:

## Main Menu:

1. Exit: Exit the program.
2. Login as Admin: Allows admins to log in.
3. Register as Admin: Allows new admins to register.
4. Login as Passenger: Enables passengers to log in.
5. Register as Passenger: Allows new passengers to register.
6. Display User Manual: Displays this user manual.
7. debug_fetch_users_table: Fetches all users.
8. debug_fetch_flights_table: Fetches all flights.
9. debug_fetch_bookings_table: Fetches all bookings.
10. debug_clear_tables: Clears all tables.
    p.s. each time you run program, n new flights are generated and inserted into flights, you can setup it in main.

## Admin Menu:

1. Add new Passenger: Allows admins to add new passengers to the system.
2. Search for Passenger: Enables admins to find passenger details by ID.
3. Update Passenger data: Admins can modify existing passenger information.
4. Delete Passenger: Removes a passenger from the system.
5. Display all registered Passengers: Shows a list of all registered passengers.
6. Display Passengers for all flights or specific flight: View bookings for all flights or a particular flight.
7. Delete Flight: Remove a flight from the system.
8. Logout: Exit the admin menu.

## Passenger Menu:

1. Book Flight: Allows passengers to book flights.
2. Update Personal Data: Allows passengers to update their personal information.
3. Delete account: Removes a passenger's account from the system.
4. Display Flight Schedules: Shows a list of all available flights.
5. Cancel Booking: Cancels a previously booked flight.
6. View My Bookings: Displays a list of bookings made by the passenger.
7. Logout: Exit the passenger menu.

## Setup and Installation

### Prerequisites:

- Python 3.x
- `tabulate` library for displaying data in tables. (This is installed automatically if you use the included `requirements.txt` file.)

### Steps to Set Up:

1. Clone the repository:
   ```bash
   git clone https://github.com/artias13/AirlineReservationSystem.git
   ```
2. Navigate into the project directory:
   ```bash
   cd AirlineReservationSystem
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## File Structure

```bash
AirlineReservationSystem/
│
├── src
├──── admin.py
├──── auth.py
├──── debug.py
├──── models.py
├──── passenger.py
├──── utils
├──────── ascii_art.py
├──────── db_client.py
├──────── flight_generator.py
├──────── user_manual.py
├──────── validate_inputs.py
├── main.py
├── requirements.txt
└── README.md
```

### Notes:

- If you don’t have a `requirements.txt` yet, you can generate it by running:
  ```bash
  pip freeze > requirements.txt
  ```
#   A i r l i n e R e s e r v a t i o n S y s t e m  
 