from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from pathlib import Path

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

FAISS_DIR = "faiss_store"
Path(FAISS_DIR).mkdir(exist_ok=True)

def generate_embeddings(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings)


def save_faiss_index(file_id, embeddings, chunks):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, f"{FAISS_DIR}/{file_id}.index")

    with open(f"{FAISS_DIR}/{file_id}.chunks", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.replace("\n", " ") + "\n")

def load_faiss_index(file_id):
    index_path = f"{FAISS_DIR}/{file_id}.index"
    chunks_path = f"{FAISS_DIR}/{file_id}.chunks"

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return None, []

    index = faiss.read_index(index_path)
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = [line.strip() for line in f.readlines()]
    return index, chunks
