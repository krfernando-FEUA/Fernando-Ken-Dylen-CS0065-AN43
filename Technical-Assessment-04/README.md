# Technical Assessment 04

**CS0065 - Intelligent Systems | AN43**

- Student: Ken Dylen Fernando
- Professor: Crisola Tan
- Assessment date: October 31, 2026

A simple Python program that uses weather and context facts to give room-comfort and outdoor advice. It demonstrates knowledge representation (KR), rule-based reasoning (RBR), and case-based reasoning (CBR).

## Run

Use Python 3. No extra packages are required.

```powershell
cd Technical-Assessment-04
python reasoning.py
```

When prompted to revise the CBR solution, press Enter to keep it or type replacement advice. The new case is retained in memory for that run; restarting the program resets the case base.

## How it works

The knowledge base contains five facts in three categories:

| Category | Facts |
| --- | --- |
| Measurements | Temperature and humidity |
| Weather | Whether it is raining |
| Context | Planned outdoor activity and room occupancy |

RBR checks all three rules and returns every matching action: cooling when temperature exceeds 30 C and the room is occupied, rain protection when rain and outdoor activity coincide, and dehumidification when humidity exceeds 80% and the room is occupied.

CBR compares the current facts with three past cases, retrieves the closest case, reuses its solution, accepts an optional manual revision, and retains the result. Numeric comparisons use fixed ranges of 50 C and 100 percentage points; Boolean comparisons use exact matches. The five scores have equal weight, and case ID breaks ties. Similarity measures closeness, not probability. Cases and thresholds are instructional examples.

With the supplied facts, all three rules fire. CBR retrieves C001 with similarity 0.986 and retains the result as C004, increasing the case count to four.

## Files

| File | Purpose |
| --- | --- |
| [reasoning.py](reasoning.py) | Complete Python implementation |
| [reports/TA4_Fernando.docx](reports/TA4_Fernando.docx) | Word report using the original assessment template |
| [screenshots/RBR_output.png](screenshots/RBR_output.png) | Screenshot of the captured RBR output |
| [screenshots/CBR_output.png](screenshots/CBR_output.png) | Screenshot of the captured CBR output |
| [outputs/python_output.txt](outputs/python_output.txt) | Standard output from a run with Enter supplied at the revision prompt |

The screenshots display captured output from the Python script. The text log does not echo the supplied Enter key, so the revision prompt and final solution share a line.
