Sistem za upravljanje ličnim finansijama

### Opis
Aplikacija je izradjena u pythonu, radi praćenja prihoda i troškova.
Podržava više korisnika, sve osnovne operacije, kreiranje, brisanje, izmenu, i prikaz, ali pored toga podržava i automatsko kreiranje transakcije, kroz link od računa poreske uprave. 

Grafički prikaz je realizovan Tkinter'om, podaci se čuvaju u lokalno sqlite bazi, finance.db.

Struktura aplikacije je sledeca
```
.
├── db
│   ├── database_manager.py
│   └── __init__.py
├── db_images
│   ├── b3e5de938fcb493faaf3900928e001ce.png
│   └── c7107aaa8c0f4ea88043749e7ee846dc.png
├── finance.db
├── gui
│   ├── app.py
│   ├── __init__.py
│   ├── izvestaji_screen.py
│   ├── kategorije_screen.py
│   ├── login.py
│   ├── pregled_screen.py
│   ├── theme.py
│   └── transakcije_screen.py
├── main.py
├── models
│   ├── category.py
│   ├── __init__.py
│   ├── transaction.py
│   └── user.py
├── readme.md
├── requirements.txt
├── services
│   ├── auth.py
│   ├── category_service.py
│   ├── finance_service.py
│   ├── __init__.py
│   ├── poreska_service.py
│   └── stats_service.py
└── switch.sh

6 directories, 27 files
```

U `db` folderu se nalazi menadzer baze, koji wrappuje sve osnovne operacije sa bazama, i ukoliko je baza prazna, inicijalizuje tabele korisnika, transakcija, i kategorija.

`db_images` je folder u kome se čuvaju slike za transakcije.

`gui` je paket koji sadrži sve ekrane za aplikaciju

`models` je paket koji sadrži modele, klase za korisnika, transakciju, i kategoriju. postoji i view klasa za transakciju, koja obuhvata više informacija, tjst obuhvata imena kategorija za prikaz, umesto id-jeva

`services` je paket koji sadrži servise koji performiraju sve operacije, npr, AuthService nam služi da kreiramo i menjamo korisnika, FinanceService je za kreiranje i menjanje transakcija, kao i razne statističke operacije nad njima

`main.py` je glavni modul, koji pokrece app. On takođe sadrži funkciju za testiranje modela i servisa, koja testira skoro sve funkcionalnosti koje servisi podržavaju, bez grafike.

### Korišćenje projekta
Prvi korak je kreiranje korisnika, pri pokretanju aplikacije se otvara početni ekran koji sadrži registraciju i login. Prilikom registracije, ukoliko su svi uneseni podaci okej (korisničko ime se ne preklapa sa nekim drugim, i lozinke se poklapaju), aplikacija će iskopirati korisničko ime u login polje. Unosom lozinke i klikom na `Uloguj se` se otvara glavni meni aplikacija.

Glavni ekran ima nekoliko tabova, `Pregled`, `Kategorije`, `Izveštaji`, `Transakcije`

#### Pregled

Podrazumevani tab pri otvaranju je pregled, koji omogućava unošenje nove transakcije, ili manuelno, ili automatski, kroz skener računa.

Za manuelno kreiranje, unosi se datum, bira se kategorija, unosi se iznos, bira se tip, i opcionalno se bira slika koja ce se prikaciti uz transakciju.

Za automatsko unošenje, potrebno je skenirati QR kod sa račuana, koji je u obliku `suf.purs.gov.rs/...` i nalepiti ga u polje za url. Pored toga, bira se kategorija koja će se pripisati ovim transakcijama, i klikom na dodaj sa računa, aplikacija će pokušati da sa poreske dobije sve informacije o računu, i stavkama.
Svaka stavka, se dodaje kao posebna transakcija, automatski se popunjavaju sva ostala polja, i čuva se rekreirana slika računa, nalik onome sa sajta poreske.


#### Kategorije
Na kategorije ekranu, možemo da kreiramo nove kategorije unošenjem naziva u input polje, kao i da editujemo ili brišemo stare kategorije. 

Menjanje kategorija se realizuje kroz isto input polje, potrebno je kliknuti na kategoriju koju korisnik želi da promeni, i zatim u input polje upisati novi naziv, a zatim kliknuti na dugme za izmenu.

Brisanje kategorija se realizuje na sličan način, klikće se na kategoriju, a zatim na brisanje selektovane. 

#### Izveštaji
Na ekranu sa izveštajima se nalaze razni statistički podatci, koji se računaju preko transakcija, aplikacija takođe podržava eksport u Excel ili csv.

#### Transakcije
Ekran transakcije nam omogućava pregled svih transakcija od korisnika, kao i opcije za izmenu i brisanje transakcija.
Takođe, ukoliko postoji slika za transakciju, može se videti selektovanjem i klikom na prikaz slike.


