from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedder import load_faiss_index, model
from app.services.llm import ask_llm  

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    file_id: str

@router.post("/")
async def query_file(request: QueryRequest):
    try:
        # Step 1: Load FAISS index and chunks
        index, chunks = load_faiss_index(request.file_id)
        if index is None or len(chunks) == 0:
            raise HTTPException(status_code=404, detail="No FAISS index or chunks found for this file.")

        # Step 2: Embed question
        question_embedding = model.encode([request.question])

        # Step 3: Search top-k in FAISS
        D, I = index.search(question_embedding, k=3)
        relevant_chunks = [chunks[i] for i in I[0] if i < len(chunks)]

        if not relevant_chunks:
            raise HTTPException(status_code=404, detail="No relevant chunks found for this question.")

        # Step 4: Create context
        context = "\n\n".join(relevant_chunks)

        # Step 5: Ask HuggingFace LLM
        answer = ask_llm(request.question, context)

        return {
            "question": request.question,
            "file_id": request.file_id,
            "answer": answer,
            "context": context,
            "top_chunks": relevant_chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
