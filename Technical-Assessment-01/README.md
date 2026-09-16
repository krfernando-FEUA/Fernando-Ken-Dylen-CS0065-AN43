# Student Performance Risk Classifier

Technical Assessment submission for **CS0065 - AN43** by Fernando, Ken Dylen.

The KNIME submission required by the activity is available in
[`DemoEarlyWarningTool`](./DemoEarlyWarningTool). The remaining files in this
assessment folder provide the Python and Streamlit recreation of the same model.

This classroom project compares three supervised classification models for
predicting whether a student is **At Risk** or **Not At Risk** from four inputs:

- Attendance
- Quiz score
- Assignment score
- Examination score

`student_id` is intentionally excluded because it is an identifier rather than a
meaningful predictive feature.

## Project files

- `train_model.py` - trains and evaluates Logistic Regression, Decision Tree,
  and Random Forest models.
- `app.py` - Streamlit prediction interface with validation and responsible-use
  guidance.
- `verify_model.py` - checks the valid worksheet examples against the saved
  pipeline.
- `student_performance.csv` - 30-record synthetic classroom dataset.
- `student_risk_pipeline.joblib` - selected fitted preprocessing and model
  pipeline.
- `model_comparison.csv` - evaluation metrics for the three models.
- `confusion_matrices.json` - confusion matrices and label order.
- `model_metadata.json` - features, evaluation setup, and model-selection notes.

## Set up and run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train_model.py
.\.venv\Scripts\python.exe verify_model.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Then open `http://localhost:8501`.

## Evaluation summary

The comparison uses a fixed-seed 70/30 stratified holdout with 21 training rows
and 9 test rows. All three models achieved 1.00 accuracy, precision, recall, and
F1-score on this small synthetic holdout. Each confusion matrix was
`[[5, 0], [0, 4]]`, using label order `[Not At Risk, At Risk]`.

Logistic Regression is saved as the selected pipeline because the models tied
and it is the simplest tied model while also providing class probabilities.

## Important limitation

The perfect scores do not demonstrate real-world readiness. The dataset contains
only 30 synthetic records with a clear pattern. This application is a classroom
demonstration and must not be used for grading, punishment, or automated student
decisions. Predictions require human review.
