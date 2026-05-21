# README.md

# Conversational VLSI RAG Tutor

An AI-powered conversational tutoring system for VLSI and Digital Design education using Retrieval-Augmented Generation (RAG), hybrid retrieval pipelines, semantic topic memory, and conversational orchestration.

---

## Project Overview

This project was developed to move beyond traditional:

```text
PDF → Embeddings → Chatbot
````

architectures and build a more realistic engineering tutoring assistant capable of:

* Explaining VLSI and Digital Design concepts conversationally
* Handling follow-up engineering questions
* Maintaining topic continuity
* Simplifying explanations dynamically
* Reducing conversational drift
* Delivering beginner-friendly tutoring responses

The system combines:

* FAISS vector retrieval
* BM25 sparse retrieval
* Cross-encoder reranking
* Conversational query reconstruction
* Semantic topic memory
* Clarification-oriented orchestration

---

## Features

### Hybrid Retrieval Pipeline

The chatbot uses:

* Dense retrieval using SentenceTransformers + FAISS
* Sparse keyword retrieval using BM25
* Cross-encoder reranking for improved relevance

---

### Conversational Query Reconstruction

Short follow-up queries like:

```text
why?
how?
what do you mean?
```

are reconstructed into standalone technical questions.

Example:

```text
User: why does that happen?
↓
Rewritten Query:
Why does metastability occur in flip-flops?
```

---

### Semantic Topic Memory

Instead of replaying raw chat history, the system maintains:

* Current engineering topic
* Confused topics
* Student skill level
* Preferred teaching style

This reduces:

* conversational drift
* recursive hallucination loops
* clarification instability

---

### Clarification-Oriented Tutoring

When the student says:

```text
I don't understand
```

The chatbot:

* avoids re-running retrieval
* avoids semantic drift
* simplifies the previous explanation directly
* re-teaches the same concept more intuitively

---

### Beginner-Friendly Pedagogy

The tutoring pipeline was optimized to:

* explain concepts intuitively first
* use analogies sparingly
* avoid textbook-style narration
* progressively deepen explanations
* maintain conversational flow

---

## Tech Stack

| Component        | Technology                           |
| ---------------- | ------------------------------------ |
| Frontend         | Streamlit                            |
| LLM API          | Groq API                             |
| LLM Model        | Llama 3.3 70B Versatile              |
| Embeddings       | all-MiniLM-L6-v2                     |
| Vector Database  | FAISS                                |
| Sparse Retrieval | BM25                                 |
| Reranker         | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Backend          | Python                               |

---

## System Architecture

```text
User Question
      ↓
Intent Detection
      ↓
Query Reconstruction
      ↓
Complexity Detection
      ↓
Hybrid Retrieval
(FAISS + BM25)
      ↓
Cross-Encoder Reranking
      ↓
Context Construction
      ↓
Conversational Tutoring Prompt
      ↓
LLM Response Generation
      ↓
Semantic Topic Memory Update
```

---

## Engineering Challenges Solved

### Retrieval Drift

Solved using:

* semantic query reconstruction
* topic-aware orchestration

---

### Recursive Conversational Contamination

Solved by:

* removing raw chat replay memory
* replacing it with semantic topic memory

---

### Clarification Failure

Solved using:

* clarification-specific orchestration
* previous-answer pedagogical refinement

---

### Over-Retrieval

Solved using:

* complexity-aware retrieval depth
* reranking-based filtering

---

## Current Limitations

Current limitations include:

* No long-term learner memory
* No evaluation benchmark suite
* No multimodal diagram understanding
* No voice tutoring
* No deployment-scale optimization
* No automated hallucination testing

---

## Future Improvements

### Planned Improvements

* Personalized learner modeling
* Adaptive explanation depth
* Circuit diagram understanding
* Verilog analysis
* Timing waveform explanation
* Retrieval evaluation benchmarks
* Multimodal tutoring
* Streaming responses
* Better UI/UX

---

## Why This Project Is Different

Most beginner RAG projects stop at:

```text
PDF → Embeddings → Chatbot
```

This project additionally explores:

* conversational orchestration
* semantic tutoring memory
* clarification routing
* pedagogical refinement
* tutoring-oriented AI behavior

The focus is not only on retrieval quality, but also on:

```text
how an AI system teaches engineering concepts conversationally
```

---

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Author

Built as an exploratory conversational AI tutoring system for:

* VLSI Design
* Digital Design
* Conversational Educational AI
* RAG System Orchestration



