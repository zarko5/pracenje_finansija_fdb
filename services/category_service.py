from models import Category

class CategoryService():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_category(self, category_name: str) -> bool:
        self.db_manager.execute("INSERT INTO categories VALUES (?)", (category_name,))
        ## treba da se preradi da se proverava da li vec postoji itd
        # i generalno da se naprave ostale operacije, brisanje, izmena, 
        # i da se sve to radi preko get_category, znaci maltene da sve radi kao sto radi u auth.py
        