import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_compliance_explanation(data, issues, warnings):

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

Shipment:
{data}

Issues:
{issues}

Warnings:
{warnings}

Format exactly like this:

Regulation Reference:
Short explanation.

Why Shipment Is Non-Compliant:
Short explanation.

Possible Consequences:
Short explanation.

Recommended Action:
Short explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict EU customs compliance expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content or ""
    return content.strip()
