from groq import Groq

from app.config.settings import (
    LLM_MODEL
)

from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_quiz(topic):

    prompt = f"""
    Generate 3 beginner-friendly conceptual quiz questions
    for the topic:

    {topic}

    Rules:
    - Questions should test conceptual understanding
    - Avoid overly theoretical or memorization-based questions
    - Keep questions concise
    - Focus on intuition and engineering understanding
    - Return only the questions
    """

    completion = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5
    )

    quiz_text = (
    completion
    .choices[0]
    .message
    .content
    )

    questions = [

    q.strip()

    for q in quiz_text.split("\n")

    if q.strip()
    ]

    return questions