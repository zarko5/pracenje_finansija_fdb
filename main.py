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
    transakcija = md.Transaction(0, korisnik.id, posao_onetime_kategorija.id, 2550,"prihodi","2026-01-01","izbacivanje suta")
    fin_servis.add_transaction(transakcija)

    transakcija_trosak = md.Transaction(0, korisnik.id, gorivo_kategorija.id, -1230,"trosak","2026-02-03","10l, OMV pumpa")
    fin_servis.add_transaction(transakcija_trosak)

    racun_data = services.PoreskaService.parse_url("https://suf.purs.gov.rs/v/?vl=A0xWVFRLVThFR0VTRTZITzBpBQAAaQUAAGCuCgAAAAAAAAABlDFtugMAAABMShbYnEAdI5sBFyEghf0t0FHscG6bscG6VVc4VD4I9%2B4GXEUvzM9XpCNBMMQQXc7u%2FL568mp%2B2qlCr%2Bk67VoqgjVACQXTbaEONzZmkBhYvYVrDSJRx8lyvlTq6XD7uz4Ly4%2F4E8df8gLj0YiVVEyJ0O%2BTRX96Dd9G%2FD6yQXxdo6thdl1nEfCn0nl7mbDOwfMforKZ75Vc1%2BIljsfekfutqMXKE9%2BF4tiEXEFLqYaZkKqU3DNTtPFAwUMPfjn9%2B4VQfkChak%2FHmOXKlysC3Jabr8iOWsqXod%2FVP85APmzqtivaIP6eoa1DydNl2fYrb6XdBxtVZpVruPL7S8dXphf2qruDsWcxbQc2ddnNrBrJAOZme5t7s5J1cqlLEEhHfVuiVuAkhkJKJBSA3OPRd%2BbpwBjE%2FuCfUJ4diwAujRJEotW2bN%2BkFezsPSxmCwKLHLyQLA%2FG3O22RmAsWdUD5k9nDKpkcj6HLfYf2kJW9lddctVbOPbncxP%2FfzldwP51FHJ5eYyc7MJMAmke8rowg3FHhDmuS%2BX6medpst3X96o39VdLkOTVetRpXGoJnXI%2F%2BrWQtN6cxKBFLUZtMHoAPSVuC7IIWaSDO329V%2FCMJsAkFc6RA%2FnUTRBq3YiNmDIp3x76HyvPUzd1KcGynWUrFkpDPykaeGVtNpn1YMAh9HbAKUumVvQze5pTVxAmOQBDI4s%3D")
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


if __name__ == "__main__":
    main()