import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.ocr import extract_text_from_image
from app.utils.pdf import extract_text_from_pdf
from app.utils.text_splitter import split_text
from app.services.embedder import generate_embeddings, save_faiss_index

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_id = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join(UPLOAD_DIR, file_id)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[INFO] File saved as: {file_path}")

        # Step 1: Extract text based on file type
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(file_path)
        elif file.filename.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No text found in the document.")

        print(f"[INFO] Extracted text length: {len(text)}")

        # Step 2: Split into chunks
        chunks = split_text(text)
        print(f"[INFO] Total chunks: {len(chunks)}")

        # Step 3: Generate embeddings
        embeddings = generate_embeddings(chunks)
        print(f"[INFO] Embeddings generated - shape: {embeddings.shape}")

        # Step 4: Save FAISS index
        save_faiss_index(file_id, embeddings, chunks)

        # ✅ Step 5: Return file ID, chunk count, and preview of extracted text
        return {
            "file_id": file_id,
            "total_chunks": len(chunks),
            "text_preview": text[:1500]  # Adjust size as needed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
