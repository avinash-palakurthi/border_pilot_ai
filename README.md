# BorderPilot AI

AI-powered EU shipment compliance automation system.

BorderPilot automates VAT validation, ADR dangerous goods screening, and ICS2 regulatory checks using LLM-powered document analysis and structured compliance pipelines.

---

## 🚀 Problem

EU import/export compliance requires manual verification of:

- VAT numbers (VIES)
- Dangerous goods classification (ADR)
- ICS2 customs declarations
- Multi-document cross-validation

Manual workflows are slow, error-prone, and costly.

---

## 🧠 Solution

BorderPilot uses AI + rule-based validation to automate compliance workflows:

Document Upload → Vision OCR → Structured Extraction → RAG-based Regulation Check → API Validation → Structured Compliance Output

---

## 🏗️ Architecture

Frontend:
- React (S3 + CloudFront)

Backend:
- FastAPI
- Pydantic validation
- LangChain RAG pipeline
- OpenAI Vision for OCR

Data & Infra:
- AWS EC2
- Docker
- EU VIES API integration

---

## 🔎 Core Features

✅ OpenAI Vision OCR for shipment document extraction  
✅ Pydantic schema validation for structured compliance fields  
✅ RAG over 9 EU regulatory documents  
✅ Real-time VAT validation via EU VIES API  
✅ Structured compliance output with recommended actions  
✅ Timestamped verification logs  

---

## 🛡️ Hallucination Control Strategy

- Retrieval-only regulation responses
- Structured output enforced via Pydantic
- API-based validation for VAT confirmation
- Deterministic validation layers before final output

---

## 📊 Example Workflow

1. Upload CMR / invoice
2. OCR extracts structured fields
3. AI maps goods to ADR regulation
4. VAT number verified via VIES
5. Compliance status returned with flags

---

## ⚙️ Deployment

- Dockerized backend
- AWS EC2 hosting
- S3 + CloudFront for frontend
- SSL via ACM

Live Demo:
https://borderpilot.anuveekshi.com/

---

## 🔮 Future Improvements

- Multi-document batch processing
- Cost monitoring dashboard
- Retry and fallback model strategy
- Observability logging (LangSmith integration planned)

---

## 👨‍💻 Author

Avinash Palakurthi  
Applied AI Engineer – Regulatory Automation