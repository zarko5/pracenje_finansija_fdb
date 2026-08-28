class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name

    def __str__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}')"