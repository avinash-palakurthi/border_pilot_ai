# from zeep import Client
# from zeep.transports import Transport
# from requests import Session
# import logging

# VIES_WSDL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

# # Create session with timeout
# session = Session()
# transport = Transport(session=session, timeout=10)

# client = Client(VIES_WSDL, transport=transport)


# def validate_vat(vat_number: str):
#     try:
#         # -------------------------
#         # 1️⃣ Normalize VAT
#         # -------------------------
#         vat_number = vat_number.replace(" ", "").strip().upper()

#         if not vat_number or len(vat_number) < 3:
#             return {
#                 "valid": False,
#                 "error": "Invalid VAT format"
#             }

#         country_code = vat_number[:2]
#         number = vat_number[2:]

#         # -------------------------
#         # 2️⃣ Call VIES
#         # -------------------------
#         response = client.service.checkVat(
#             countryCode=country_code,
#             vatNumber=number
#         )

#         return {
#             "valid": bool(response.valid),
#             "name": response.name if response.name else None,
#             "address": response.address if response.address else None
#         }

#     except Exception as e:
#         logging.error(f"VIES error: {str(e)}")

#         return {
#             "valid": False,
#             "error": "VIES service unavailable or request blocked"
#         }


from zeep import Client
from zeep.transports import Transport
from requests import Session
import logging
from datetime import datetime

VIES_WSDL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

# Create session with timeout
session = Session()
transport = Transport(session=session, timeout=10)

client = Client(VIES_WSDL, transport=transport)


def validate_vat(vat_number: str):
    try:
        # -------------------------
        # 1️⃣ Normalize VAT
        # -------------------------
        vat_number = vat_number.replace(" ", "").strip().upper()

        if not vat_number or len(vat_number) < 3:
            return {
                "valid": False,
                "error": "Invalid VAT format",
                "verification_token": None,
                "request_date": None
            }

        country_code = vat_number[:2]
        number = vat_number[2:]

        # -------------------------
        # 2️⃣ Call VIES
        # -------------------------
        response = client.service.checkVat(
            countryCode=country_code,
            vatNumber=number
        )

        request_time = str(response.requestDate)

        verification_token = f"VIES-{vat_number}-{request_time}"

        return {
            "valid": bool(response.valid),
            "name": response.name if response.name else None,
            "address": response.address if response.address else None,
            "request_date": request_time,
            "verification_token": verification_token,
            "error": None
        }

    except Exception as e:
        logging.error(f"VIES error: {str(e)}")

        return {
            "valid": False,
            "error": "VIES service unavailable or request blocked",
            "verification_token": None,
            "request_date": None
        }