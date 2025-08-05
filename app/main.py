from fastapi import FastAPI
from app.routes import upload, query

app = FastAPI(
    title="Smart RAG API",
    description="An intelligent document-based QA system with OCR and multimodal input",
    version="1.0.0"
)

# Register API routes
app.include_router(upload.router, prefix="/upload")
app.include_router(query.router, prefix="/query")

@app.get("/")
def root():
    return {"message": "Welcome to the Smart RAG API"}
