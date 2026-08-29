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

    def get_user_transactions(self, user_id: str) -> list[Transaction]:   ## za ovo bi mogli mozda da passujemo usera celog, al mnogo je to importa okolo
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

    def get_total_income(self, user_id: str) -> float:
        transakcije_korisnika = self.get_user_transactions(user_id)
        income = 0
        ### ovo moze sigurno u one lineru da se resi, al ajde, kasnije
        for transakcija in transakcije_korisnika:
            if transakcija.amount > 0: # sve pozitivne kolicine su prihodi
                income += transakcija.amount
        return income
        
    def get_total_expenses(self, user_id: str) -> float:
        transakcije_korisnika = self.get_user_transactions(user_id)
        expenses = 0
        ### ovo moze sigurno u one lineru da se resi, al ajde, kasnije
        for transakcija in transakcije_korisnika:
            if transakcija.amount < 0: # sve pozitivne kolicine su prihodi
                expenses += transakcija.amount
        return expenses

    def get_total_balance(self, user_id: str) -> float:
        return self.get_total_income - self.get_total_expenses


    ## bilo bi dobro vrv isto kao sto je u auth servisu
    # da imamo svaku operaciju, apdejt, delete, i get
