from models import Transaction, TransactionView
import requests
from datetime import datetime

class PoreskaService:
    def __init__(self):
        pass

    def parse_url(url):
        headers = {"Accept": "application/json"}

        try:
            resp = requests.get(url,headers=headers, timeout=10)
            resp.raise_for_status()
    
            data = resp.json()
            # print(data)
            return data

        except requests.exceptions.RequestException as e:
            print(f"greska pri zahtevu poreskoj: {e}")

    def parse_invoice_data(invoice_data, user_id: int, category_id: int) -> list[Transaction] | None:
        if "invoiceRequest" not in invoice_data:
            print("los odgovor od poreske")
            return None

        invoice_request = invoice_data["invoiceRequest"]
        invoice_result = invoice_data["invoiceResult"]

        if "items" not in invoice_request:
            print("nema stavki na racunu")
            return None

        items = invoice_request["items"]
        transactions = []

        datum = datetime.strptime(invoice_result.get("sdcTime"), "%Y-%m-%dT%H:%M:%S.%fZ")
        ### transakcija za svaki artikal na racunu, nije idealno
        ### ali moze biti korisnije za svrstavanje po kategorijama kasnije
        for item in items:
            name = item.get("name")
            quantity = item.get("quantity", 0)
            unit_price = item.get("unitPrice", 0.0)
            total_price = item.get("totalPrice", 0.0)

            transaction = Transaction(
                transaction_id=0,
                user_id=user_id, 
                category_id=category_id, 
                amount=total_price,
                transaction_type="trosak",
                transaction_date=datum.strftime("%Y-%m-%d"),
                desc=f"{name} - {quantity} x {unit_price}"
            )
            transactions.append(transaction)

        return transactions
    

### neki testni linkovi
### https://suf.purs.gov.rs/v/?vl=A0xWVFRLVThFR0VTRTZITzBpBQAAaQUAAGCuCgAAAAAAAAABlDFtugMAAABMShbYnEAdI5sBFyEghf0t0FHscG6bscG6VVc4VD4I9%2B4GXEUvzM9XpCNBMMQQXc7u%2FL568mp%2B2qlCr%2Bk67VoqgjVACQXTbaEONzZmkBhYvYVrDSJRx8lyvlTq6XD7uz4Ly4%2F4E8df8gLj0YiVVEyJ0O%2BTRX96Dd9G%2FD6yQXxdo6thdl1nEfCn0nl7mbDOwfMforKZ75Vc1%2BIljsfekfutqMXKE9%2BF4tiEXEFLqYaZkKqU3DNTtPFAwUMPfjn9%2B4VQfkChak%2FHmOXKlysC3Jabr8iOWsqXod%2FVP85APmzqtivaIP6eoa1DydNl2fYrb6XdBxtVZpVruPL7S8dXphf2qruDsWcxbQc2ddnNrBrJAOZme5t7s5J1cqlLEEhHfVuiVuAkhkJKJBSA3OPRd%2BbpwBjE%2FuCfUJ4diwAujRJEotW2bN%2BkFezsPSxmCwKLHLyQLA%2FG3O22RmAsWdUD5k9nDKpkcj6HLfYf2kJW9lddctVbOPbncxP%2FfzldwP51FHJ5eYyc7MJMAmke8rowg3FHhDmuS%2BX6medpst3X96o39VdLkOTVetRpXGoJnXI%2F%2BrWQtN6cxKBFLUZtMHoAPSVuC7IIWaSDO329V%2FCMJsAkFc6RA%2FnUTRBq3YiNmDIp3x76HyvPUzd1KcGynWUrFkpDPykaeGVtNpn1YMAh9HbAKUumVvQze5pTVxAmOQBDI4s%3D
### https://suf.purs.gov.rs/v/?vl=A0pQTkUyTkYzSlBORTJORjPOUwMA300DAKzqnwAAAAAAAAABnsJC9sgAAAA6Hf6KKiRexVSe3U4nexvBLocBq6uZIc2LK0dvWHV5iw2t2Z4YRqqdL47+milYUiNydjMIsZ2Qfe3IGYTbVyObQGAuxzRxxM7Dh1harJd0T3kdGRQhz2O0upWaCEDqas+fK2cX1SNEHA7dN64be9wXH8/wtnUsq1xl8QVY1XSlI1OUklQfFePt+PE8JZrfSzP/UxGscqOVbpfQ2OvFWjc6m6nbK7Hufz7BugauyqycJ0coAtkFn945MeUEXpq8GzEvLGgfDzi9AU4+x8c9hqfHNWEaP/sT5TD2ZFT1igEqHsm2WPuZ1kJOk5vuqolw4bKiMhubrIFT1TA7OquTUOkjg6kx5v7wdQ4rVVD0rktRnnfNwIl2ltqlsHmImnjAbET3yvF8op6Ds6gu+vX7s7AcAuuTz9RSYU8epC0PP/tfeS/+y5KmQsJ7kvhJOXRxspcpkX4Z8SODehXo4ky1yJuvUqIulCRr7xLhVbH2cdgqlN9eS9Hvf0ox/hFZKEXGe1WMF5B4rhQ1D+sPons5NVxOmbei36J48LoJGUgMk/CHBeR83MuSeIuq2W9fFfJb4Gu26YEILQyv0jyyQYXpRY8qzqucITlJot06ObLJlo2/oY70Wvm7QXy+XY6O2vG+GGq+8Hn47jJPSq0DIhMTRX+iqy6ayzrpIGZlGjDMPk4Cnj7b7aQwu/0iQbKiVjC5ZPs=

