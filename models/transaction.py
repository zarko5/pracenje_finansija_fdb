class Transaction:
    # mozda izmenjati kasnije za transaction date da bude zap tip datum
    def __init__(self, transaction_id: int, user_id: int, category_id: int, amount: float ,transaction_type: str, transaction_date: str ,desc: str):
        self.id = transaction_id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.type = transaction_type
        self.date = transaction_date
        self.description = desc
    def __str__(self) -> str:
        return f"Transaction(id={self.id}, user={self.user_id}, category_id={self.category_id}, amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')"

    ### treba nam ovo samo za lepo stampanje kad je lista u pitanju
    def __repr__(self) -> str: 
        return self.__str__()

class TransactionView:
    def __init__(self, transaction: Transaction, username: str, category_name: str):
        self.id = transaction.id
        self.user_id = transaction.user_id
        self.username = username
        self.category_id = transaction.category_id
        self.category_name = category_name
        self.amount = transaction.amount
        self.type = transaction.type
        self.date = transaction.date
        self.description = transaction.description

    def __str__(self) -> str:
        return f"TransactionView(id={self.id}, user={self.user_id}, category_name={self.category_name}, amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')"

    def __repr__(self) -> str: 
        return self.__str__()

    # ## ovo za csv writer
    # def to_dict(self) -> dict:
    #     return {
    #         "id": self.id,
    #         # "user_id": self.user_id, # ovo nam ne treba nuzno, ne vidim sto bi bilo bitno za usera
    #         # alternativa koja mi je ok je da se vidi username
    #         "category_name": self.category_name,
    #         "amount": self.amount,
    #         "type": self.type,
    #         "date": self.date,
    #         "description": self.description,
    #     # }