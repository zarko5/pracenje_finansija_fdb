from argon2 import PasswordHasher
from models import User


ph = PasswordHasher()

class AuthService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # def register_user(self, username, password):
    def register_user(self, username: str, password: str) -> User | None:
        user = self.get_user(username)

        if user is not None:
            print(f"Korisnik {username} vec postoji")
            return None
        
        pass_hash = ph.hash(password)
        try:
            self.db_manager.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pass_hash))
            return self.get_user(username)
        
        except Exception as e:
            print(f"Greška prilikom registracije korisnika: {e}")
            raise ValueError("Greška prilikom registracije korisnika.")


    def get_user(self, username: str) -> User | None:
        user_row = self.db_manager.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

        if user_row is None:
            return None
        
        return User(user_row["id"],user_row["username"],user_row["password_hash"])


    # mozda dodati za ovu metodu da moze da uzima i str pa da pozove samo get_user
    def delete_user(self, user: User) -> bool:
        try:
            self.db_manager.execute("DELETE FROM users WHERE id= ?", (user.id,))
            print(f"korisnik '{user.username}' uspesno obrisan")
            return True
        except Exception as e:
            print (f"Greska pri brisanju korisnika, {e}")
            return False


    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user(username)

        if user is None:
            print(f"korisnik {username} nije pronadjen u bazi")
            return None

        try:
            ph.verify(user.password_hash,password)
            print (f"korisnik {username} uspesno autentifikovan")
            return user
        except Exception as e:
            print("Greska u autentifikaciji")
            return None

