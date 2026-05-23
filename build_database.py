import os
import fitz  # PyMuPDF
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
import re

# --- 1. CONFIGURATION & SECURITY ---
# Load environment variables from the .env file to protect your API key
load_dotenv()

# Local relative path to your textbook
PDF_SOURCES = [

    {
        "path": "./data/VLSI Design_Neil Weste_Text book.pdf",

        "source": "Neil Weste",

        "subject": "VLSI",

        "difficulty": "advanced"
    },

    {
        "path": "./data/Morris Mano.pdf",

        "source": "Morris Mano",

        "subject": "Digital Electronics",

        "difficulty": "beginner"
    }
]

# --- 2. DATA EXTRACTION & PROCESSING ---

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text
# This function uses a regex pattern to identify textbook-style section headings (e.g., "1.1 Introduction") and splits the text into sections based on these headings. Each section is stored as a dictionary with a "title" and "content". If no headings are found, it returns the entire text as a single section.
def split_into_sections(text):

    # Regex pattern for textbook-style headings
    pattern = r"\n\d+\.\d+\s+[A-Z][^\n]*"

    matches = list(re.finditer(pattern, text))

    sections = []

    # If no headings found, fallback
    if not matches:
        return [{"title": "General", "content": text}]

    for i in range(len(matches)):

        start = matches[i].start()

        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        section_title = matches[i].group().strip()

        sections.append({
            "title": section_title,
            "content": section_text
        })

    return sections

def create_recursive_chunks(

    text,

    source_name,

    subject_name,

    difficulty_level
    ):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )
    
    raw_chunks = text_splitter.split_text(text)

    structured_chunks = []

    for idx, chunk in enumerate(raw_chunks):

        structured_chunk = {
            "text": chunk,
            "metadata": {
                "chunk_id": idx,
                "source": source_name,
                "subject": subject_name,
                "difficulty": difficulty_level,
                "chunk_length": len(chunk)
            }
        }

        structured_chunks.append(structured_chunk)
    return structured_chunks

print("Extracting and processing textbooks...")

text_chunks = []

for pdf in PDF_SOURCES:

    pdf_path = pdf["path"]

    source_name = pdf["source"]

    subject_name = pdf["subject"]

    difficulty_level = pdf["difficulty"]

    if not os.path.exists(pdf_path):

        raise FileNotFoundError(
            f"Could not find PDF: {pdf_path}"
        )

    print(f"\nProcessing: {source_name}")

    raw_book_text = extract_text_from_pdf(
        pdf_path
    )

    chunks = create_recursive_chunks(

        raw_book_text,

        source_name,

        subject_name,

        difficulty_level
    )

    text_chunks.extend(chunks)

print(
    f"\nTotal chunks created: "
    f"{len(text_chunks)}"
)

# --- 3. VECTOR DATABASE (FAISS) CONSTRUCTION ---
print("Loading local embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Translating text into math vectors...")
chunk_texts = [chunk["text"] for chunk in text_chunks]
# --- BM25 Corpus Creation ---

tokenized_chunks = [
    text.lower().split()
    for text in chunk_texts
]

bm25 = BM25Okapi(tokenized_chunks)

embeddings = embedding_model.encode(chunk_texts)
dimension = embeddings.shape[1]

# Create and populate the FAISS Index
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))
print(f"Index ready! Total Vectors stored: {index.ntotal}")

# --- 4. EXPORTING THE BRAIN ---
print("Saving vector database and text chunks locally...")
# These will save directly to your current VS Code folder
faiss.write_index(index, "vector_index.faiss")
with open("text_chunks.pkl", "wb") as f:
    pickle.dump(text_chunks, f)
with open("bm25.pkl", "wb") as f:
    pickle.dump(bm25, f)

print("Export complete. You are ready to run the Streamlit dashboard!")