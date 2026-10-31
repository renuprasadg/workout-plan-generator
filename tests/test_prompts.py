from workout_generator.models import WorkoutPreferences
from workout_generator.prompts import build_system_prompt, build_user_prompt


def test_system_prompt():
    prompt = build_system_prompt()

    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "equipment" in prompt.lower()


def test_user_prompt():
    preferences = WorkoutPreferences(
        fitness_goal="lose_fat",
        difficulty_level="beginner",
        equipment="no_equipment",
        days_per_week=3,
        duration_minutes=30,
        injuries="knee discomfort",
    )

    prompt = build_user_prompt(preferences)

    assert "lose_fat" in prompt
    assert "beginner" in prompt
    assert "no_equipment" in prompt
    assert "3" in prompt
    assert "30 minutes" in prompt
    assert "knee discomfort" in prompt
