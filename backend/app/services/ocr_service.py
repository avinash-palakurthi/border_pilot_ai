import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def extract_cmr_data(upload_file):

    file_bytes = await upload_file.read()
    base64_image = base64.b64encode(file_bytes).decode("utf-8")

    prompt = """
    Extract structured shipment data from this CMR document.

    Return strictly JSON with keys:
    shipper_name
    shipper_vat
    receiver_name
    receiver_vat
    hs_code
    cargo_description
    gross_weight
    un_number
    country_dispatch
    country_destination

    If a field is missing, return null.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("OpenAI returned empty response")

    cleaned = content.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    data_dict = json.loads(cleaned)

    return data_dict


async def extract_invoice_data(upload_file):
  file_bytes=await upload_file.read()
  base64_image=base64.b64encode(file_bytes).decode("utf-8")
  
  prompt="""
  Extract structured shipment data from this COMMERCIAL INVOICE.

    Return ONLY valid JSON (no explanation, no markdown).

    Use this exact structure:

    {
      "hs_code": null,
      "shipper_vat": null,
      "receiver_vat": null
    }

    If a field is missing, return null.
  """
  
  response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role":"user",
        "content":[
          {"type":"text","text":prompt},
          {
            "type":"image_url",
            "image_url":{
              "url":f"data:image/png;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    temperature=0
  )
  
  
  content=response.choices[0].message.content
  
  if not content:
    raise ValueError("OpenAI returned empty response (Invoice) ")
  
  cleaned=content.strip()
  
  if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

  return json.loads(cleaned)