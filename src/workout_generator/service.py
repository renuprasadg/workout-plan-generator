from workout_generator.llm_client import generate_workout_plan
from workout_generator.models import WorkoutPreferences
from workout_generator.prompts import build_system_prompt, build_user_prompt
from workout_generator.validators import validate_preferences


def create_workout_plan(preferences: WorkoutPreferences) -> str:
    """Validate preferences and generate a workout plan."""

    errors = validate_preferences(preferences)

    if errors:
        raise ValueError("; ".join(errors))

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(preferences)

    return generate_workout_plan(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
