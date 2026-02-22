def map_to_ens(shipment_data: dict) -> dict:
    return {
        "consignor_name": shipment_data.get("shipper_name"),
        "consignee_name": shipment_data.get("receiver_name"),
        "carrier_eori": shipment_data.get("carrier_eori"),
        "hs_code": shipment_data.get("hs_code"),
        "goods_description": shipment_data.get("goods_description"),
        "gross_weight": shipment_data.get("gross_weight"),
        "country_of_dispatch": shipment_data.get("country_dispatch"),
        "country_of_destination": shipment_data.get("country_destination"),
        "un_number": shipment_data.get("un_number"),
    }


def ens_completeness_check(ens_data: dict) -> list:
    issues = []

    if not ens_data.get("hs_code") or len(str(ens_data["hs_code"])) < 6:
        issues.append("HS Code must be minimum 6 digits for ENS filing.")

    if not ens_data.get("consignor_name"):
        issues.append("Consignor information missing.")

    if not ens_data.get("country_of_dispatch"):
        issues.append("Country of dispatch required.")

    if not ens_data.get("gross_weight"):
        issues.append("Gross weight required for ENS.")

    return issues