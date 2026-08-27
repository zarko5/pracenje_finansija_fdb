from db.database_manager import DatabaseManager
import models as md

# from models import *

def main():
    db = DatabaseManager()
    db.initialize_database()
    print("Baza inicijalizovana")
    test_models()



def test_models():
    # test modela
    category = md.Category(1, "gorivo")
    print(category)

    transakcija = md.Transaction(1, 1, 50,"prihodi","2026-02-03","plata")
    print(transakcija)



if __name__ == "__main__":
    main()