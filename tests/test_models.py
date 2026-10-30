from workout_generator.models import WorkoutPreferences


def test_workout_preferences():
    preferences = WorkoutPreferences(
        fitness_goal="weight_loss",
        difficulty_level="beginner",
        days_per_week=3,
        duration_minutes=30,
        injuries="none",
        equipment="dumbbells",
    )
    assert preferences.fitness_goal == "weight_loss"
    assert preferences.difficulty_level == "beginner"
    assert preferences.days_per_week == 3
    assert preferences.duration_minutes == 30
    assert preferences.injuries == "none"
    assert preferences.equipment == "dumbbells"



    
    