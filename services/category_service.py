from models import Category

class CategoryService():
    def __init__(self, db_manager):
        self.db_manager = db_manager

        # Preradjeno da proverava na svim da li postoji, i na update dodana zastita da nema duplikat
        ## ubacena sve komande za kategorije
        ### i da se sve to radi preko get_category, znaci maltene da sve radi kao sto radi u auth.py -
    def add_category(self, category_name: str) -> Category:
        kategorija_postoji = self.get_category(category_name)

        if kategorija_postoji is not None:
            print (f"kategorija sa imenom {category_name} vec postoji u bazi")
            return kategorija_postoji
            # msm da je bolje mozda da returnuje kategoriju koja je, ako i postoji

        ## preuredjeno u try
        try:
            self.db_manager.execute("INSERT INTO categories(name) VALUES (?)", (category_name,))
            print(f"Kategorija {category_name} je uspesno kreirana.")
            return self.get_category(category_name)

        except Exception as e:
            print(f"Greska prilikom kreiranja kategorije {e}")
            return False

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

    def update_category(self, category_id: int, new_name: str, ) -> bool:
        kategorija_postoji = self.get_category_by_id(category_id)

        if kategorija_postoji is None:
            print(f"Kategorija {category_id} ne postoji, izmena nije moguca.")
            return False

        # ovde je samo dodatna provrea da ukoliko ime vec postoji ne moye da se izmeni u isto
        ime_vec_postoji = self.get_category(new_name)

        if ime_vec_postoji is not None and ime_vec_postoji.id != category_id:
            print(f"Kategorija '{new_name}' vec postoji, nije moguce izmeniti")
            return False

        try:
            self.db_manager.execute("UPDATE categories SET name = ? WHERE id = ?" ,(new_name, category_id))
            print(f"Kategorija {kategorija_postoji.name} je uspesno izmenjena u {new_name}")
            return True

        except Exception as e:
            print (f"Greska prilikom azuriranja kategorije {e}")
            return False

    def delete_category(self, category_name: str) -> bool:
        kategorija_postoji = self.get_category(category_name)

        if kategorija_postoji is None:
            print(f"Kategorija sa imenom {category_name} ne postoji, brisanje nije moguce.")
            return False

        try:
            self.db_manager.execute("DELETE FROM categories WHERE id = ?",(kategorija_postoji.id,))
            print(f"Kategorija {category_name} je uspesno obrisna.")
            return True

        except Exception as e:
            print(f"Greska prilkom brisanja kategorije {e}")
            return False
