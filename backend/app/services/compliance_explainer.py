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


import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_compliance_explanation(data, issues, warnings, vies_results=None):

    # Determine overall status
    if not issues and not warnings:
        status = "COMPLIANT"
    elif issues:
        status = "NON-COMPLIANT"
    else:
        status = "NEEDS REVIEW"

    # Dynamic section title — fixed to include warnings
    if not issues and not warnings:
        compliance_section = "Why Shipment Is Compliant"
    elif issues:
        compliance_section = "Why Shipment Is Non-Compliant"
    else:
        compliance_section = "Why Shipment Requires Attention"

    # Build VIES context
    vies_context = "Not performed"
    if vies_results:
        shipper = vies_results.get("shipper", {})
        receiver = vies_results.get("receiver", {})
        vies_context = f"""Shipper VAT: {shipper.get('vat')} — VIES Status: {shipper.get('status')}
Receiver VAT: {receiver.get('vat')} — VIES Status: {receiver.get('status')}"""

    prompt = f"""
You are an EU customs compliance expert.

Return a SHORT and CLEAR compliance summary.

IMPORTANT RULES:
- Do NOT use markdown symbols (#, *, -, etc.)
- Do NOT use bullet points
- Do NOT use numbering
- Use simple section titles followed by colon
- Keep response under 250 words
- Keep language professional and direct
- VIES VAT verification is already completed — trust the results below, do NOT re-assess VAT validity
- Overall status is already determined — align your assessment with it exactly

Overall Status: {status}

VAT Verification (VIES) — Already Confirmed:
{vies_context}

Shipment:
{data}

Issues (empty means no issues):
{issues if issues else "None"}

Warnings (empty means no warnings):
{warnings if warnings else "None"}

Format exactly like this:

Regulation Reference:
Short explanation.

{compliance_section}:
Short explanation based on the actual issues and warnings above.

Possible Consequences:
Short explanation.

Recommended Action:
Short explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict EU customs compliance expert. "
                    "Always trust pre-verified VIES results provided to you. "
                    "Do not re-assess VAT validity. "
                    "Align your assessment exactly with the overall status provided."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content or ""
    return content.strip()

    # Determine overall status
    if not issues and not warnings:
        status = "COMPLIANT"
    elif issues:
        status = "NON-COMPLIANT"
    else:
        status = "NEEDS REVIEW"

    # Dynamic section title
    compliance_section = (
        "Why Shipment Is Non-Compliant" if issues else "Why Shipment Is Compliant"
    )

    # Build VIES context
    vies_context = "Not performed"
    if vies_results:
        shipper = vies_results.get("shipper", {})
        receiver = vies_results.get("receiver", {})
        vies_context = f"""Shipper VAT: {shipper.get('vat')} — VIES Status: {shipper.get('status')}
Receiver VAT: {receiver.get('vat')} — VIES Status: {receiver.get('status')}"""

    prompt = f"""
You are an EU customs compliance expert.

Return a SHORT and CLEAR compliance summary.

IMPORTANT RULES:
- Do NOT use markdown symbols (#, *, -, etc.)
- Do NOT use bullet points
- Do NOT use numbering
- Use simple section titles followed by colon
- Keep response under 250 words
- Keep language professional and direct
- VIES VAT verification is already completed — trust the results below, do NOT re-assess VAT validity

Overall Status: {status}

VAT Verification (VIES) — Already Confirmed:
{vies_context}

Shipment:
{data}

Issues (empty means no issues):
{issues if issues else "None"}

Warnings (empty means no warnings):
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict EU customs compliance expert. Always trust pre-verified VIES results provided to you. Do not re-assess VAT validity.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content or ""
    return content.strip()