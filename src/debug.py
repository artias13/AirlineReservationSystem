
def debug_aciton(action, db_client):
    """
    Handles debug actions based on the given action string.

    Args:
        action (str): The action to perform (e.g., "fetch_users_table", "fetch_flights_table", etc.)
        db_client: The database client instance.

    Raises:
        ValueError: If an unknown action is provided.

    Returns:
        The result of the performed action (varies depending on the action).
    """
    if action == "fetch_users_table":
        return debug_fetch_users_table(db_client)
    elif action == "fetch_flights_table":
        return debug_fetch_flights_table(db_client)
    elif action == "fetch_bookings_table":
        return debug_fetch_bookings_table(db_client)
    elif action == "clear_tables":
        return debug_clear_tables(db_client)
    else:
        raise ValueError("Unknown action")

def debug_fetch_users_table(db_client):
    """
    Fetches and displays all rows from the 'users' table.

    Args:
        db_client: The database client instance.

    Returns:
        list: All rows from the 'users' table.
    """
    cursor = db_client.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    return result

def debug_fetch_flights_table(db_client):
    """
    Fetches and displays all rows from the 'flights' table.

    Args:
        db_client: The database client instance.

    Returns:
        list: All rows from the 'flights' table.
    """
    cursor = db_client.execute("SELECT * FROM flights")
    result = cursor.fetchall()
    print(result)
    return result

def debug_fetch_bookings_table(db_client):
    """
    Fetches and displays all rows from the 'bookings' table.

    Args:
        db_client: The database client instance.

    Returns:
        list: All rows from the 'bookings' table.
    """
    cursor = db_client.execute("SELECT * FROM bookings")
    result = cursor.fetchall()
    print(result)
    return result

def debug_clear_tables(db_client):
    """
    Clears all data from the 'users', 'flights', and 'bookings' tables.

    Prompts the user for confirmation before performing the operation.

    Args:
        db_client: The database client instance.

    Returns:
        None
    """
    confirmation = input("Are you sure you want to clear all tables? (yes/no): ")
    if confirmation.lower() == "yes":
        try:
            # Delete data from tables
            db_client.execute("DELETE FROM users")
            db_client.execute("DELETE FROM flights")
            db_client.execute("DELETE FROM bookings")
            
            # Reset sequences for auto-incrementing IDs
            db_client.execute("DELETE FROM sqlite_sequence WHERE name='users'")
            db_client.execute("DELETE FROM sqlite_sequence WHERE name='flights'")
            db_client.execute("DELETE FROM sqlite_sequence WHERE name='bookings'")
            
            db_client.commit()
            print("Tables cleared successfully and auto-increment IDs reset.")
        except Exception as e:
            db_client.rollback()
            print(f"Error clearing tables: {str(e)}")
    else:
        print("Table clearing cancelled.")
        return