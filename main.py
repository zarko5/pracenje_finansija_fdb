import sqlite3

from db.database_manager import DatabaseManager

def main():

    # initialize_database()
    db = DatabaseManager()
    conn = db.connect()
    db.initialize_database()
    conn.close()
    print("Application started")

if __name__ == "__main__":
    main()