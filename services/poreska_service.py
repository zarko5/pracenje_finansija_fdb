from models import Transaction, TransactionView
import requests
from datetime import datetime

#### importi za scraper
import sys
import re
import time
import httpx
import json
import base64
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup, NavigableString


class PoreskaService:
    POST_URL = "https://suf.purs.gov.rs/specifications"
    MAX_RETRIES = 5
    RETRY_DELAY = 1.5
    FONT_SIZE = 13
    LINE_HEIGHT_MULT = 1.42857143
    SCALE = 2
    DPI = (300, 300)

    def __init__(self):
        pass

    @staticmethod
    def parse_url_json(url):
        headers = {"Accept": "application/json"}
        try:
            resp = requests.get(url,headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            items_data = PoreskaService.parse_scrape_url(url)
            data["items"] = items_data["items"]
            return data

        except requests.exceptions.RequestException as e:
            print(f"greska pri zahtevu poreskoj: {e}")

    def parse_invoice_data(invoice_data, user_id: int, category_id: int) -> list[Transaction] | None:
        if "invoiceRequest" not in invoice_data:
            print("los odgovor od poreske")
            return None

        invoice_request = invoice_data["invoiceRequest"]
        invoice_result = invoice_data["invoiceResult"]

        if "items" not in invoice_data:
            print("nema stavki na racunu")
            return None

        items = invoice_data["items"]
        transactions = []

        # datum = datetime.strptime(invoice_result.get("sdcTime"), "%Y-%m-%dT%H:%M:%S.%fZ")
        datum = datetime.fromisoformat(invoice_result.get("sdcTime").replace("Z", "+00:00"))
        ### transakcija za svaki artikal na racunu, nije idealno
        ### ali moze biti korisnije za svrstavanje po kategorijama kasnije
        for item in items:
            name = item.get("name")
            quantity = item.get("quantity")
            unit_price = item.get("unitPrice")
            total_price = item.get("total")

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

    @staticmethod
    def parse_scrape_url(url):

        token_pattern = r"viewModel\.Token\(\s*'([^']+)'\s*\);"
        invoice_pattern = r"viewModel\.InvoiceNumber\(\s*'([^']+)'\s*\);"

        try:
            with httpx.Client(timeout=10, follow_redirects=True) as client:

                response = client.get(url)
                response.raise_for_status()
                html = response.text

                soup = BeautifulSoup(html, "html.parser")
                pre = soup.find("pre")

                elements = []

                if pre:
                    for node in pre.descendants:
                        if isinstance(node, NavigableString):
                            txt = str(node)
                            if txt.strip():
                                elements.append(("text", txt))
                        elif getattr(node, "name", None) == "img":
                            elements.append(("img", node))

                token = PoreskaService.extract_value(token_pattern, html)
                invoice = PoreskaService.extract_value(invoice_pattern, html)

                # print(token or "missing token")
                # print(invoice or "missing invoice")

                output = PoreskaService.render_receipt_image(elements)
                # print(f"[DEBUG] Receipt image saved to: {output}")

                if token and invoice:
                    for attempt in range(1, PoreskaService.MAX_RETRIES + 1):
                        # print(f"[DEBUG] Attempt {attempt}", file=sys.stderr)
                        try:
                            post_response = client.post(
                                PoreskaService.POST_URL,
                                data={
                                    "invoiceNumber": invoice,
                                    "token": token
                                }
                            )

                            post_response.raise_for_status()
                            data = post_response.json()

                            # print(f"[DEBUG] {data}", file=sys.stderr)

                            if data.get("success") is True:
                                # return json.dumps(data)
                                return data
                                break

                            time.sleep(PoreskaService.RETRY_DELAY)

                        except Exception as e:
                            print(f"[DEBUG] error: {e}", file=sys.stderr)
                            time.sleep(PoreskaService.RETRY_DELAY)

                # json.dumps(data)
        except Exception as e:
            print(f"Fatal error: {e}", file=sys.stderr)
            sys.exit(1)


    @staticmethod
    def extract_value(pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def extract_qr_base64(src):
        match = re.search(r"base64,([A-Za-z0-9+/=]+)", src)
        return match.group(1) if match else None

    @staticmethod
    def get_img_width(tag):
        try:
            return int(tag.get("width", 160))
        except:
            return 160

    @staticmethod
    def render_receipt_image(elements, output_path="receipt.png"):
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                PoreskaService.FONT_SIZE * PoreskaService.SCALE
            )
        except:
            font = ImageFont.load_default()

        padding = 20 * PoreskaService.SCALE
        line_height = int(PoreskaService.FONT_SIZE * PoreskaService.LINE_HEIGHT_MULT * PoreskaService.SCALE)

        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))

        # char grid reference for alignment stability
        char_width = dummy.textbbox((0, 0), "M", font=font)[2]

        max_text_width = 0
        qr_max_width = 0

        for typ, val in elements:
            if typ == "text":
                lines = val.split("\n")
                for line in lines:
                    line = line.replace("\r", "")
                    bbox = dummy.textbbox((0, 0), line, font=font)
                    w = bbox[2] - bbox[0]
                    max_text_width = max(max_text_width, w)

            elif typ == "img":
                qr_max_width = max(qr_max_width, PoreskaService.get_img_width(val) * PoreskaService.SCALE)

        content_width = max(max_text_width, qr_max_width)
        width = content_width + (padding * 2)

        height = 8000

        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        y = padding

        for typ, val in elements:
            if typ == "text":
                text = val.replace("\r", "")
                lines = text.split("\n")

                for line in lines:
                    clean = line.replace("\u00a0", " ")
                    draw.text((padding, y), clean, fill="black", font=font)
                    y += line_height

            elif typ == "img":
                src = val.get("src", "")
                b64 = PoreskaService.extract_qr_base64(src)

                if b64:
                    qr_bytes = base64.b64decode(b64)
                    qr_img = Image.open(BytesIO(qr_bytes)).convert("RGB")

                    qr_size = PoreskaService.get_img_width(val) * PoreskaService.SCALE
                    qr_img = qr_img.resize((qr_size, qr_size))

                    # snap QR to character grid (fix half-character drift)
                    content_center = padding + (
                        ((content_width // char_width) * char_width - qr_size) // 2
                    )

                    img.paste(qr_img, (int(content_center), y))

                    # tighter spacing after QR (receipt-like flow)
                    y += qr_size + int(line_height * 0.3)

        cropped = img.crop((0, 0, width, y + padding))
        cropped.save(output_path, dpi=PoreskaService.DPI)
        return output_path


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
