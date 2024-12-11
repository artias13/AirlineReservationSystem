# db_client.py

import sqlite3
from threading import Lock

class DatabaseClient:
    """
    Singleton class for managing database connections.

    Attributes:
        _instance (DatabaseClient): The singleton instance of the class.
        _lock (Lock): Thread lock for ensuring thread-safe instantiation.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """
        Creates a new instance of the DatabaseClient class if none exists.

        Returns:
            DatabaseClient: The singleton instance of the class.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseClient, cls).__new__(cls)
                    cls._instance.connect()
        return cls._instance

    def connect(self):
        """
        Establishes a connection to the SQLite database.

        Creates a connection to the 'airline_reservation.db' file and sets up a cursor.
        """
        self.conn = sqlite3.connect('airline_reservation.db')
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()

    def execute(self, query, params=None):
        """
        Executes an SQL query on the database.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for parameterized queries.

        Returns:
            sqlite3.Cursor: The cursor object after executing the query.
        """
        if params is None:
            return self.cursor.execute(query)
        else:
            return self.cursor.execute(query, params)

    def commit(self):
        """
        Commits the current transaction.
        """
        self.conn.commit()

    def rollback(self):
        """
        Rolls back the current transaction.
        """
        self.conn.rollback()
