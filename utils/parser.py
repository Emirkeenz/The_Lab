import os
import docx2txt
import fitz  # PyMuPDF
import json
import chromadb

from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.storage.storage_context import StorageContext

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Папки для хранения
CHUNKS_DIR = "lesson_chunks"
INDEX_DIR = "rag_indexes"
os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# Сохранение чанков в JSON
def save_chunks_to_json(chunks: list[str], subject: str, lesson_name: str):
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in lesson_name)
    subject_dir = os.path.join(CHUNKS_DIR, subject)
    os.makedirs(subject_dir, exist_ok=True)
    file_path = os.path.join(subject_dir, f"{safe_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

# Извлечение текста из файлов
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

# 🔥 Разделение текста на чанки через LangChain
def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_text(text)

# 🔧 Создание RAG-индекса
def build_rag_index(chunks: list[str], subject: str, lesson_name: str):
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in lesson_name)
    db_path = os.path.join(INDEX_DIR, f"{subject}_{safe_name}")

    documents = [Document(text=chunk) for chunk in chunks]
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    chroma_client = chromadb.PersistentClient(path=db_path)
    vector_store = ChromaVectorStore(chroma_collection=chroma_client.get_or_create_collection("rag"))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(nodes, storage_context=storage_context)
    return index

# 📥 Запрос к индексу
def query_lesson(index: VectorStoreIndex, question: str) -> str:
    query_engine = index.as_query_engine()
    return query_engine.query(question).response
