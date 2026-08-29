from models import Transaction, TransactionView
import csv
# from .category_service import CategoryService
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

    def get_user_transactions(self, user_id: str) -> list[Transaction] | None:   ## za ovo bi mogli mozda da passujemo usera celog, al mnogo je to importa okolo
        try:
            trans_objects = self.db_manager.fetch_all("SELECT * FROM transactions WHERE user_id = ?",(user_id,))
            lista_transakcija = []
            for obj in trans_objects:
                trn_temp = Transaction(obj["id"],obj["user_id"],obj["category_id"],obj["amount"], obj["transaction_type"],obj["transaction_date"], obj["description"])
                lista_transakcija.append(trn_temp)
            return lista_transakcija

        except Exception as e:
            print(f"greska prilikom trazenja transakcija za korisnika {user_id}")
            return None

    def get_user_transactions_details(self, user_id: str) -> list[TransactionView] | None:
        rows = self.db_manager.fetch_all("""
            SELECT
                t.id,
                t.user_id,
                u.username,
                t.category_id,
                c.name AS category_name,
                t.amount,
                t.transaction_type,
                t.transaction_date,
                t.description
            FROM transactions t
            JOIN users u ON u.id = t.user_id
            JOIN categories c ON c.id = t.category_id
            WHERE t.user_id = ?
        """, (user_id,))

        return [
            TransactionView(
                Transaction(
                    transaction_id=row["id"],
                    user_id=row["user_id"],
                    category_id=row["category_id"],
                    amount=row["amount"],
                    transaction_type=row["transaction_type"],
                    transaction_date=row["transaction_date"],
                    desc=row["description"]
                ),
            row["username"], 
            row["category_name"]
            )
            for row in rows
        ]


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
        return self.get_total_income(user_id) + self.get_total_expenses(user_id)


    def export_csv(self, user_id: str, fname: str) -> bool:
        transakcije_korisnika_details = self.get_user_transactions_details(user_id)
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id", "username", "category_name", "amount",
                    "type", "date", "description"
                ]
            )
            writer.writeheader()
            for item in transakcije_korisnika_details:
                writer.writerow({
                    "id": item.id,
                    "username": item.username,
                    "category_name": item.category_name,
                    "amount": item.amount,
                    "type": item.type,
                    "date": item.date,
                    "description": item.description,
                })
        return True
    ## bilo bi dobro vrv isto kao sto je u auth servisu
    # da imamo svaku operaciju, apdejt, delete, i get
