from argon2 import PasswordHasher

ph = PasswordHasher()

class AuthService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # def register_user(self, username, password):
    def register_user(self, username, password):
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