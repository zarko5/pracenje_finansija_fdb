from db.database_manager import DatabaseManager
import models as md
from argon2 import PasswordHasher
# from models import *

def main():
    db = DatabaseManager()
    db.initialize_database()
    print("Baza inicijalizovana")

    # test modela
    category = md.Category(1, "gorivo")
    print(category)

    transakcija = md.Transaction(1, 1, 50,"prihodi","2026-02-03","plata")
    print(transakcija)

    # test user modela
    ph = PasswordHasher()
    user = md.User(1, "miki", ph.hash("password"))   
    print(user)
    print(user.password_hash) 


if __name__ == "__main__":
    main()