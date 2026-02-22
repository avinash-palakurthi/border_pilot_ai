from pydantic import BaseModel
from typing import Optional


class ShipmentData(BaseModel):
  shipper_name:Optional[str]
  shipper_vat:Optional[str]
  receiver_name:Optional[str]
  receiver_vat:Optional[str]
  hs_code:Optional[str]
  cargo_description:Optional[str]
  gross_weight:Optional[float]
  un_number:Optional[str]
  country_dispatch:Optional[str]
  country_destination:Optional[str]
  adr_certificate_uploaded: Optional[bool] = False
  

