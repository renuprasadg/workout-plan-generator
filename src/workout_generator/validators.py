from workout_generator.models import WorkoutPreferences

VALID_GOALS = {
    "build_muscle",
    "lose_fat",
    "general_fitness",
    "improve_endurance",
}

VALID_LEVELS = {
    "beginner",
    "intermediate",
    "advanced",
}

VALID_EQUIPMENT = {
    "no_equipment",
    "home_dumbbells",
    "full_gym",
}


def validate_preferences(preferences: WorkoutPreferences) -> list[str]:
    """Validate workout preferences and return a list of errors."""

    errors: list[str] = []

    # Validate fitness goal
    if (
        not isinstance(preferences.fitness_goal, str)
        or preferences.fitness_goal not in VALID_GOALS
    ):
        errors.append("Invalid fitness goal")

    # Validate difficulty level
    if (
        not isinstance(preferences.difficulty_level, str)
        or preferences.difficulty_level not in VALID_LEVELS
    ):
        errors.append("Invalid difficulty level")

    # Validate equipment
    if (
        not isinstance(preferences.equipment, str)
        or preferences.equipment not in VALID_EQUIPMENT
    ):
        errors.append("Invalid equipment selection")

    # Validate workout days
    if (
        type(preferences.days_per_week) is not int
        or not 1 <= preferences.days_per_week <= 7
    ):
        errors.append("Days per week must be between 1 and 7")

    # Validate optional workout duration
    if preferences.duration_minutes is not None and (
        type(preferences.duration_minutes) is not int
        or not 15 <= preferences.duration_minutes <= 120
    ):
        errors.append("Workout duration must be between 15 and 120 minutes")
    # Validate optional injuries
    if not isinstance(preferences.injuries, str):
        errors.append("Injuries or limitations must be text")

    return errors
