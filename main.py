from db.database_manager import DatabaseManager
import models as md
import services
from gui import App
# from models import *

def main():
    db = DatabaseManager()
    db.initialize_database()
    print("Baza inicijalizovana")
    # test_models(db)

    ### pokretanje grafike
    app = App(db)
    
    app.mainloop()



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
    transakcija = md.Transaction(0, korisnik.id, posao_onetime_kategorija.id, 2550,"prihodi","2026-01-01","izbacivanje suta")
    fin_servis.add_transaction(transakcija)

    transakcija_trosak = md.Transaction(0, korisnik.id, gorivo_kategorija.id, -1230,"trosak","2026-02-03","10l, OMV pumpa")
    fin_servis.add_transaction(transakcija_trosak)



    racun_data = services.PoreskaService.parse_url_json("https://suf.purs.gov.rs/v/?vl=AzlWSFJaQkpaOVZIUlpCSlpJSAAABUEAABAD7gMAAAAAAAABn0dL8LgAAAB9wLARVkKyDFEukV87w/4NKfxq527cOAJCJTFVPK756EoTqmFZmom/zMxRkrU6lSpjV8GCF378lVv8+kPNEm3sEN3TDd9WcOXQJ77KadUYQcI0LrEtuYyLhg0pJU1AUT6E5Un2wiSDZT8FqHHoj2n1vrznDYZfFcw8xS3vk4RKycYFgnIN1a35gzFs3jVM8OQURabt5cpkQ65IH4NZ8QQcQujMxM85tI3izId3Bw3xGxP/beyIiLgXacxuNz/Swk/Ft/twEIwHDjJnWiU1dOYLogm3AdKTdnQ3aL3OCOg1H87x1etTofk240rmKbsVR6PiGAZQvy0yV72FQG2OUASrG40hM8YXWwvlZ83CQ4CYaVNFQfIqNSsq3SaxPxmNwRyUKGoBbtZVjc+6bH7cjCXxFCa8x0YJBV4HzoSkoX7if8Sm2z+wJHHl2tzjoLm2Lr2dLvMfMYbJlsO82PzTlBTvG8QpEklgSpYRamCTtNKNATLNLgZ3fNmFa5BHOFuk2U5bk+QAd0oUlk6dbmHlZ9156/NKOiga31k5w5CnJOTNK+ZeCYgXvG0Vb7An65GEaoAX+JIzUb2YQEjK5Mqlidbfw9gu4mBxZRPoa5wEQ3UhO5kaSlVYPC9rwm8r6vFYo/ak92FexZgw2ljY3YBVyD1Kg8OmiMSnHAaFlWIJTuH3a8fwvSyUgcBV/NpgKFX6kaw=")
    print(racun_data)
    transakcije = services.PoreskaService.parse_invoice_data(racun_data, korisnik.id, gorivo_kategorija.id)

    for transakcija in transakcije:
        fin_servis.add_transaction(transakcija)

    print(fin_servis.get_user_transactions(korisnik.id))

    print(f"ukupan prihod: {fin_servis.get_total_income(korisnik.id)}")
    print(f"ukupan trosak: {fin_servis.get_total_expenses(korisnik.id)}")
    print(f"ukupan balans: {fin_servis.get_total_balance(korisnik.id)}")

    fin_servis.export_csv(korisnik.id, "test.csv")


    print(fin_servis.get_user_transactions_by_category(korisnik.id, posao_onetime_kategorija.id))   
    print(fin_servis.get_user_transactions_by_date_range(korisnik.id, "2026-02-01", "2026-02-04"))

    print(f"ukupni troskovi po kategorijama: {fin_servis.get_expenses_by_category(korisnik.id)}")

    print(f"ukupni mesecni troskovi {fin_servis.get_monthly_expenses(korisnik.id)}")
    athserv.delete_user(korisnik) ### na brisanju korisnika se kaskadno brisu i sve transakcije
    kat_servis.delete_category(gorivo_kategorija.name)
    kat_servis.update_category(posao_onetime_kategorija.id, "specijalni poslovi dragan")
    kat_servis.delete_category(posao_onetime_kategorija.name)

if __name__ == "__main__":
    main()