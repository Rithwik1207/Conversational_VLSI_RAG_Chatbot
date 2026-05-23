import streamlit as st
from app.quizzes.quiz_generator import (
    generate_quiz
)

from app.quizzes.quiz_evaluator import (
    evaluate_answer
)

def initialize_quiz(current_course_topic):

    if not st.session_state.quiz_questions:

        quiz = generate_quiz(
            current_course_topic
        )

        st.session_state.quiz_questions = quiz

        st.session_state.quiz_answers = {}

        st.session_state.quiz_feedback = []

        st.session_state.quiz_submitted = False

def render_quiz_ui(current_course_topic):
    # =========================
    # Persistent Quiz UI
    # =========================

    if st.session_state.quiz_questions:

        st.divider()

        st.subheader("🧠 Quick Knowledge Check")

        for i, question in enumerate(
            st.session_state.quiz_questions
        ):

            st.markdown(question)

            answer = st.text_area(

                f"✍ Your Answer {i+1}",

                value=st.session_state.quiz_answers.get(i, ""),

                key=f"quiz_box_{i}"
            )

            st.session_state.quiz_answers[i] = answer


        if st.button(
            "✅ Evaluate My Understanding",
            key="evaluate_quiz"
        ):

            feedback_results = []

            for i, question in enumerate(
                st.session_state.quiz_questions
            ):

                student_answer = (
                    st.session_state.quiz_answers.get(i, "")
                )

                feedback = evaluate_answer(

                    current_course_topic,

                    question,

                    student_answer
                )

                feedback_results.append(feedback)

            st.session_state.quiz_feedback = (
                feedback_results
            )

            st.session_state.quiz_submitted = True

            feedback_text = (
                "# 📘 Evaluation Feedback\n\n"
            )

            for i, feedback in enumerate(
                feedback_results
            ):

                feedback_text += (
                    f"## Feedback for Question {i+1}\n\n"
                    f"{feedback}\n\n"
                )

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": feedback_text
            })

            st.session_state.quiz_questions = []

            st.session_state.quiz_answers = {}

            st.session_state.quiz_submitted = False

            st.rerun()


        if st.session_state.quiz_submitted:

            st.divider()

            st.subheader("📘 Evaluation Feedback")

            for i, feedback in enumerate(
                st.session_state.quiz_feedback
            ):

                st.markdown(
                    f"### Feedback for Question {i+1}"
                )

                st.markdown(feedback)

                st.divider()