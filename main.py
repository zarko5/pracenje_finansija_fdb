from db.database_manager import DatabaseManager
import models as md
import services
# from models import *

def main():
    db = DatabaseManager()
    db.initialize_database()
    print("Baza inicijalizovana")
    test_models(db)



def test_models(db):
    # test modela
    category = md.Category(1, "gorivo")
    print(category)

    transakcija = md.Transaction(1, 1, 50,"prihodi","2026-02-03","plata")
    print(transakcija)

    athserv = services.AuthService(db)
    athserv.register_user("pera_username", "password")
    korisnik = md.User(1,"pera_username","passtest")
    print(korisnik)



if __name__ == "__main__":
    main()