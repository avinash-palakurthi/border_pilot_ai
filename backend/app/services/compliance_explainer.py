# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def generate_compliance_explanation(data, issues, warnings):

#     prompt = f"""
# You are an EU customs compliance expert.

# Return a SHORT and CLEAR compliance summary.

# IMPORTANT RULES:
# - Do NOT use markdown symbols (#, *, -, etc.)
# - Do NOT use bullet points
# - Do NOT use numbering
# - Use simple section titles followed by colon
# - Keep response under 250 words
# - Keep language professional and direct

# Shipment:
# {data}

# Issues:
# {issues}

# Warnings:
# {warnings}

# Format exactly like this:

# Regulation Reference:
# Short explanation.

# Why Shipment Is Non-Compliant:
# Short explanation.

# Possible Consequences:
# Short explanation.

# Recommended Action:
# Short explanation.
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a strict EU customs compliance expert."},
#             {"role": "user", "content": prompt},
#         ],
#         temperature=0.1,
#     )

#     content = response.choices[0].message.content or ""
#     return content.strip()


# 


# import os
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


REGULATION_MAP = {
    "vat_intra_eu": "Directive 2006/112/EC (EU VAT Directive)",
    "dangerous_goods_road": "ADR Agreement as implemented by Directive 2008/68/EC",
    "customs_union": "Union Customs Code (Regulation (EU) No 952/2013)"
}


def determine_status(issues: List[str], warnings: List[str]) -> str:
    if issues:
        return "NON-COMPLIANT"
    if warnings:
        return "NEEDS REVIEW"
    return "COMPLIANT"


def build_vies_context(vies_results: Optional[Dict]) -> str:
    if not vies_results:
        return "Not performed"

    shipper = vies_results.get("shipper", {})
    receiver = vies_results.get("receiver", {})

    return (
        f"Shipper VAT: {shipper.get('vat', 'N/A')} — "
        f"VIES Status: {shipper.get('status', 'N/A')}\n"
        f"Receiver VAT: {receiver.get('vat', 'N/A')} — "
        f"VIES Status: {receiver.get('status', 'N/A')}"
    )


def infer_shipment_type(shipment_data: Dict) -> str:
    """
    Basic deterministic inference.
    You can expand this later.
    """
    if shipment_data.get("un_number"):
        return "dangerous_goods_road"

    if shipment_data.get("intra_eu") is True:
        return "vat_intra_eu"

    return "customs_union"


def select_regulation(shipment_type: str) -> str:
    return REGULATION_MAP.get(
        shipment_type,
        "Relevant EU regulatory framework"
    )


def generate_compliance_explanation(
    shipment_data: Dict,
    issues: List[str],
    warnings: List[str],
    vies_results: Optional[Dict] = None,
    shipment_type: Optional[str] = None
) -> str:

    status = determine_status(issues, warnings)

    # If shipment_type not provided, infer it safely
    if not shipment_type:
        shipment_type = infer_shipment_type(shipment_data)

    regulation_reference = select_regulation(shipment_type)
    vies_context = build_vies_context(vies_results)

    compliance_section = (
        "Why Shipment Is Non-Compliant"
        if status == "NON-COMPLIANT"
        else "Why Shipment Requires Attention"
        if status == "NEEDS REVIEW"
        else "Why Shipment Is Compliant"
    )

    prompt = f"""
You are a strict EU compliance expert.

IMPORTANT RULES:
- Use ONLY the regulation provided
- Do NOT invent legal references
- Do NOT override system compliance status
- Keep response under 220 words
- No markdown, no bullets, no numbering

Overall Status: {status}

Regulation To Use:
{regulation_reference}

VAT Verification (VIES) — Already Confirmed:
{vies_context}

Shipment Data:
{shipment_data}

Issues:
{issues if issues else "None"}

Warnings:
{warnings if warnings else "None"}

Format exactly like this:

Regulation Reference:
Short explanation.

{compliance_section}:
Short explanation.

Possible Consequences:
Short explanation.

Recommended Action:
Short explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a deterministic EU compliance expert. "
                        "Never invent regulations. "
                        "Never override provided compliance status."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        return (response.choices[0].message.content or "").strip()

    except Exception:
        return (
            "Compliance explanation unavailable due to a temporary system issue. "
            "Please review shipment manually."
        )