import re
# --- Intent Detection & Routing ---

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
    query_words = query.split()

    if any(word in query_words for word in GREETING_KEYWORDS):
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