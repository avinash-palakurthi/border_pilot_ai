from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import ShipmentData
from typing import Optional
from app.services.ocr_service import extract_cmr_data, extract_invoice_data

router = APIRouter()


@router.post("/extract")
async def extract_documents(
    cmr: UploadFile = File(...),
    invoice: UploadFile = File(...),
    packing_list: Optional[UploadFile] = File(None),
    adr_certificate: Optional[UploadFile] = File(None),
):

    try:
        # ----------------------------
        # 1️⃣ Basic Validation
        # ----------------------------

        allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf",".webp"]

        if not cmr or not cmr.filename:
            raise HTTPException(status_code=400, detail="CMR document is required.")

        if not invoice or not invoice.filename:
            raise HTTPException(status_code=400, detail="Invoice document is required.")

        if not any(cmr.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(status_code=400, detail="Invalid CMR file type")

        if not any(invoice.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(status_code=400, detail="Invalid Invoice file type")

        print("CMR received:", cmr.filename)
        print("Invoice received:", invoice.filename)

        # ----------------------------
        # 2️⃣ OCR Extraction
        # ----------------------------

        cmr_data = await extract_cmr_data(cmr)
        invoice_data = await extract_invoice_data(invoice)

        # ----------------------------
        # 3️⃣ Merge Data
        # Invoice overrides missing CMR fields
        # ----------------------------
        
        merged = {**cmr_data}

        for key, value in invoice_data.items():
            if value:
                merged[key] = value

        # ----------------------------
        # 4️⃣ Clean Numeric Fields
        # ----------------------------

        if merged.get("gross_weight"):
            weight = str(merged["gross_weight"])
            cleaned_weight = "".join(
                c for c in weight if c.isdigit() or c == "."
            )

            try:
                merged["gross_weight"] = float(cleaned_weight)
            except:
                merged["gross_weight"] = None

        # ----------------------------
        # 5️⃣ Convert to Schema
        # ----------------------------

        merged["adr_certificate_uploaded"] = adr_certificate is not None
        extracted_data = ShipmentData(**merged)
        
        # ----------------------------
        # 6️⃣ ENS / ICS2 Completeness Check
        # ----------------------------

    
        return {
            "status": "pending_review",
            "data": extracted_data,
            
            
        }
        
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        )
