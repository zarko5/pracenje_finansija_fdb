from models import Transaction

class FinanceService():
    def __init__(self,db_manager):
        self.db_manager = db_manager

    # korisnik takodje treba da bude autentifikovan
    # i ili da se validiraju podatci, u smislu klasa itd za kategoreje recimo
    def add_transaction(self, transaction: Transaction) -> bool:
        try:
            self.db_manager.execute("INSERT INTO transactions (user_id, category_id, amount, transaction_type, transaction_date, description) VALUES (?, ?, ?, ?, ?, ?)", 
                                    (transaction.user_id,transaction.category_id, transaction.amount, transaction.type, transaction.date, transaction.description))
            print (f"transakcija uspesno dodata")
            return True
        except Exception as e:
            print(f"greska prilikom dodavanja transakcije: {e}")
            return False

    def get_user_transactions(self, user_id: str):   ## za ovo bi mogli mozda da passujemo usera celog, al mnogo je to importa okolo
        try:
            trans_objects = self.db_manager.fetch_all("SELECT * FROM transactions WHERE user_id = ?",(user_id,))
            lista_transakcija = []
            for obj in trans_objects:
                trn_temp = Transaction(obj["id"],obj["user_id"],obj["category_id"],obj["amount"], obj["transaction_type"],obj["transaction_date"], obj["description"])
                lista_transakcija.append(trn_temp)
            return lista_transakcija

        except Exception as e:
            print(f"greska prilikom trazenja transakcija za korisnika {user_id}")
            return False



    ## bilo bi dobro vrv isto kao sto je u auth servisu
    # da imamo svaku operaciju, apdejt, delete, i get
