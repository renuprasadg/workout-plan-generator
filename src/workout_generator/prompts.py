from workout_generator.models import WorkoutPreferences


def build_system_prompt() -> str:
    return """
You are a fitness planning assistant who creates practical,
structured weekly workout plans.

Follow these rules:

1. Generate exactly the number of workout days requested.
2. Match exercises to the user's experience level.
3. Only recommend exercises compatible with the available equipment.
4. Respect the user's stated injuries and physical limitations.
   Do not recommend exercises that clearly conflict with them.
5. Include a warm-up, exercises, sets, repetitions or duration,
   rest periods, and a cool-down for each workout day.
6. Respect the requested workout duration when provided.
7. Include recovery or rest-day guidance where appropriate.
8. Present the workout plan in clear Markdown with headings
   for each workout day.
9. Do not make medical diagnoses or guarantee that exercises
   are safe for a particular injury.
10. If injuries or limitations are mentioned, add a short disclaimer
    advising the user to seek appropriate professional guidance.

Provide a realistic and actionable plan.
Avoid unnecessary explanations and generic advice.
""".strip()


def build_user_prompt(preferences: WorkoutPreferences) -> str:
    duration = (
        f"{preferences.duration_minutes} minutes"
        if preferences.duration_minutes is not None
        else "Not specified"
    )

    injuries = preferences.injuries.strip() or "None reported"

    return f"""
Generate a personalised weekly workout plan using these preferences:

Fitness goal: {preferences.fitness_goal}
Experience level: {preferences.difficulty_level}
Days available per week: {preferences.days_per_week}
Available equipment: {preferences.equipment}
Workout duration: {duration}
Injuries or limitations: {injuries}

Generate exactly {preferences.days_per_week} workout days.
Do not recommend equipment outside the user's available equipment.
Use a clear day-by-day Markdown format.
""".strip()