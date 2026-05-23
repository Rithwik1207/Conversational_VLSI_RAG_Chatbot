import streamlit as st

from app.tutoring.course_manager import (
    get_current_topic,
    advance_topic
)


def render_course_ui():

    current_course_topic = get_current_topic(
        st.session_state.course_progress
    )

    st.markdown(
        f"## 📘 Lesson "
        f"{st.session_state.course_progress + 1}"
    )

    st.info(
        f"Current Topic: {current_course_topic}"
    )

    progress_value = (
        st.session_state.course_progress + 1
    ) / 10

    st.progress(progress_value)

    st.divider()

    teach_clicked = st.button(
        "▸ Teach This Topic",
        key="teach_topic"
    )

    next_topic_clicked = st.button(
        "➡ Next Topic",
        key="next_topic"
    )

    if next_topic_clicked:

        if (
            st.session_state.quiz_questions and
            not st.session_state.quiz_submitted
        ):

            st.warning(
                "Please complete the quiz before moving "
                "to the next lesson."
            )

            st.stop()

        st.session_state.quiz_questions = []

        st.session_state.quiz_answers = {}

        st.session_state.quiz_feedback = []

        st.session_state.quiz_submitted = False

        st.session_state.course_progress = (
            advance_topic(
                st.session_state.course_progress
            )
        )

        st.rerun()

    return (
        teach_clicked,
        current_course_topic
    )