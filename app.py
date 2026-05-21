import streamlit as st
import faiss
import pickle
import os
import re
from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)
from groq import Groq
from dotenv import load_dotenv

# --- 1. System Initialization ---
load_dotenv()
st.set_page_config(page_title="VLSI AI Assistant", layout="centered")
st.title("🔌 VLSI Engineering Knowledge Base")

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- 2. Initialize Memory (The Notepad) ---
# If this is the first time opening the app, create an empty list for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_user_query" not in st.session_state:
    st.session_state.last_user_query = ""
if "learning_profile" not in st.session_state:

    st.session_state.learning_profile = {

        "skill_level": "beginner",

        "confused_topics": [],

        "explained_topics": [],

        "preferred_style": "analogies"
    }
if "current_topic" not in st.session_state:

    st.session_state.current_topic = ""

# --- 3. Load the Exported Data ---
@st.cache_resource
def load_backend():
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    reranker = CrossEncoder(
    'cross-encoder/ms-marco-MiniLM-L-6-v2'
)
    index = faiss.read_index("vector_index.faiss")
    with open("text_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    with open("bm25.pkl", "rb") as f:
        bm25 = pickle.load(f)

    return embedding_model, reranker, index, chunks, bm25

embedding_model, reranker, index, text_chunks, bm25 = load_backend()
# --- 3B. Intent Detection & Routing ---

GREETING_KEYWORDS = [
    "hi", "hello", "hey", "good morning",
    "good evening", "yo", "hola"
]

SMALL_TALK_KEYWORDS = [
    "how are you",
    "what can you do",
    "who are you",
    "thank you",
    "thanks"
]

CLARIFICATION_KEYWORDS = [
    "i don't understand",
    "i dont understand",
    "explain simpler",
    "simplify that",
    "say that again",
    "what do you mean",
    "can you explain again",
    "i am confused",
    "confusing"
]

AMBIGUOUS_KEYWORDS = [
    "delay",
    "timing",
    "power"
]

def normalize_query(query):
    return re.sub(r"\s+", " ", query.strip().lower())

def detect_intent(query):
    query = normalize_query(query)

    # Greeting Detection
    if any(word in query for word in GREETING_KEYWORDS):
        return "greeting"

    # Small Talk Detection
    for phrase in SMALL_TALK_KEYWORDS:
        if phrase in query:
            return "small_talk"
        
    # Clarification Detection
    for phrase in CLARIFICATION_KEYWORDS:
        if phrase in query:
            return "clarification"

    # Ambiguous Query Detection
    if query.startswith("explain") or query.startswith("what is"):
        for word in AMBIGUOUS_KEYWORDS:
            if word in query and len(query.split()) <= 3:
                return "ambiguous"

    # Default → Technical Query
    return "technical"
def detect_complexity(query):

    query = normalize_query(query)

    ADVANCED_KEYWORDS = [

        "timing",
        "pipeline",
        "flip-flop",
        "setup",
        "hold",
        "metastability",
        "clock skew",
        "synchronizer",
        "latch",
        "dynamic logic",
        "verilog",
        "power analysis",
        "noise margin",
        "propagation delay",
        "fanout",
        "critical path"
    ]

    long_query = len(query.split()) > 10

    advanced_present = any(
        word in query
        for word in ADVANCED_KEYWORDS
    )

    if long_query or advanced_present:
        return "complex"

    return "simple"
def is_followup(query):

    SHORT_FOLLOWUPS = [

        "why",
        "how",
        "what do you mean",
        "explain",
        "i don't understand",
        "why is that",
        "how so",
        "what",
        "can you explain"
    ]

    query = normalize_query(query)

    return (
        query in SHORT_FOLLOWUPS
    )

def is_valid_topic(query):

    weak_queries = [

        "why",
        "how",
        "what",
        "explain",
        "again",
        "i don't understand",
        "did not understand",
        "what do you mean",
        "huh",
        "okay",
        "yes"
    ]

    cleaned = query.lower().strip()

    if cleaned in weak_queries:
        return False

    if len(cleaned.split()) <= 2:
        return False

    return True

def reconstruct_followup_query(
    current_topic,
    followup_question
):

    prompt = f"""
    Current topic:
    {current_topic}

    Follow-up student question:
    {followup_question}

    Rewrite this into a clean standalone
    VLSI engineering question.

    Keep it concise and technically clear.

    Only return the rewritten question.
    """

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.0
        )

        rewritten = (
            completion
            .choices[0]
            .message
            .content
            .strip()
        )

        return rewritten

    except:

        return (
            current_topic
            + " "
            + followup_question
        )


