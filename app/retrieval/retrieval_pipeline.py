from app.retrieval.hybrid_search import (
    retrieve_context
)

from app.tutoring.intent_router import (
    normalize_query,
    detect_complexity,
    is_followup,
    is_valid_topic
)
from app.core.debug import (
    debug_log
)


def execute_retrieval_pipeline(

    user_question,

    reconstruct_followup_query,

    current_topic

):
    print("PIPELINE EXECUTING")

    rewritten_query = normalize_query(
        user_question
    )

    debug_log(
    "Normalized Query",
    rewritten_query
    )

    followup = is_followup(
        user_question
    )

    debug_log(
    "Followup Detection",
    followup
    )

    if followup:

        rewritten_query = (
            reconstruct_followup_query(
                current_topic,
                user_question
            )
        )

    if is_valid_topic(rewritten_query):

        current_topic = rewritten_query

    complexity = detect_complexity(
        rewritten_query
    )

    debug_log(
    "Detected Complexity",
    complexity
    )

    retrieved_chunks = retrieve_context(
        rewritten_query,
        complexity
    )

    debug_log(
    "Retrieved Chunks Count",
    len(retrieved_chunks)
    )

    context_text = ""

    for i, chunk in enumerate(retrieved_chunks):

        chunk_text = chunk["text"]

        metadata = chunk["metadata"]

        source = metadata.get(
            "source",
            "Unknown"
        )

        subject = metadata.get(
            "subject",
            "Unknown"
        )

        difficulty = metadata.get(
            "difficulty",
            "Unknown"
        )

        context_text += (

            f"\n--- Retrieved Educational Context {i+1} ---\n"

            f"Source Textbook: {source}\n"

            f"Subject Area: {subject}\n"

            f"Difficulty Level: {difficulty}\n\n"

            f"{chunk_text}\n\n"
        )

    return {

        "rewritten_query": rewritten_query,

        "complexity": complexity,

        "context_text": context_text,

        "current_topic": current_topic
    }