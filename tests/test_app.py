
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def test_app_loads_successfully():
    at = AppTest.from_file(str(APP_PATH)).run()

    assert not at.exception
    assert len(at.selectbox) == 3
    assert len(at.form_submit_button) == 1


def test_default_inputs():
    at = AppTest.from_file(str(APP_PATH)).run()

    assert at.selectbox[0].value == "build_muscle"
    assert at.selectbox[1].value == "beginner"
    assert at.selectbox[2].value == "no_equipment"
    assert at.slider[0].value == 3

    assert not at.exception


def test_generate_workout_plan():
    with patch(
        "workout_generator.service.create_workout_plan",
        return_value="## Day 1 - Full Body Workout",
    ) as mock_service:
        at = AppTest.from_file(str(APP_PATH)).run()

        at.selectbox[0].set_value("lose_fat")
        at.selectbox[1].set_value("intermediate")
        at.slider[0].set_value(4)

        at.form_submit_button[0].click().run()

        assert not at.exception
        mock_service.assert_called_once()

        preferences = mock_service.call_args.args[0]

        assert preferences.fitness_goal == "lose_fat"
        assert preferences.difficulty_level == "intermediate"
        assert preferences.days_per_week == 4
        assert preferences.equipment == "no_equipment"

        assert at.session_state["workout_plan"] == (
            "## Day 1 - Full Body Workout"
        )


def test_api_failure_displays_error():
    with patch(
        "workout_generator.service.create_workout_plan",
        side_effect=RuntimeError("Groq API unavailable"),
    ):
        at = AppTest.from_file(str(APP_PATH)).run()

        at.form_submit_button[0].click().run()

        assert not at.exception
        assert len(at.error) == 1
        assert "Unable to generate" in at.error[0].value
        assert at.session_state["workout_plan"] == ""
