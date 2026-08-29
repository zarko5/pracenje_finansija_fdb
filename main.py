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

    ## auth test
    print("auth sa pogresnim kredencijalima", end=": ")
    athserv.authenticate_user("pera_username","netacnaloz")

    print("auth sa tacnim podatcima", end=": ")
    athserv.authenticate_user("pera_username","password")


    kat_servis = services.CategoryService(db)
    gorivo_kategorija = kat_servis.add_category("gorivo")
    posao_onetime_kategorija = kat_servis.add_category("posao onetime")


    fin_servis = services.FinanceService(db)

    # transakcija da se reworkuje, ili i za kategorije i transakcije i korisnike da se napravi proto
    # bez id-ja koji se passuje funkcijama za create?
    transakcija = md.Transaction(0, korisnik.id, posao_onetime_kategorija.id, 2550,"prihodi","2026-02-03","izbacivanje suta")
    fin_servis.add_transaction(transakcija)

    transakcija_trosak = md.Transaction(0, korisnik.id, gorivo_kategorija.id, -1230,"trosak","2026-02-03","10l, OMV pumpa")
    fin_servis.add_transaction(transakcija_trosak)


    print(fin_servis.get_user_transactions(korisnik.id))

    print(f"ukupan prihod: {fin_servis.get_total_income(korisnik.id)}")
    print(f"ukupan trosak: {fin_servis.get_total_expenses(korisnik.id)}")
    print(f"ukupan balans: {fin_servis.get_total_balance(korisnik.id)}")

    fin_servis.export_csv(korisnik.id, "test.csv")


    athserv.delete_user(korisnik) ### na brisanju korisnika se kaskadno brisu i sve transakcije


if __name__ == "__main__":
    main()