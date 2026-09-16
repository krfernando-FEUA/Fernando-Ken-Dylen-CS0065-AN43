# Asynchronous Activity 1 Student Early Warning Tool Using KNIME

This folder contains the required submission files for Asynchronous Activity 1
in CS0065 Intelligent Systems, section AN43. The KNIME workflow predicts whether
a student is **At Risk** or **Not At Risk** from attendance, quiz, assignment,
and examination scores.

## Files

- `DemoEarlyWarningTool.knwf` - exported KNIME workflow with saved execution
  results.
- `student_performance_knime.csv` - 30-record synthetic dataset used by the
  workflow.
- `Fernando_Ken_Dylen_KNIME_GitHub_Evidence.pdf` - screenshots and captions
  documenting the completed workflow and repository preparation.

## Workflow

The workflow performs these steps:

1. Reads the student performance CSV file.
2. Removes `student_id` from the predictive inputs.
3. Normalizes the four academic features.
4. Creates a fixed, stratified 70/30 training and test partition.
5. Trains Decision Tree, Logistic Regression, and Random Forest classifiers.
6. Applies each classifier to the test data.
7. Uses Scorer nodes to compare predictions with `risk_status`.

## Algorithms

- Decision Tree
- Logistic Regression
- Random Forest

All three models correctly classified the nine records in the saved test
partition. Each model produced a confusion matrix of `[[5, 0], [0, 4]]` using
the label order `[Not At Risk, At Risk]`. These results are suitable only for a
classroom demonstration because the dataset contains 30 synthetic records.

## How to Run

1. Download `DemoEarlyWarningTool.knwf` and
   `student_performance_knime.csv`.
2. Open KNIME Analytics Platform.
3. Select **File > Import KNIME Workflow** and choose the `.knwf` file.
4. Open the CSV Reader configuration.
5. Browse to the included `student_performance_knime.csv` file and confirm the
   preview contains 30 rows and 6 columns.
6. Execute all nodes.
7. Open each Scorer node to review the confusion matrix and accuracy statistics.

## Dataset Columns

- `student_id` - record identifier, excluded from model training
- `attendance` - attendance score
- `quiz_score` - quiz score
- `assignment_score` - assignment score
- `exam_score` - examination score
- `risk_status` - target label

## Author

Ken Dylen Fernando

## Course and Section

CS0065 Intelligent Systems - AN43
