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
    # valjalo bi preraditi mozda da athserv uzima user objekat?
    korisnik = athserv.get_user("pera_username")

    print(korisnik)

    athserv.authenticate_user("pera_username","netacnaloz")
    athserv.authenticate_user("pera_username","password")

    athserv.delete_user(korisnik)


if __name__ == "__main__":
    main()