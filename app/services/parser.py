from pathlib import Path
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import sqlite3
import docx
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(file_path: Path) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path: Path) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path: Path) -> str:
    return Path(file_path).read_text()

def extract_text_from_image(file_path: Path) -> str:
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)

def extract_text_from_csv(file_path: Path) -> str:
    df = pd.read_csv(file_path)
    return df.to_string(index=False)

def extract_text_from_sqlite(file_path: Path) -> str:
    text = ""
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        name = table_name[0]
        text += f"\nTable: {name}\n"
        df = pd.read_sql_query(f"SELECT * FROM {name}", conn)
        text += df.to_string(index=False) + "\n"

    conn.close()
    return text
