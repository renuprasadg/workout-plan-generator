from types import SimpleNamespace
from unittest.mock import patch

import httpx
import pytest
from groq import APIConnectionError

from workout_generator.llm_client import generate_workout_plan

SYSTEM_PROMPT = "You are a fitness assistant."
USER_PROMPT = "Create a three-day workout plan."


def mock_completion(content: str):
    """Create a fake Groq completion response."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


def test_generate_workout_plan_success(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    with patch("workout_generator.llm_client.Groq") as mock_groq:
        mock_client = mock_groq.return_value
        mock_client.chat.completions.create.return_value = mock_completion(
            "Day 1: Walking"
        )

        result = generate_workout_plan(
            SYSTEM_PROMPT,
            USER_PROMPT,
        )

        assert result == "Day 1: Walking"
        mock_client.chat.completions.create.assert_called_once()


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with (
        patch("workout_generator.llm_client.load_dotenv"),
        pytest.raises(ValueError, match="GROQ_API_KEY"),
    ):
        generate_workout_plan(
            SYSTEM_PROMPT,
            USER_PROMPT,
        )


def test_empty_response(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    with patch("workout_generator.llm_client.Groq") as mock_groq:
        mock_client = mock_groq.return_value
        mock_client.chat.completions.create.return_value = mock_completion("")

        with pytest.raises(ValueError, match="empty workout plan"):
            generate_workout_plan(
                SYSTEM_PROMPT,
                USER_PROMPT,
            )


def test_no_choices(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    with patch("workout_generator.llm_client.Groq") as mock_groq:
        mock_client = mock_groq.return_value
        mock_client.chat.completions.create.return_value = SimpleNamespace(choices=[])

        with pytest.raises(ValueError, match="no response"):
            generate_workout_plan(
                SYSTEM_PROMPT,
                USER_PROMPT,
            )


def test_api_connection_failure(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    with patch("workout_generator.llm_client.Groq") as mock_groq:
        mock_client = mock_groq.return_value

        mock_client.chat.completions.create.side_effect = APIConnectionError(
            request=httpx.Request(
                "POST",
                "https://api.groq.com/openai/v1/chat/completions",
            )
        )

        with pytest.raises(RuntimeError, match="Unable to generate"):
            generate_workout_plan(
                SYSTEM_PROMPT,
                USER_PROMPT,
            )
