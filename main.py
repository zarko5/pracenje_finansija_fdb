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




    # category = md.Category(1, "gorivo")
    kat_servis = services.CategoryService(db)
    gorivo_kategorija = kat_servis.add_category("gorivo")
    gorivo_kategorija = kat_servis.get_category("gorivo")
    print(gorivo_kategorija)


    fin_servis = services.FinanceService(db)

    # transakcija da se reworkuje, ili i za kategorije i transakcije i korisnike da se napravi proto
    # bez id-ja koji se passuje funkcijama za create?
    transakcija = md.Transaction(0, korisnik.id, gorivo_kategorija.id, 50,"prihodi","2026-02-03","plata")

    fin_servis.add_transaction(transakcija)

    print(fin_servis.get_user_transactions(korisnik.id))

    print(f"ukupan prihod: {fin_servis.get_total_income(korisnik.id)}")
    print(f"ukupan trosak: {fin_servis.get_total_expenses(korisnik.id)}")
    print(f"ukupan balans: {fin_servis.get_total_balance(korisnik.id)}")

    fin_servis.export_csv(korisnik.id, "test.csv")
    # print(trnlist[0])

    athserv.delete_user(korisnik)


if __name__ == "__main__":
    main()