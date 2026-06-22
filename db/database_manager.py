import sqlite3

class DatabaseManager:

    def __init__(self, db_path="finance.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def execute(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def initialize_database(self):
        self.execute("""
         CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE)
            """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
            );
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,

            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            transaction_date TEXT NOT NULL,

            description TEXT,

            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
            );
        """)
        