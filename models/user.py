class User:
    def __init__(self, user_id: int, username: str, password_hash: str):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    def __str__(self) -> str:
        return f"User(id={self.id}, username='{self.username}')"