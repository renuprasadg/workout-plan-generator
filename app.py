
import streamlit as st

from workout_generator.models import WorkoutPreferences
from workout_generator.service import create_workout_plan


st.set_page_config(
    page_title="AI Workout Plan Generator",
    page_icon="💪",
    layout="centered",
)

st.title("💪 AI Workout Plan Generator")

st.write(
    "Generate a personalised weekly workout plan "
    "based on your fitness goals and preferences."
)

# Initialise session state
if "workout_plan" not in st.session_state:
    st.session_state["workout_plan"] = ""


# Collect user preferences
with st.form("workout_form"):

    fitness_goal = st.selectbox(
        "Fitness Goal",
        options=[
            "build_muscle",
            "lose_fat",
            "general_fitness",
            "improve_endurance",
        ],
        format_func=lambda value: value.replace("_", " ").title(),
    )

    difficulty_level = st.selectbox(
        "Experience Level",
        options=[
            "beginner",
            "intermediate",
            "advanced",
        ],
        format_func=lambda value: value.title(),
    )

    equipment = st.selectbox(
        "Equipment Available",
        options=[
            "no_equipment",
            "home_dumbbells",
            "full_gym",
        ],
        format_func=lambda value: value.replace("_", " ").title(),
    )

    days_per_week = st.slider(
        "Workout Days Per Week",
        min_value=1,
        max_value=7,
        value=3,
    )

    include_duration = st.checkbox(
        "Specify workout duration",
        value=True,
    )

    duration_minutes = None

    if include_duration:
        duration_minutes = st.slider(
            "Workout Duration (Minutes)",
            min_value=15,
            max_value=120,
            value=30,
            step=5,
        )

    injuries = st.text_area(
        "Injuries or Physical Limitations (Optional)",
        placeholder="e.g. Avoid overhead pressing",
    )

    submitted = st.form_submit_button(
        "Generate Workout Plan",
        use_container_width=True,
    )


# Handle form submission
if submitted:

    preferences = WorkoutPreferences(
        fitness_goal=fitness_goal,
        difficulty_level=difficulty_level,
        equipment=equipment,
        days_per_week=days_per_week,
        duration_minutes=duration_minutes,
        injuries=injuries,
    )

    # Clear the previous plan
    st.session_state["workout_plan"] = ""

    try:
        with st.spinner("Generating your workout plan..."):
            plan = create_workout_plan(preferences)

        st.session_state["workout_plan"] = plan

    except ValueError as exc:
        st.error(str(exc))

    except RuntimeError:
        st.error(
            "Unable to generate your workout plan. "
            "Please try again later."
        )


# Display generated plan
if st.session_state["workout_plan"]:

    st.divider()

    st.subheader("Your Personalised Workout Plan")

    st.markdown(st.session_state["workout_plan"])

    st.download_button(
        label="Download Workout Plan",
        data=st.session_state["workout_plan"],
        file_name="workout_plan.md",
        mime="text/markdown",
    )


st.divider()

st.caption(
    "This application provides general fitness information "
    "and is not a substitute for professional medical advice."
)
