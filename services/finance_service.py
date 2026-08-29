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

    def get_transactions(
        self,
        user_id: int | None = None,
        category_id: int | None = None,
        transaction_type: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None
    ) -> list[Transaction] | None:  
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)

        if category_id is not None:
            query += " AND category_id = ?"
            params.append(category_id)

        if transaction_type is not None:
            query += " AND transaction_type = ?"
            params.append(transaction_type)

        if date_from is not None:
            query += " AND transaction_date >= ?"
            params.append(date_from)

        if date_to is not None:
            query += " AND transaction_date <= ?"
            params.append(date_to)

        query += " ORDER BY transaction_date DESC"

        try:
            rows = self.db_manager.fetch_all(query, tuple(params))
            return [
                Transaction(
                    row["id"],
                    row["user_id"],
                    row["category_id"],
                    row["amount"],
                    row["transaction_type"],
                    row["transaction_date"],
                    row["description"]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Greška pri vraćanju transakcija: {e}")
            return None


    def get_user_transactions(self, user_id: str) -> list[Transaction] | None:   ## za ovo bi mogli mozda da passujemo usera celog, al mnogo je to importa okolo
        return self.get_transactions(user_id=user_id)

    def get_user_transactions_by_category(self, user_id: str, category_id: str) -> list[Transaction] | None:
        return self.get_transactions(user_id=user_id, category_id=category_id)

    def get_user_transactions_by_type(self, user_id: str, transaction_type: str) -> list[Transaction] | None:
        return self.get_transactions(user_id=user_id, transaction_type=transaction_type)

    def get_user_transactions_by_date_range(self, user_id: str, date_from: str, date_to: str) -> list[Transaction] | None:
        return self.get_transactions(user_id=user_id, date_from=date_from, date_to=date_to)

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


    def get_expenses_by_category(self, user_id: str) -> dict[str, float]:
        rows = self.db_manager.fetch_all("""
            SELECT c.name AS category_name, SUM(t.amount) AS total_expense
            FROM transactions t
            JOIN categories c ON c.id = t.category_id
            WHERE t.user_id = ? AND t.amount < 0
            GROUP BY c.name
        """, (user_id,))
        ### da su i troskovi i income tu, myb menjati kasnije
        ### WHERE t.user_id = ? ako hocemo i troskove i income, videti


        return {row["category_name"]: row["total_expense"] for row in rows}

    def get_monthly_expenses(self, user_id: str) -> dict[str, float]:
        rows = self.db_manager.fetch_all("""
            SELECT
                strftime('%Y-%m', transaction_date) AS month,
                SUM(amount) AS total_expense
            FROM transactions
            WHERE user_id = ?
            AND amount < 0
            GROUP BY strftime('%Y-%m', transaction_date)
            ORDER BY month DESC
        """, (user_id,))

        return {
            row["month"]: float(row["total_expense"])
            for row in rows
        }


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
        ### zapravo i ovo i funkcija iznad mogu da budu
        ### jedan sql upit
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
