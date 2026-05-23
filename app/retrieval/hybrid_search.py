import faiss
import pickle
from app.config.settings import (
    EMBEDDING_MODEL,
    RERANK_MODEL,
    FAISS_INDEX_PATH,
    TEXT_CHUNKS_PATH,
    BM25_PATH,
    SIMPLE_RETRIEVAL_K,
    ADVANCED_RETRIEVAL_K,
    BM25_TOP_K,
    FINAL_SIMPLE_CHUNKS,
    FINAL_ADVANCED_CHUNKS
)
from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

# --- Load Backend ---

def load_backend():

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    reranker = CrossEncoder(
        RERANK_MODEL
    )

    index = faiss.read_index(
        FAISS_INDEX_PATH
    )

    with open(TEXT_CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    with open(BM25_PATH, "rb") as f:
        bm25 = pickle.load(f)

    return embedding_model, reranker, index, chunks, bm25


embedding_model, reranker, index, text_chunks, bm25 = load_backend()


# --- Retrieval Function ---

def retrieve_context(rewritten_query, complexity):

    question_vector = embedding_model.encode(
        [rewritten_query]
    ).astype('float32')

    if complexity == "simple":
        retrieval_k = SIMPLE_RETRIEVAL_K
    else:
        retrieval_k = ADVANCED_RETRIEVAL_K

    distances, indices = index.search(
        question_vector,
        k=retrieval_k
    )

    # --- BM25 Retrieval ---

    tokenized_query = rewritten_query.lower().split()

    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_top_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:BM25_TOP_K]

    # --- Hybrid Merge ---

    combined_indices = (
        list(indices[0]) + bm25_top_indices
    )

    unique_indices = list(
        dict.fromkeys(combined_indices)
    )

    initial_chunks = [
        text_chunks[i]
        for i in unique_indices[:5]
    ]

    # --- Reranking ---

    rerank_pairs = [
        (rewritten_query, chunk["text"])
        for chunk in initial_chunks
    ]

    rerank_scores = reranker.predict(
        rerank_pairs
    )

    scored_chunks = list(
        zip(rerank_scores, initial_chunks)
    )

    scored_chunks.sort(
        key=lambda x: x[0],
        reverse=True
    )

    if complexity == "simple":
        final_chunk_count = FINAL_SIMPLE_CHUNKS
    else:
        final_chunk_count = FINAL_ADVANCED_CHUNKS

    retrieved_chunks = [
        chunk
        for score, chunk in scored_chunks[:final_chunk_count]
    ]

    return retrieved_chunks