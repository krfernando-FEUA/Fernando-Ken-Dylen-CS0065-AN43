"""Smoke-test the saved pipeline against the worksheet's valid examples."""

from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_risk_pipeline.joblib"
FEATURES = ["attendance", "quiz_score", "assignment_score", "exam_score"]

TESTS = {
    "A": ([95, 90, 92, 88], "Not At Risk"),
    "B": ([55, 48, 52, 50], "At Risk"),
    "C": ([72, 66, 68, 63], "At Risk"),
}


def main() -> None:
    model = joblib.load(MODEL_PATH)
    for name, (values, expected) in TESTS.items():
        sample = pd.DataFrame([values], columns=FEATURES)
        actual = str(model.predict(sample)[0])
        print(f"Test {name}: expected={expected!r}, actual={actual!r}")
        if actual != expected:
            raise AssertionError(f"Test {name} failed")
    print("All valid worksheet tests passed.")


if __name__ == "__main__":
    main()
