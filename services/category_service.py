from models import Category

class CategoryService():
    def __init__(self, db_manager):
        self.db_manager = db_manager

        ## treba da se preradi da se proverava da li vec postoji itd
        # i generalno da se naprave ostale operacije, brisanje, izmena, 
        # i da se sve to radi preko get_category, znaci maltene da sve radi kao sto radi u auth.py    
    def add_category(self, category_name: str) -> Category:
        kategorija_postoji = self.get_category(category_name)
        
        if kategorija_postoji is not None:
            print (f"kategorija sa imenom {category_name} vec postoji u bazi")
            return kategorija_postoji
            # msm da je bolje mozda da returnuje kategoriju koja je, ako i postoji
        
        ## preraditi na try catch 
        self.db_manager.execute("INSERT INTO categories(name) VALUES (?)", (category_name,))
        return self.get_category(category_name)

    def get_category(self, category_name: str) -> Category | None:
        category_row = self.db_manager.fetch_one("SELECT * FROM categories WHERE name = ?", (category_name,))

        if category_row is None:
            return None

        return Category(category_row["id"],category_row["name"])

    def get_category_by_id(self, id: int):
        category_row = self.db_manager.fetch_one("SELECT * FROM categories WHERE id = ?", (id,))
    
        if category_row is None:
            return None

        return Category(category_row["id"],category_row["name"])
    
