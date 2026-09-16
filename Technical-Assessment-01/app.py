"""Streamlit interface for the student performance risk classifier."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_risk_pipeline.joblib"
FEATURES = ["attendance", "quiz_score", "assignment_score", "exam_score"]


st.set_page_config(
    page_title="Student Performance Risk Check",
    page_icon="🎓",
    layout="centered",
)


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "The trained pipeline is missing. Run `python train_model.py` first."
        )
    return joblib.load(MODEL_PATH)


st.title("Student Performance Risk Check")
st.write(
    "Enter the four academic indicators below. The model provides an early-support "
    "signal, not a final judgment about a student."
)

with st.form("prediction_form"):
    attendance = st.number_input(
        "Attendance", min_value=0.0, max_value=100.0, value=72.0, step=1.0
    )
    quiz_score = st.number_input(
        "Quiz score", min_value=0.0, max_value=100.0, value=66.0, step=1.0
    )
    assignment_score = st.number_input(
        "Assignment score", min_value=0.0, max_value=100.0, value=68.0, step=1.0
    )
    exam_score = st.number_input(
        "Examination score", min_value=0.0, max_value=100.0, value=63.0, step=1.0
    )
    submitted = st.form_submit_button("Predict", use_container_width=True)

if submitted:
    values = [attendance, quiz_score, assignment_score, exam_score]
    if any(value < 0 or value > 100 for value in values):
        st.error("Every input must be between 0 and 100.")
    else:
        model = load_model()
        sample = pd.DataFrame([values], columns=FEATURES)
        prediction = str(model.predict(sample)[0])
        probabilities = model.predict_proba(sample)[0]
        probability_by_class = dict(zip(model.classes_, probabilities))
        at_risk_probability = float(probability_by_class.get("At Risk", 0.0))

        if prediction == "At Risk":
            st.error("Prediction: At Risk")
        else:
            st.success("Prediction: Not At Risk")
        st.metric("Estimated At Risk probability", f"{at_risk_probability:.1%}")
        st.warning(
            "Human review is required. A teacher should check the student's complete "
            "record, speak with the student, and consider relevant circumstances "
            "before taking supportive action."
        )

with st.expander("About this classroom model"):
    st.write(
        "This demonstration was trained on only 30 synthetic records. Its output must "
        "not be used for punishment, grading, or automated decisions. A real system "
        "would require representative data, privacy safeguards, fairness testing, "
        "external validation, monitoring, and an appeal process."
    )
