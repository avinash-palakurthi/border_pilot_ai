import os
import uuid
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct

# -----------------------------------
# ENV
# -----------------------------------

load_dotenv()

# ✅ Fix: Use fallback "" to avoid str | None type error
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
QDRANT_URL: str = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

DATA_FOLDER = "./data"
COLLECTION_NAME = "borderpilot_regulations"
BATCH_SIZE = 8
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# -----------------------------------
# CLIENTS
# -----------------------------------

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60 
)

# ✅ Fix: Now OPENAI_API_KEY is guaranteed str, no type error
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = OpenAIEmbeddings()
llm_client = OpenAI()


# -----------------------------------
# 1️⃣ Load All Documents
# -----------------------------------

def load_all_documents():
    documents = []

    for file_path in Path(DATA_FOLDER).glob("*"):
        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

        elif file_path.suffix.lower() == ".csv":
            loader = CSVLoader(str(file_path))
            documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents")
    return documents


# -----------------------------------
# 2️⃣ Split Documents
# -----------------------------------

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks


# -----------------------------------
# 3️⃣ LLM Classification
# -----------------------------------

def classify_chunk(text: str) -> dict:
    prompt = f"""
Classify this EU regulation text.

Return ONLY JSON (no markdown, no code blocks):

{{
  "regulation_name": "ICS2 | ADR | VAT | HS | EUDR | OTHER",
  "category": "ens_filing | vat_validation | dangerous_goods_transport | commodity_classification | import_control | other",
  "risk_type": "documentation_missing | misclassification | non_declaration | transport_violation | other",
  "article_reference": "Article X or null"
}}

TEXT:
{text[:1200]}
"""

    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw_content = response.choices[0].message.content

    # ✅ Fix: Guard against None before calling .strip()
    if not raw_content:
        return {
            "regulation_name": "OTHER",
            "category": "other",
            "risk_type": "other",
            "article_reference": None
        }

    content = raw_content.strip()

    # Strip markdown code blocks if LLM wraps response in ```json ... ```
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "regulation_name": "OTHER",
            "category": "other",
            "risk_type": "other",
            "article_reference": None
        }


# -----------------------------------
# 4️⃣ Create Collection (Safe)
# -----------------------------------

def create_payload_indexes():
    from qdrant_client.http import models as rest_models

    # Create keyword index for category
    qdrant_client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="category",
        field_schema=rest_models.PayloadSchemaType.KEYWORD,
    )

    print("Payload index for 'category' created.")



def create_collection():
    existing = [c.name for c in qdrant_client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE
            )
        )
        print("Collection created")
    else:
        print("Collection already exists")

    # 🔥 Always ensure payload index exists
    create_payload_indexes()



# -----------------------------------
# 5️⃣ Embed + Classify + Upload
# -----------------------------------

def embed_and_upload(chunks):

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i+BATCH_SIZE]

        texts = [doc.page_content for doc in batch]
        vectors = embeddings.embed_documents(texts)

        points = []

        for doc, vector in zip(batch, vectors):
            classification = classify_chunk(doc.page_content)

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "document": doc.page_content,
                        "source": doc.metadata.get("source", ""),
                        "regulation_name": classification.get("regulation_name", "OTHER"),
                        "category": classification.get("category", "other"),
                        "risk_type": classification.get("risk_type", "other"),
                        "article_reference": classification.get("article_reference", ""),
                    }
                )
            )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

        print(f"Uploaded batch {i//BATCH_SIZE + 1}")


# -----------------------------------
# 6️⃣ Full Ingestion Pipeline
# -----------------------------------

def run_ingestion():
    print("Loading documents...")
    documents = load_all_documents()

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Creating collection...")
    create_collection()

    print("Embedding + Classifying + Uploading...")
    embed_and_upload(chunks)

    print("Ingestion completed successfully 🚀")


# -----------------------------------
# 7️⃣ Retrieval (Runtime Only)
# -----------------------------------

def retrieve_context(query: str, category_filter: str | None = None) -> str:

    query_vector = embeddings.embed_query(query)

    search_filter = None

    if category_filter:
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(value=category_filter)
                )
            ]
        )

    response = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=search_filter,
        limit=5,
    )
    results = response.points

    # ✅ Fix: payload is a plain dict — safely access with .get() + default values
    output = []
    for hit in results:
        payload: dict = hit.payload if hit.payload else {}
        regulation = payload.get("regulation_name", "N/A")
        article = payload.get("article_reference", "N/A")
        document = payload.get("document", "")
        output.append(f"[{regulation} - {article}]\n{document}")

    return "\n\n".join(output)


if __name__ == "__main__":
    run_ingestion()