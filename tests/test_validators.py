import pytest

from workout_generator.models import WorkoutPreferences
from workout_generator.validators import validate_preferences


def test_valid_preferences():
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        duration_minutes=30,
        injuries="",
    )

    errors = validate_preferences(preferences)

    assert errors == []


def test_invalid_fitness_goal():
    preferences = WorkoutPreferences(
        fitness_goal="sleep",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
    )

    errors = validate_preferences(preferences)

    assert "Invalid fitness goal" in errors


def test_invalid_difficulty_level():
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="expert",
        equipment="no_equipment",
        days_per_week=3,
    )

    errors = validate_preferences(preferences)

    assert "Invalid difficulty level" in errors


def test_invalid_equipment():
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="spaceship",
        days_per_week=3,
    )

    errors = validate_preferences(preferences)

    assert "Invalid equipment selection" in errors


@pytest.mark.parametrize("days", [0, 8, -1, 10, "three", True])
def test_invalid_workout_days(days):
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=days,
    )

    errors = validate_preferences(preferences)

    assert "Days per week must be between 1 and 7" in errors


@pytest.mark.parametrize("days", [1, 3, 7])
def test_valid_workout_days(days):
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=days,
    )

    assert validate_preferences(preferences) == []


@pytest.mark.parametrize("duration", [0, 10, 121, -30, "sixty", True])
def test_invalid_duration(duration):
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        duration_minutes=duration,
    )

    errors = validate_preferences(preferences)

    assert "Workout duration must be between 15 and 120 minutes" in errors


@pytest.mark.parametrize("duration", [None, 15, 30, 120])
def test_valid_duration(duration):
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        duration_minutes=duration,
    )

    assert validate_preferences(preferences) == []


def test_invalid_injuries():
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        injuries=123,
    )

    errors = validate_preferences(preferences)

    assert "Injuries or limitations must be text" in errors


def test_multiple_validation_errors():
    preferences = WorkoutPreferences(
        fitness_goal="sleep",
        difficulty_level="expert",
        equipment="spaceship",
        days_per_week=10,
        duration_minutes=200,
    )

    errors = validate_preferences(preferences)

    assert len(errors) == 5
    assert "Invalid fitness goal" in errors
    assert "Invalid difficulty level" in errors
    assert "Invalid equipment selection" in errors
