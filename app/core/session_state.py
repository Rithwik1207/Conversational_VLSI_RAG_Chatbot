import streamlit as st


def initialize_session_state():

    defaults = {

        "chat_history": [],

        "last_user_query": "",

        "learning_profile": {

            "skill_level": "beginner",

            "confused_topics": [],

            "explained_topics": [],

            "preferred_style": "analogies"
            
        },

        "current_topic": "",

        "course_mode": False,

        "course_progress": 0,

        "pending_course_query": None,

        "quiz_feedback": [],

        "quiz_questions": [],

        "quiz_answers": {},

        "quiz_submitted": False,

        "is_course_generation": False
        
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value