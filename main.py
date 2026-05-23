import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from app.retrieval.hybrid_search import retrieve_context
from app.tutoring.intent_router import (
    normalize_query,
    detect_intent,
    detect_complexity,
    is_followup,
    is_valid_topic
    )
from app.tutoring.prompts import (
    build_clarification_prompt,
    build_system_prompt
    )
from app.config.settings import (
    PAGE_TITLE,
    APP_TITLE,
    LLM_MODEL,
    LLM_TEMPERATURE,
    CLARIFICATION_TEMPERATURE,
    QUERY_REWRITE_TEMPERATURE
    )
from app.tutoring.course_manager import (
    get_current_topic,
    )
from app.tutoring.visual_retriever import (
    retrieve_visuals
    )
from app.quizzes.quiz_generator import (
    generate_quiz
    )
from app.ui.quiz_ui import (
    render_quiz_ui,
    initialize_quiz
    )
from app.ui.course_ui import (
    render_course_ui
    )
from app.core.session_state import (
    initialize_session_state
    )
from app.retrieval.retrieval_pipeline import (
    execute_retrieval_pipeline
    )
from app.core.helpers import (
    reconstruct_followup_query
    )

# --- 1. System Initialization ---
load_dotenv()
st.set_page_config(page_title=PAGE_TITLE, layout="centered")
st.title(APP_TITLE)

if st.button("📘 Start Digital Electronics Course"):
    st.session_state.course_mode = True
    st.session_state.course_progress = 0

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- Initialize Session State ---

initialize_session_state()   

# --- 4. The User Interface ---

user_question = (
    st.session_state.pending_course_query
)

# Step A: Draw all previous messages

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

current_course_topic = None     

# --- Course Mode UI ---

if st.session_state.course_mode:

    (
        teach_clicked,
        current_course_topic
    ) = render_course_ui()

    if teach_clicked:

        st.session_state.is_course_generation = True

        st.session_state.pending_course_query = (

            f"Teach me {current_course_topic} "
            f"from beginner level with intuition, "
            f"examples, and engineering explanation."
        )

        st.rerun()

# Step B: Wait for a NEW question
manual_question = st.chat_input(
    "Ask a question about VLSI design..."
)

if manual_question:
    user_question = manual_question

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
        st.session_state.pending_course_query = None

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

        try:
            clarification_prompt = build_clarification_prompt(
                previous_answer,
                user_question
            )

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
                temperature=CLARIFICATION_TEMPERATURE
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
        pipeline_result = (
            execute_retrieval_pipeline(

                user_question,

                reconstruct_followup_query,

                st.session_state.current_topic
            )
        )

        rewritten_query = (
            pipeline_result["rewritten_query"]
        )

        complexity = (
            pipeline_result["complexity"]
        )

        context_text = (
            pipeline_result["context_text"]
        )

        st.session_state.current_topic = (
            pipeline_result["current_topic"]
        )
        
            # --- Prompt Construction ---

        learning_profile = (
            st.session_state.learning_profile
        )

        messages = [
            {
                "role": "system",
                "content": (
                    build_system_prompt(
                        learning_profile,
                        complexity,
                        st.session_state.current_topic
                    )
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
            temperature=LLM_TEMPERATURE,
        )

            answer = chat_completion.choices[0].message.content
            st.session_state.last_assistant_response = answer

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })
            st.session_state.last_topic = rewritten_query
            st.session_state.last_user_query = user_question
            st.session_state.pending_course_query = None

        # --- Display Response ---
            with st.chat_message("assistant"):
                st.markdown(answer)

                visuals = retrieve_visuals(user_question)

                for visual in visuals:

                    st.image(
                        visual,
                        use_container_width=True
                    )
                st.divider()
                
                if st.session_state.is_course_generation:

                    initialize_quiz(current_course_topic)

                    st.session_state.is_course_generation = False

        except Exception as e:

            st.error(f"API Error: {e}")

# =========================
# Persistent Quiz Renderer
# =========================

if (

    st.session_state.course_mode and

    st.session_state.quiz_questions

    ):

    current_course_topic = get_current_topic(
        st.session_state.course_progress
    )

    render_quiz_ui(current_course_topic)

    
