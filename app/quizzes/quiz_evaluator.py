from groq import Groq

from dotenv import load_dotenv

from app.config.settings import (
    LLM_MODEL
)

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_answer(
    topic,
    question,
    student_answer
):

    prompt = f"""
    You are evaluating a beginner engineering student.

    Topic:
    {topic}

    Question:
    {question}

    Student Answer:
    {student_answer}

    Evaluate:
    1. Conceptual correctness
    2. Missing understanding
    3. Misconceptions
    4. Confidence level

    Then:
    - Give short constructive feedback
    - Explain what the student missed
    - Keep tone supportive and educational
    """

    completion = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4
    )

    return (
        completion
        .choices[0]
        .message
        .content
    )