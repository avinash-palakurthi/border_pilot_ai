from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import extract, validate

app=FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(extract.router)
app.include_router(validate.router)

@app.get("/")
def root():
  return{"message":"BorderPilot Backend Running"}