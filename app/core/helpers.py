import os

from groq import Groq

from dotenv import load_dotenv

from app.config.settings import (
    LLM_MODEL,
    QUERY_REWRITE_TEMPERATURE
)

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

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

            model=LLM_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=QUERY_REWRITE_TEMPERATURE
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