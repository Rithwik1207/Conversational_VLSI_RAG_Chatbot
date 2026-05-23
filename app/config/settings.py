# --- Embedding Models ---

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

RERANK_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# --- Vector Store Paths ---

FAISS_INDEX_PATH = "vector_index.faiss"

TEXT_CHUNKS_PATH = "text_chunks.pkl"

BM25_PATH = "bm25.pkl"

# --- LLM Settings ---

LLM_MODEL = "llama-3.3-70b-versatile"

LLM_TEMPERATURE = 0.2

CLARIFICATION_TEMPERATURE = 0.2

QUERY_REWRITE_TEMPERATURE = 0.0

# --- Retrieval Settings ---

SIMPLE_RETRIEVAL_K = 2

ADVANCED_RETRIEVAL_K = 5

BM25_TOP_K = 3

FINAL_SIMPLE_CHUNKS = 1

FINAL_ADVANCED_CHUNKS = 2

# --- UI Settings ---

PAGE_TITLE = "VLSI AI Assistant"

APP_TITLE = "AI Tutor for VLSI and Digital Design"