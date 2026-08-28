from models import Transaction

class FinanceService():
    def __init__(self,db_manager):
        self.db_manager = db_manager

    def add_transaction(self, transaction: Transaction) -> bool:
        try:
            self.db_manager.execute("INSERT INTO transactions (category_id, amount, type, date, description) VALUES (?, ?, ?, ?, ?)", 
                                    (transaction.category_id, transaction.amount, transaction.type, transaction.date, transaction.description))
            return True
        except Exception as e:
            print(f"greska prilikom dodavanja transakcije: {e}")
            return False