# ovo je link od poreske gde je opisano funkcionisanje sistema, moze da se radi i scrape njihove stranice 
# ako treba na primer da se dobije i EAN (barkod ugl), od svakog proizvoda, ali za ovu app bih rekao da je dovoljno
# https://tap.suf.purs.gov.rs/help/view/1307279411/%D0%A1%D0%BA%D0%B5%D0%BD%D0%B8%D1%80%D0%B0%D1%9A%D0%B5-%D1%80%D0%B0%D1%87%D1%83%D0%BD%D0%B0-%D1%81%D0%B0-JSON-%D0%BE%D0%B4%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%D0%BE%D0%BC/sr-Cyrl-RS

## u samom odgovoru ovom ima bas puno informacija
## mozemo u sustini da imamo apstrakciju na artikal bazirane troskove 

### -- ok poreska je ipak zeznula stvari, tjst izbacili su items, ne vidi
### se u odgovoru ali im stoji u specifikaciji, svakako, idemo dalje na scrape metodu


### primer responsa
# {
#     "invoiceRequest": {
#         "posTime": null,
#         "taxId": "240799085",
#         "businessName": "Knjige",
#         "locationName": "1155567-Knjiga 1",
#         "address": "Prvomajska 13",
#         "city": "БЕОГРАД",
#         "administrativeUnit": "Београд-Нови Београд",
#         "buyer": null,
#         "buyerCostCenter": null,
#         "cashier": null,
#         "requestedBy": "5BX9A4MP",
#         "referentDocumentNumber": null,
#         "invoiceType": 0,
#         "transactionType": 0,
#         "payments": [
#             {
#                 "paymentType": 3,
#                 "amount": 1.0000
#             }
#         ],
#         "items": [
#             {
#                 "name": "item1",
#                 "quantity": 1,
#                 "unitPrice": 1.00,
#                 "totalPrice": 1.00,
#                 "gtin": null
#             }
#         ]
#     },
#     "invoiceResult": {
#         "totalAmount": 1.0,
#         "transactionTypeCounter": 12283,
#         "totalCounter": 12327,
#         "invoiceCounterExtension": "NS",
#         "invoiceNumber": "5BX9A4MP-AAYH6AO0-12327",
#         "signedBy": "AAYH6AO0",
#         "sdcTime": "2024-08-28T12:37:28.033Z"
#     },
#     "journal": "============ FISCAL INVOICE ============\ ...... ovde sam odsekao, u sustini za linijski stampac je forma
# #     "isValid": true,
#     "refundStatus": null
# }
