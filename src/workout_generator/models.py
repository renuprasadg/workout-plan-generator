from dataclasses import dataclass


@dataclass
class WorkoutPreferences:
    fitness_goal: str
    difficulty_level: str
    equipment: str
    days_per_week: int
    duration_minutes: int | None = None
    injuries: str = ""
    