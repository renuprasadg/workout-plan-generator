import os

from dotenv import load_dotenv
from groq import APIError, Groq

load_dotenv()


def generate_workout_plan(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Generate a workout plan using Groq."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured")

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    try:
        client = Groq(api_key=api_key, timeout=30.0)

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_completion_tokens=2500,
        )

        if not completion.choices:
            raise ValueError("LLM returned no response")

        plan = completion.choices[0].message.content

        if not plan or not plan.strip():
            raise ValueError("LLM returned an empty workout plan")

        return plan.strip()

    except APIError as exc:
        raise RuntimeError(
            "Unable to generate a workout plan. Please try again."
        ) from exc
