# Inventory Restocking Decision Support

CS0065 AN43, Group 6

- Ken Dylen Fernando — Leader
- Alvin Christian Panio
- Nadine Love Ramos

The project ranks 60 synthetic UGREEN inventory records using weighted scoring and a rule-based comparison. Both methods calculate suggested quantities within the budget reserved for each item.

## Files

| File | Purpose |
| --- | --- |
| [Colab notebook](colab/UGREEN_Inventory_Restocking.ipynb) | Calculations, manual examples, tests, comparisons, and CSV exports |
| [Streamlit app](python/app.py) | Local interface for sample data, CSV uploads, or one item |
| [Algorithm module](python/inventory.py) | Validation, both scoring methods, ranking, and exports |
| [Tests](python/test_inventory.py) | Nine tests covering normal, missing, boundary, and uncertain cases |
| [Requirements](python/requirements.txt) | Python dependencies |
| [KNIME workflow](knime/UGREEN_Inventory_Restocking.knwf) | Both algorithms, embedded dataset, and no annotations |
| [Dataset](data/inventory.csv) | 60 records with seven input features |
| [Data dictionary](data/data_dictionary.csv) | Field definitions and validation rules |

## Google Colab

[Open the notebook in Colab](https://colab.research.google.com/github/krfernando-FEUA/Fernando-Ken-Dylen-CS0065-AN43/blob/main/Midterm-Exam-Project/colab/UGREEN_Inventory_Restocking.ipynb).

Run the first cell and upload `inventory.csv`, `inventory.py`, and `test_inventory.py` together. Run the remaining cells in order. The notebook displays rankings, comparison results, a chart, test results, and a manual example, then exports CSV files to its `results` folder. Runtime files must be uploaded again when Colab starts a fresh runtime.

## Local Python and Streamlit

From `Midterm-Exam-Project`, run:

```bash
python -m pip install -r python/requirements.txt
python python/inventory.py
python -m unittest discover -s python -p test_inventory.py -v
python -m streamlit run python/app.py
```

The Python script creates `results` with both rankings, the comparison, weight sensitivity, metrics, and settings. Streamlit runs separately from the Colab notebook.

## KNIME

Import `knime/UGREEN_Inventory_Restocking.knwf` into KNIME and execute all nodes. The CSV Reader uses the embedded dataset. The two Sorters contain the complete rankings, and the final Row Filters show the top 10 items for each method. Validate replacement datasets with the Python module before using them in KNIME.

## Results and limitations

The supplied dataset has 37 items needing restocking. The two methods share eight items in their top-10 lists. Both suggest 464 units costing PHP 66,570 because they use the same quantity and budget rules. Nineteen items have funding gaps.

Inventory values and prices are synthetic. The model assumes constant usage, known costs, and separate item budgets. It does not account for pending orders, supplier availability, or shared-budget allocation. Staff should review urgency ratings and funding gaps before placing orders.
