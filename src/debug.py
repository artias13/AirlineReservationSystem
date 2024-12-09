
def debug_aciton(action, db_client):
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
    cursor = db_client.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    return result

def debug_fetch_flights_table(db_client):
    cursor = db_client.execute("SELECT * FROM flights")
    result = cursor.fetchall()
    print(result)
    return result

def debug_fetch_bookings_table(db_client):
    cursor = db_client.execute("SELECT * FROM bookings")
    result = cursor.fetchall()
    print(result)
    return result

def debug_clear_tables(db_client):
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