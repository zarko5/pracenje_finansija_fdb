class Transaction:
    def __init__(self, transaction_id, category_id, amount ,transaction_type, transaction_date,desc):
        self.id = transaction_id
        self.category_id = category_id
        self.amount = amount
        self.type = transaction_type
        self.date = transaction_date
        self.description = desc
    def __str__(self):
        return f"Transaction(id={self.id}, category_id={self.category_id}, amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')"