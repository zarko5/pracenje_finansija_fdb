from db.database_manager import DatabaseManager

def main():
    db = DatabaseManager()
    db.initialize_database()
    print("Baza inicijalizovana.")
    print("Application started")

if __name__ == "__main__":
    main()