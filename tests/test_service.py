from unittest.mock import patch

import pytest

from workout_generator.models import WorkoutPreferences
from workout_generator.service import create_workout_plan


def valid_preferences() -> WorkoutPreferences:
    return WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        duration_minutes=30,
        injuries="",
    )


def test_create_workout_plan_success():
    preferences = valid_preferences()

    with patch("workout_generator.service.generate_workout_plan") as mock_generate:
        mock_generate.return_value = "Day 1: Walking"

        result = create_workout_plan(preferences)

        assert result == "Day 1: Walking"
        mock_generate.assert_called_once()


def test_invalid_preferences():
    preferences = valid_preferences()
    preferences.days_per_week = 10

    with patch("workout_generator.service.generate_workout_plan") as mock_generate:
        with pytest.raises(ValueError, match="Days per week"):
            create_workout_plan(preferences)

        mock_generate.assert_not_called()


def test_multiple_validation_errors():
    preferences = valid_preferences()
    preferences.fitness_goal = "sleep"
    preferences.days_per_week = 10

    with pytest.raises(ValueError) as exc_info:
        create_workout_plan(preferences)

    error_message = str(exc_info.value)

    assert "Invalid fitness goal" in error_message
    assert "Days per week" in error_message


def test_groq_error_propagation():
    preferences = valid_preferences()

    with patch("workout_generator.service.generate_workout_plan") as mock_generate:
        mock_generate.side_effect = RuntimeError("Unable to generate a workout plan")

        with pytest.raises(RuntimeError, match="Unable to generate"):
            create_workout_plan(preferences)


def test_prompts_passed_to_groq():
    preferences = valid_preferences()

    with patch("workout_generator.service.generate_workout_plan") as mock_generate:
        mock_generate.return_value = "Workout plan"

        create_workout_plan(preferences)

        mock_generate.assert_called_once()

        _, kwargs = mock_generate.call_args

        assert "fitness" in kwargs["system_prompt"].lower()
        assert "lose_fat" in kwargs["user_prompt"]
        assert "beginner" in kwargs["user_prompt"]
        assert "no_equipment" in kwargs["user_prompt"]