# --- 4. The User Interface ---

# Step A: Draw all the PAST messages to the screen so it looks like a real chat app
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step B: Wait for a NEW question
user_question = st.chat_input("Ask a question about VLSI design...")

if (
    user_question and
    user_question != st.session_state.last_user_query
    ):
    # Immediately draw the user's new question on the screen
    with st.chat_message("user"):
        st.write(user_question)

    # --- Intent Detection ---
    intent = detect_intent(user_question)

    # --- Conversational Routing ---

    if intent == "greeting":
        answer = (
            "Hello! I'm your conversational VLSI and Digital Design tutor. "
            "You can ask me about CMOS, timing analysis, logic design, "
            "flip-flops, Verilog, and more."
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })
        st.session_state.last_user_query = user_question

        st.stop()

    elif intent == "small_talk":
        answer = (
            "I'm doing well! I can help explain VLSI and digital design concepts, "
            "answer textbook-based technical questions, and guide you through topics step-by-step."
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.stop()

    elif intent == "ambiguous":
        answer = (
            "Your question is a bit broad. Could you clarify what you mean?\n\n"
            "For example:\n"
            "- timing analysis\n"
            "- dynamic power\n"
            "- static power\n"
            "- clock delay"
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.stop()

    elif intent == "clarification":
            
        previous_answer = st.session_state.get(
                "last_assistant_response",
            ""
            )

        clarification_prompt = f"""
        You are continuing an ongoing tutoring conversation.

        You previously explained the following concept to the student:

        {previous_answer}

        The student still did not understand it.

        Re-explain the SAME idea:
        - more simply
        - more intuitively
        - more conversationally
        - using beginner-friendly wording
        - with at most one analogy

        Do NOT:
        - introduce new topics
        - mention books or reference material
        - ask the user what they mean
        - restart the conversation
        - sound like customer support

        Assume the student is asking about the SAME concept.

        Teach naturally like a patient engineering professor.
        """  

        try:

            clarification_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an experienced VLSI professor helping a beginner understand engineering concepts clearly and naturally."
                        )
                    },
                    {
                        "role": "user",
                        "content": clarification_prompt
                    }
                ],
                temperature=0.2,
            )

            answer = clarification_completion.choices[0].message.content

            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

            st.session_state.last_user_query = user_question
            st.stop()

        except Exception as e:

            st.error(f"Clarification Error: {e}")
    with st.spinner("Searching textbook vectors..."):

    # --- Conversational Query Rewriting ---
        rewritten_query = normalize_query(
    user_question
)
        followup = is_followup(user_question)

        if followup:

            rewritten_query = (
                reconstruct_followup_query(
                    st.session_state.current_topic,
                    user_question
                )
            )
        if is_valid_topic(rewritten_query):

            st.session_state.current_topic = rewritten_query

        print(f"\n[Rewritten Query]: {rewritten_query}")

    #--- Complexity Detection ---
        complexity = detect_complexity(
            rewritten_query
        )          

        # --- Embedding + Retrieval ---
        question_vector = embedding_model.encode(
            [rewritten_query]
            ).astype('float32')

        if complexity == "simple":

            retrieval_k = 2

        else:

            retrieval_k = 5

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
    )[:3]

    # --- Retrieve Structured Chunks ---
        # --- Hybrid Retrieval Merge ---

        combined_indices = list(indices[0]) + bm25_top_indices

    # Remove duplicates while preserving order
        unique_indices = list(dict.fromkeys(combined_indices))

    # --- Initial Hybrid Retrieval ---

        initial_chunks = [
        text_chunks[i]
        for i in unique_indices[:5]
    ]

# --- Prepare Query-Chunk Pairs for Reranking ---

        rerank_pairs = [
        (rewritten_query, chunk["text"])
        for chunk in initial_chunks
    ]

