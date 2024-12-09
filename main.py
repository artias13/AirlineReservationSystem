# main.py

from src.models import Menu, MenuItem, MenuSystem
from src import auth, admin, passenger, debug
from src.utils import user_manual, db_client, flight_generator


class ReservationSystem:
    def __init__(self):
        self.menu_system = MenuSystem()
        self.db_client = db_client.DatabaseClient()
        self.flight_generator = flight_generator.RandomFlightGenerator()

        # generate n flights
        flights = self.flight_generator.generate_flights(5)
        self.flight_generator.print_flights(flights)

        # setup db schema
        self.db_client.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL
            )
        """)

        self.db_client.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_schedule TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                available_seats INTEGER NOT NULL,
                from_location TEXT NOT NULL,
                to_location TEXT NOT NULL,
                departure_time DATETIME NOT NULL,
                arrival_time DATETIME NOT NULL,
                flight_time TEXT NOT NULL,
                gate TEXT NOT NULL,
                distance TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        self.db_client.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                flight_id TEXT NOT NULL,
                tickets INTEGER NOT NULL,
                booking_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (flight_id) REFERENCES flights(id)
            )
        """)
        
        #print(f"PRINTING FLIGHTS: {flights}")
        # update flights table
        if flights != []:
            print(flights)
            print(f"Generating {len(flights)} flights...")
            flight_data = [self.flight_generator.prepare_flight_data(flight) for flight in flights]
            #print(f"PRINTING FLIGHT DATA: {flight_data}")
            print(f"Inserting {len(flights)} flights...")
            for flight_data in flights:
                self.db_client.execute(""" 
                    INSERT INTO flights (flight_schedule, flight_number, available_seats, from_location, to_location, departure_time, arrival_time, flight_time, gate, distance, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, flight_data)

        self.db_client.commit()
        print("Database setup completed.")

        # Set up main menu
        main_menu_items = [
            MenuItem("Exit", lambda x: exit()),
            MenuItem("Login as Admin", lambda x: self.handle_auth_action(self.db_client, "login_as_admin")),
            MenuItem("Register as Admin", lambda x: self.handle_auth_action(self.db_client, "register_as_admin")),
            MenuItem("Login as Passenger", lambda x: self.handle_auth_action(self.db_client, "login_as_passenger")),
            MenuItem("Register as Passenger", lambda x: self.handle_auth_action(self.db_client, "register_as_passenger")),
            MenuItem("Display User Manual", lambda x: user_manual.print_user_manual()),
            MenuItem("(debug) fetch_users_table", lambda x: debug.debug_fetch_users_table(self.db_client)),
            MenuItem("(debug) fetch_flights_table", lambda x: debug.debug_fetch_flights_table(self.db_client)),
            MenuItem("(debug) fetch_bookings_table", lambda x: debug.debug_fetch_bookings_table(self.db_client)),
            MenuItem("(debug) clear_tables", lambda x: debug.debug_clear_tables(self.db_client)),
        ]
        main_menu = Menu("Main Menu", main_menu_items)
        self.menu_system.add_menu('main', main_menu)

        # Set up admin menu
        admin_menu_items = [
            MenuItem("Add new Passenger", lambda x: self.handle_admin_action(self.db_client, "add_new_passenger")),
            MenuItem("Search for Passenger", lambda x: self.handle_admin_action(self.db_client, "search_for_passenger")),
            MenuItem("Update Passenger data", lambda x: self.handle_admin_action(self.db_client, "update_passenger_data")),
            MenuItem("Delete Passenger", lambda x: self.handle_admin_action(self.db_client, "delete_passenger")),
            MenuItem("Display all Passengers", lambda x: self.handle_admin_action(self.db_client, "display_all_passengers")),
            MenuItem("Display all flights registered by a Passenger", lambda x: self.handle_admin_action(self.db_client, "display_all_flights_registered_by_passenger", flight_generator=self.flight_generator)),
            MenuItem("Display all registered passengers in a Flight", lambda x: self.handle_admin_action(self.db_client, "display_registered_passengers_for_flight")),
            MenuItem("Delete Flight", lambda x: self.handle_admin_action(self.db_client, "delete_flight")),
            MenuItem("Back to Main Menu/Logout...", lambda x: self.menu_system.logout()),
        ]
        admin_menu = Menu("Admin Menu", admin_menu_items)
        self.menu_system.add_menu('admin', admin_menu)

        # Set up passenger menu
        passenger_menu_items = [
            MenuItem("Book a flight", lambda x: self.handle_passenger_action(self.db_client, "book_flight", self.flight_generator, self.menu_system)),
            MenuItem("Update personal data", lambda x: self.handle_passenger_action(self.db_client, "update_personal_data", menu_system=self.menu_system)),
            MenuItem("Delete Account", lambda x: self.handle_passenger_action(self.db_client, "delete_account", menu_system=self.menu_system)),
            MenuItem("Display Flight Schedule", lambda x: self.handle_passenger_action(self.db_client, "display_flight_schedule", self.flight_generator)),
            MenuItem("Cancel booking", lambda x: self.handle_passenger_action(self.db_client, "cancel_booking", menu_system=self.menu_system)),
            MenuItem("View my bookings", lambda x: self.handle_passenger_action(self.db_client, "view_my_bookings", menu_system=self.menu_system)),
            MenuItem("Back to Main Menu/Logout...", lambda x: self.menu_system.logout()),
        ]
        passenger_menu = Menu("Passenger Menu", passenger_menu_items)
        self.menu_system.add_menu('passenger', passenger_menu)
        
    def handle_auth_action(self, db_client, action):
        if action == "login_as_admin" or action == "login_as_passenger":
            auth_result, current_user_id, current_user_name, current_user_email, current_user_role = auth.auth_action(action, db_client)
            print(f"auth_result: {auth_result}, current_user_id: {current_user_id}, current_user_name: {current_user_name}, current_user_email: {current_user_email}, current_user_role: {current_user_role}")
            if auth_result:
                self.menu_system.current_user_id = current_user_id
                self.menu_system.current_user_name = current_user_name
                self.menu_system.current_user_role = current_user_role
                self.menu_system.current_user_email = current_user_email
            else:
                print("Login failed")
        else:
            auth.auth_action(action, db_client)

    def handle_passenger_action(self, db_client, action, flight_generator=None, menu_system=None):
        result = passenger.passenger_action(action, db_client, flight_generator, menu_system)
        if result == "deleted":
            self.menu_system.current_menu = 'main'
            self.menu_system.current_user_id = None
            self.menu_system.current_user_name = None
            self.menu_system.current_user_email = None
            self.menu_system.current_user_role = None
        else:
            pass

    def handle_admin_action(self, db_client, action, flight_generator=None, menu_system=None):
        result = admin.admin_action(action, db_client, flight_generator, menu_system)
        if result == "deleted":
            self.menu_system.current_menu = 'main'
            self.menu_system.current_user_id = None
            self.menu_system.current_user_name = None
            self.menu_system.current_user_email = None
            self.menu_system.current_user_role = None
        else:
            pass

    def run(self):
        while True:
            if self.menu_system.current_user_email is None:
                self.menu_system.run_menu('main', self.db_client)
            elif self.menu_system.current_user_role == 1:
                self.menu_system.run_menu('admin', self.db_client)
            else:
                self.menu_system.run_menu('passenger', self.db_client)

# Main execution
if __name__ == "__main__":
    reservation_system = ReservationSystem()
    reservation_system.run()
