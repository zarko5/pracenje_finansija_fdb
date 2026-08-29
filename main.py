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
    # prvo pravimo korisnika
    athserv = services.AuthService(db)
    athserv.register_user("pera_username", "password")

    korisnik = athserv.get_user("pera_username")

#    print(korisnik)

    ## auth test
    print("auth sa pogresnim kredencijalima", end=": ")
    athserv.authenticate_user("pera_username","netacnaloz")

    print("auth sa tacnim podatcima", end=": ")
    athserv.authenticate_user("pera_username","password")

    athserv.delete_user(korisnik)



    # category = md.Category(1, "gorivo")
    kat_servis = services.CategoryService(db)
    gorivo_kategorija = kat_servis.add_category("gorivo")
    gorivo_kategorija = kat_servis.get_category("gorivo")
    print(gorivo_kategorija)


    fin_servis = services.FinanceService(db)
    transakcija = md.Transaction(1,1, 1, 50,"prihodi","2026-02-03","plata")
    # print(transakcija)
    fin_servis.add_transaction(transakcija)


if __name__ == "__main__":
    main()