# --- Cross-Encoder Scoring ---

        rerank_scores = reranker.predict(rerank_pairs)

# --- Sort Chunks By Relevance ---

        scored_chunks = list(
    zip(rerank_scores, initial_chunks)
)

        scored_chunks.sort(
    key=lambda x: x[0],
    reverse=True
)

# --- Final Top Chunks After Reranking ---

        if complexity == "simple":

            final_chunk_count = 1

        else:

            final_chunk_count = 2

        retrieved_chunks = [
            chunk
            for score, chunk in scored_chunks[:final_chunk_count]
        ]   

    # --- Build Context ---
        context_text = ""

        for i, chunk in enumerate(retrieved_chunks):

            chunk_text = chunk["text"]
            chunk_source = chunk["metadata"]["source"]

            context_text += (
    f"{chunk_text}\n\n"
)
    # --- Prompt Construction ---
        learning_profile = st.session_state.learning_profile
        messages = [
        {
            "role": "system",
            "content": (

        "You are an experienced VLSI and Digital Design tutor helping engineering students learn concepts clearly and intuitively. "

        "Avoid phrases like 'let's break this down', "
        "'now let's talk about', "
        "'or similar tutoring narration.' "

        "Start explanations directly. "

        f"Student skill level: {learning_profile['skill_level']}. "

        f"Previously confusing topics: "
        f"{', '.join(learning_profile['confused_topics'])}. "

        f"Preferred teaching style: "
        f"{learning_profile['preferred_style']}. "

        f"Current question complexity: {complexity}. "

        "If the question is simple, give a short intuitive explanation first. "

        "If the question is complex, provide a more structured technical explanation with deeper reasoning. "

        "Teach naturally like a patient human professor or mentor, not like an AI assistant or textbook summarizer. "

        f"Current active topic: {st.session_state.current_topic}. "
        "When the student asks short follow-up questions like "
        "'why?', 'how?', 'what do you mean?', or 'i don't understand', "
        "interpret them relative to the current active topic. "

        "Use the provided textbook knowledge only as supporting reference material internally. "
        "Never mention textbooks, excerpts, retrieved chunks, passages, or context. "

        "Avoid phrases like 'let's break this down', 'the text says', "
        "'this excerpt discusses', or similar assistant-style wording. "

        "For beginner students, prioritize intuition, clarity, and simple explanations before formal technical detail. "

        "Start with the core idea first, then gradually add deeper explanation only if needed. "

        "Keep explanations concise, focused, and conversational. "
        "Do not introduce unrelated advanced topics unless explicitly asked. "

        "When answering follow-up or clarification questions, stay focused on the previously discussed concept unless the topic changes explicitly. "

        "Use analogies sparingly and only when they significantly improve intuition."   
        "Avoid oversimplifications that become technically incorrect. "

        "When explaining technical concepts:\n"

        "- Begin with intuitive understanding.\n"
        "- Then provide technical explanation.\n"
        "- Keep explanations structured and easy to follow.\n"
        "- Avoid unnecessary jargon and excessive detail.\n"
        "- Use bullet points only when useful.\n"

        "If a question is ambiguous, ask a short clarifying question before answering. "

        "Maintain technical accuracy while remaining approachable and conversational. "

        "Format equations in LaTeX using $ for inline equations and $$ for block equations."
    )
}    
    ]
        if st.session_state.current_topic:

            messages.append({
                "role": "system",
                "content": (
                    "Current ongoing engineering topic: "
                    f"{st.session_state.current_topic}"
            )
        })
    # --- Add Current Query ---
        messages.append({
        "role": "user",
        "content": (
            f"REFERENCE KNOWLEDGE:\n{context_text}\n\n"
            f"USER QUESTION: {user_question}"
        )
    })

    # --- Generate Response ---
        try:

            chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.2,
        )

            answer = chat_completion.choices[0].message.content
            st.session_state.last_assistant_response = answer

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
        })

            st.session_state.chat_history.append(
    {
        "role": "assistant",
        "content": answer
    }
) 
            st.session_state.last_topic = rewritten_query
            st.session_state.last_user_query = user_question

        # --- Display Response ---
            with st.chat_message("assistant"):
                st.markdown(answer)

        except Exception as e:

            st.error(f"API Error: {e}")