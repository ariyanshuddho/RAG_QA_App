from typing import List

def classify_document_type(text_chunks: List[str]) -> str:
    """
    Very basic rule-based document type classifier based on keyword matching.
    Can be replaced later with ML or embedding-based classifier.
    """
    joined_text = " ".join(text_chunks).lower()

    if "curriculum vitae" in joined_text or "summary" in joined_text or "skills" in joined_text:
        return "CV"
    elif "invoice number" in joined_text or "total due" in joined_text:
        return "Invoice"
    elif "report" in joined_text and "introduction" in joined_text:
        return "Report"
    elif "contract" in joined_text or "agreement" in joined_text:
        return "Contract"
    elif "dear" in joined_text and "sincerely" in joined_text:
        return "Letter"
    else:
        return "Unknown"
