# db_client.py

import sqlite3
from threading import Lock

class DatabaseClient:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseClient, cls).__new__(cls)
                    cls._instance.connect()
        return cls._instance

    def connect(self):
        self.conn = sqlite3.connect('airline_reservation.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, query, params=None):
        if params is None:
            return self.cursor.execute(query)
        else:
            return self.cursor.execute(query, params)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
