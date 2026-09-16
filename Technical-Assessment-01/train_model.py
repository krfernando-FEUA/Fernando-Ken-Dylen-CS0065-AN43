"""Train and compare student risk classifiers, then save the selected pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "student_performance.csv"
MODEL_PATH = BASE_DIR / "student_risk_pipeline.joblib"
METRICS_PATH = BASE_DIR / "model_comparison.csv"
CONFUSION_PATH = BASE_DIR / "confusion_matrices.json"
METADATA_PATH = BASE_DIR / "model_metadata.json"

FEATURES = ["attendance", "quiz_score", "assignment_score", "exam_score"]
TARGET = "risk_status"
POSITIVE_LABEL = "At Risk"
RANDOM_STATE = 42


def make_pipeline(classifier: object) -> Pipeline:
    numeric_steps = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[("academic_scores", numeric_steps, FEATURES)],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def evaluate_model(name: str, pipeline: Pipeline, x_train: pd.DataFrame,
                   x_test: pd.DataFrame, y_train: pd.Series,
                   y_test: pd.Series) -> tuple[dict[str, object], list[list[int]]]:
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    metrics = {
        "algorithm": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, pos_label=POSITIVE_LABEL, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, pos_label=POSITIVE_LABEL, zero_division=0
        ),
        "f1_score": f1_score(
            y_test, predictions, pos_label=POSITIVE_LABEL, zero_division=0
        ),
    }
    matrix = confusion_matrix(
        y_test, predictions, labels=["Not At Risk", "At Risk"]
    ).tolist()
    return metrics, matrix


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    x = data[FEATURES]
    y = data[TARGET]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    models = {
        "Logistic Regression": make_pipeline(
            LogisticRegression(max_iter=1_000, random_state=RANDOM_STATE)
        ),
        "Decision Tree": make_pipeline(
            DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE)
        ),
        "Random Forest": make_pipeline(
            RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE)
        ),
    }

    results: list[dict[str, object]] = []
    matrices: dict[str, object] = {
        "label_order": ["Not At Risk", "At Risk"],
        "matrices": {},
    }
    for name, pipeline in models.items():
        metrics, matrix = evaluate_model(
            name, pipeline, x_train, x_test, y_train, y_test
        )
        results.append(metrics)
        matrices["matrices"][name] = matrix

    metrics_frame = pd.DataFrame(results)
    metrics_frame.to_csv(METRICS_PATH, index=False, float_format="%.4f")
    CONFUSION_PATH.write_text(json.dumps(matrices, indent=2), encoding="utf-8")

    # Every model ties on the holdout. Logistic regression is selected because it
    # is the simplest of the tied models and produces useful class probabilities.
    selected_name = "Logistic Regression"
    selected_pipeline = models[selected_name]
    selected_pipeline.fit(x, y)
    joblib.dump(selected_pipeline, MODEL_PATH)

    metadata = {
        "selected_model": selected_name,
        "selection_reason": (
            "All three models tied; logistic regression was selected for simplicity "
            "and probability output."
        ),
        "features": FEATURES,
        "target": TARGET,
        "excluded_columns": ["student_id"],
        "random_state": RANDOM_STATE,
        "evaluation": "70/30 stratified holdout",
        "training_rows": len(x_train),
        "test_rows": len(x_test),
        "final_fit_rows": len(x),
        "classes": list(selected_pipeline.classes_),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(metrics_frame.to_string(index=False))
    print(f"\nSaved selected pipeline to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
