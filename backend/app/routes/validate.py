from fastapi import APIRouter
from app.models.schemas import ShipmentData
from app.services.vies_service import validate_vat
from app.services.compliance_explainer import generate_compliance_explanation
from app.services.ens_service import map_to_ens, ens_completeness_check
router = APIRouter()


@router.post("/validate")
async def validate_shipment(data: ShipmentData):

    issues = []
    warnings = []

    # -----------------------
    # 1️⃣ VAT Verification (Single Call Only)
    # -----------------------

    shipper_vies = None
    receiver_vies = None

    if data.shipper_vat:
        shipper_vies = validate_vat(data.shipper_vat)

        if shipper_vies.get("error"):
            warnings.append("VIES unavailable – manual VAT verification required")
        elif not shipper_vies.get("valid"):
            issues.append("Shipper VAT invalid in VIES system")

    if data.receiver_vat:
        receiver_vies = validate_vat(data.receiver_vat)

        if receiver_vies.get("error"):
            warnings.append("VIES unavailable – manual VAT verification required")
        elif not receiver_vies.get("valid"):
            issues.append("Receiver VAT invalid in VIES system")

    # -----------------------
    # 2️⃣ HS Code Format
    # -----------------------

    if data.hs_code:
        cleaned_hs = data.hs_code.replace(".", "")
        if not cleaned_hs.isdigit():
            issues.append("HS Code format invalid")

    # -----------------------
    # 3️⃣ Dangerous Goods Detection
    # -----------------------

    cargo = (data.cargo_description or "").lower()
    dangerous_keywords = ["lithium", "battery", "flammable", "chemical", "gasoline"]

    is_dangerous = False

    if data.hs_code and data.hs_code.startswith("27"):
        is_dangerous = True

    if any(word in cargo for word in dangerous_keywords):
        is_dangerous = True

    if is_dangerous:
        if not bool(data.adr_certificate_uploaded):
            warnings.append("ADR certificate required for dangerous goods")

    # ---------------------------
    # 4️⃣ ICS2 Pre-Departure Checks
    # ---------------------------

    if not data.hs_code:
        issues.append("ICS2: HS code required for ENS filing")

    if not data.country_dispatch:
        issues.append("ICS2: Country of dispatch required")

    if not data.country_destination:
        issues.append("ICS2: Country of destination required")

    if not data.receiver_name:
        issues.append("ICS2: Consignee name required")

    if not data.cargo_description:
        issues.append("ICS2: Goods description required")
    elif len(data.cargo_description.strip()) < 10:
        warnings.append("ICS2: Goods description too vague – provide more detail")
        # ---------------------------
    # 4️⃣.1 ENS Structured Assessment
    # ---------------------------

    ens_data = map_to_ens(data.dict())
    ens_issues = ens_completeness_check(ens_data)

    ens_assessment = {
        "status": "complete" if not ens_issues else "incomplete",
        "issues": ens_issues
    }
    # ---------------------------
    # 5️⃣ Weight Sanity Check
    # ---------------------------

    if data.gross_weight and data.gross_weight > 40000:
        warnings.append("Weight unusually high – verify transport limits")

    # ---------------------------
    # 6️⃣ Decision Engine (AFTER all checks)
    # ---------------------------

    if issues:
        status = "red"
    elif warnings:
        status = "yellow"
    else:
        status = "green"

    # ---------------------------
    # 7️⃣ Notification Logic
    # ---------------------------

    notification = None

    if status == "red":
        notification = {
            "type": "critical",
            "message": "Shipment blocked. Recheck documents with warehouse compliance officer before departure."
        }

    elif status == "yellow":
        notification = {
            "type": "warning",
            "message": "Shipment requires review. Please verify details before dispatch."
        }

    # ---------------------------
    # 8️⃣ AI Explanation
    # ---------------------------

    explanation = generate_compliance_explanation(
        data.dict(),
        issues,
        warnings
    )

    # ---------------------------
    # 9️⃣ Final Response
    # ---------------------------

    return {
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "notification": notification,
        "ai_report": explanation,
        "vies_verification": {
            "shipper": shipper_vies,
            "receiver": receiver_vies
        },
        "ens_assessment": ens_assessment
    }

