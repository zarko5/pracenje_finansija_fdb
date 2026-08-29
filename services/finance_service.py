from models import Transaction

class FinanceService():
    def __init__(self,db_manager):
        self.db_manager = db_manager

    # trebalo bi nekoliko izmena ovde, transakcije bi trebalo da se prate po korisniku
    # korisnik takodje treba da bude autentifikovan, 
    # i ili da se validiraju podatci, u smislu klasa itd za kategoreje recimo
    def add_transaction(self, transaction: Transaction) -> bool:
        try:
            self.db_manager.execute("INSERT INTO transactions (category_id, amount, type, date, description) VALUES (?, ?, ?, ?, ?)", 
                                    (transaction.category_id, transaction.amount, transaction.type, transaction.date, transaction.description))
            return True
        except Exception as e:
            print(f"greska prilikom dodavanja transakcije: {e}")
            return False

    ## bilo bi dobro vrv isto kao sto je u auth servisu
    # da imamo svaku operaciju, apdejt, delete, i get
    