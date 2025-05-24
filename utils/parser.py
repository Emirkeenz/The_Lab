import os
import docx2txt
import fitz  # PyMuPDF
import json

CHUNKS_DIR = "lesson_chunks"
os.makedirs(CHUNKS_DIR, exist_ok=True)

def save_chunks_to_json(chunks: list[str], subject: str, lesson_name: str):
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in lesson_name)
    subject_dir = os.path.join(CHUNKS_DIR, subject)
    os.makedirs(subject_dir, exist_ok=True)
    file_path = os.path.join(subject_dir, f"{safe_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Поддерживаются только .pdf и .docx файлы")

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    return docx2txt.process(file_path)

def split_text_into_chunks(text: str, max_tokens: int = 300) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_tokens:
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
