from argon2 import PasswordHasher
from models import User


ph = PasswordHasher()

class AuthService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # def register_user(self, username, password):
    def register_user(self, username: str, password: str) -> bool:
        user_exists = self.db_manager.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if user_exists:
            raise ValueError("Korisničko ime već postoji.")
            # return False
        pass_hash = ph.hash(password)
        try:
            self.db_manager.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pass_hash))
        except Exception as e:
            print(f"Greška prilikom registracije korisnika: {e}")
            raise ValueError("Greška prilikom registracije korisnika.")
        return True

    def delete_user(self, username: str) -> bool:
        user_exists = self.db_manager.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if user_exists:
            self.db_manager.execute("DELETE FROM users WHERE username = ?", (username,))
            return True
        raise ValueError("Korisnik ne postoji.")

    def authenticate_user(self, username: str, password: str) -> bool:
        user_row = self.db_manager.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if user_row is None:
            return None

        try:
            ph.verify(user_row["password_hash"],password)
            return User(user_row["id"],user_row["username"],user_row["password_hash"])
        except Exception as e:
            print("Greska u autentifikaciji")
            return None

