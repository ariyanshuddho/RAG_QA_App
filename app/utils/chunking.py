from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits a long string into overlapping chunks.

    Args:
        text (str): The full input text.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of characters to overlap between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    start = 0
    text = text.strip().replace("\n", " ")

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
