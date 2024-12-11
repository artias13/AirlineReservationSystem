import random
import datetime
from tabulate import tabulate

class RandomFlightGenerator:
    """
    Class responsible for generating random flight data.

    Attributes:
        id_counter (int): Counter for generating unique IDs.
        DESTINATIONS (list): List of tuples containing destination city names and coordinates.
    """
    def __init__(self):
        self.id_counter = 0
        
    DESTINATIONS = [
        ("Karachi", "24.871940", "66.988060"),
        ("Bangkok", "13.921430", "100.595337"),
        ("Jakarta", "-6.174760", "106.827072"),
        ("Islamabad", "33.607587", "73.100316"),
        ("New York City", "40.642422", "-73.781749"),
        ("Lahore", "31.521139", "74.406519"),
        ("Gilgit Baltistan", "35.919108", "74.332838"),
        ("Jeddah", "21.683647", "39.152862"),
        ("Riyadh", "24.977080", "46.688942"),
        ("New Delhi", "28.555764", "77.096520"),
        # ... Add more destinations as needed
    ]

    def generate_random_id(self):
        """
        Generates a unique ID for flights.

        Increments the internal counter and returns the next ID.

        Returns:
            int: The generated ID.
        """
        self.id_counter += 1
        return self.id_counter
        

    def generate_random_destinations(self):
        """
        Generates random origin and destination cities.

        Selects two different cities from the DESTINATIONS list.

        Returns:
            tuple: Two tuples representing origin and destination cities.
        """
        random_city1 = random.choice(self.DESTINATIONS)
        random_city2 = random.choice(self.DESTINATIONS)
        
        while random_city2 == random_city1:
            random_city2 = random.choice(self.DESTINATIONS)
        
        return random_city1, random_city2

    def generate_random_flight_number(self, length=6):
        """
        Generates a random flight number.

        Creates a flight number consisting of two uppercase letters, a hyphen, and three digits.

        Args:
            length (int): The total length of the flight number (default is 6).

        Returns:
            str: The generated flight number.
        """
        letters = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))
        digits = ''.join(str(i) for i in range(10))
        
        # Limit letters to 2 uppercase letters
        flight_number = ''.join(random.choice(letters) for _ in range(2))
        
        # Add hyphen
        flight_number += '-'
        
        # Add 3 digits
        flight_number += ''.join(random.choice(digits) for _ in range(3))
        
        return flight_number


    def generate_random_flight(self):
        """
        Generates a random flight data entry.

        Creates a comprehensive flight data entry with realistic values.

        Returns:
            list: A list containing flight details.
        """
        city1, lat1, lon1 = random.choice(self.DESTINATIONS)
        city2, lat2, lon2 = random.choice(self.DESTINATIONS)
        
        while (city1, lat1, lon1) == (city2, lat2, lon2):
            city2, lat2, lon2 = random.choice(self.DESTINATIONS)
        
        flight_number = self.generate_random_flight_number()
        seats = random.randint(75, 500)
        
        # Generate realistic flight time
        max_hours = 14
        flight_time = datetime.timedelta(hours=random.randint(1, max_hours))
        
        departure_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        arrival_time = departure_time + flight_time
        
        return [
            #self.generate_random_id(),
            f"{city1} -> {city2}",
            flight_number,
            seats,
            f"{city1}, {lat1}, {lon1}",
            f"{city2}, {lat2}, {lon2}",
            departure_time.strftime("%Y-%m-%d %H:%M:%S"),
            arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
            str(flight_time),
            f"G{random.randint(1, 50)}",
            f"{random.randint(1000, 10000)} km",
            f"As Per Schedule"
        ]

    def generate_flights(self, num_flights):
        """
        Generates multiple random flights.

        Creates a list of random flight entries.

        Args:
            num_flights (int): The number of flights to generate.

        Returns:
            list: A list of random flight entries.
        """
        if num_flights == 0:
            return []
        return [self.generate_random_flight() for _ in range(num_flights)]

    def print_flights(self, flights):
        """
        Prints the given flights in a tabular format.

        Args:
            flights (list): List of flight data entries.

        Returns:
            None
        """
        if not flights:
            print("No flights found.")
            return
        
        # Get the keys from the first dictionary in the list
        headers = ["Flight Schedule", "Flight No.", "Seats", "From", "To", "Departure Time", "Arrival Time", "Flight Time", "Gate", "Distance", "Status"]
        
        print(
            tabulate(
                flights,
                headers=headers,
                tablefmt="grid",
                colalign=("center",) * len(headers),
            )
        )

    def prepare_flight_data(self, flight):
        """
        Prepares flight data for further processing.

        Converts string representations of dates to datetime objects.

        Args:
            flight (list): Flight data entry.

        Returns:
            tuple: Prepared flight data.
        """
        departure_time = datetime.datetime.strptime(flight[5], '%Y-%m-%d %H:%M:%S')
        arrival_time = datetime.datetime.strptime(flight[6], '%Y-%m-%d %H:%M:%S')
        return (
            flight[0],
            flight[1],
            flight[2],
            flight[3],
            flight[4],
            departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            flight[7],
            flight[8],
            flight[9],
            flight[10]
        )
