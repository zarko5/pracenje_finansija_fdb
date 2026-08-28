class Transaction:
    # mozda izmenjati kasnije za transaction date da bude zap tip datum
    def __init__(self, transaction_id: int, category_id: int, amount: float ,transaction_type: str, transaction_date: str ,desc: str):
        self.id = transaction_id
        self.category_id = category_id
        self.amount = amount
        self.type = transaction_type
        self.date = transaction_date
        self.description = desc
    def __str__(self) -> str:
        return f"Transaction(id={self.id}, category_id={self.category_id}, amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')"