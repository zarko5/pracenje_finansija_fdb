class User:
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}')"