# LoopGuard · Friendship Fair

A **Python + KNIME + Streamlit expert system** for a fictional Sanrio game economy. It supports a designer making one decision: should a connected sequence of exchanges be corrected, retained as an intentional reward, or investigated for missing facts?

The working application is a native Streamlit workbench with editable tables and explanations. Hello Kitty, My Melody, Kuromi and the café characters provide the domain: shops, recipes and rewards. This is an unofficial classroom scenario, with invented economics.

## Start the Streamlit application

Use Python 3.12. From this folder, create a local environment and install the pinned dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open **http://127.0.0.1:8501/**. On macOS/Linux use `.venv/bin/python` for the last two commands. No Node.js, API key, hosted service, or model training is required.

Use **Audit → Edit economy → Test a fix**. KNIME is a separate working section, and **Rules & exports** contains the complete rule catalog and downloadable facts. Edits are isolated to a Streamlit session; save project JSON to keep them after closing it. Undo retains the last 20 changes.

## Where the intelligence lives

| Technology | Actual responsibility |
| --- | --- |
| Python | Validate facts, discover bounded exchange loops, calculate exact whole-execution batches, apply 35 explicit rules, explain conclusions, recommend changes and simulate restrictions |
| KNIME | Read Python's raw route facts, apply native Rule Engine nodes for classification and severity, and export decisions for comparison |
| Streamlit | Enter/edit the economy, inspect facts and rule traces, preview and apply fixes, run simulations and exchange data with KNIME |

The native KNIME workflow is `knime/LoopGuard_Friendship_Fair.knwf`. See [KNIME setup and execution](../knime/README.md). The separate Python Integration extension is optional; the supplied native workflow uses CSV Reader, Rule Engine and CSV Writer nodes. Automatic execution depends on the installed KNIME edition/extensions; the app reports that capability instead of substituting Python results for a KNIME run.

For a manual comparison, download the **current** workflow from Streamlit's KNIME section, execute it in KNIME, then upload its `data/decisions.csv` in that section. The app checks the input fingerprint and route coverage before displaying agreement or disagreement.

## The demonstration

Hello Kitty sells two ribbons for 20 Friendship Coins. My Melody crafts them into a gift. The gift counter returns 24 coins. Python establishes the +4 gain, then the rules check intent, caps and cooldowns before deciding whether it is problematic.

Choose **Test a fix → Align the buyback**. Its isolated preview changes the return to 20 and removes this route's gain. The café's intended, bounded reward remains. **Missing Telemetry** demonstrates why absent evidence cannot be assumed unlimited.

Four included scenarios: Friendship Fair, Balanced Market, Missing Telemetry and Festival Rush. The baseline has seven items, 15 trades and six currency-returning routes.

## Python and CSV use

```powershell
python audit.py --scenario friendship-fair --output results
python audit.py --project my-economy.json --output results
```

These commands write items, transactions, raw `cycle_facts.csv`, decisions, rule traces, a Markdown report and the exact project. Add `--knime` to invoke a compatible local KNIME batch executor. A failed KNIME run is reported as a failure, never as agreement.

The engine itself uses only Python's standard library:

```python
from loopguard import analyze, apply_patch, simulate

audit = analyze(model)
route = audit["findings"][0]
proposed = apply_patch(model, route["recommendations"][0]["patch"])
result = simulate(proposed, route["id"], requested_batches=10, hours=24)
```

## Verify and present

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

- [Project design and five-member roles](PROJECT.md)
- [Presentation walkthrough](DEMO.md)
- [Verification results and limits](VERIFICATION.md)
- [Character artwork sources](ASSETS.md)

Search is limited to simple currency-returning paths of at most six trades, 3,000 routes and 30,000 expansions. The prototype uses one input and one output per trade. No random drops, player demand, inventory shortages, account-identity enforcement or multi-ingredient recipes are modeled. A clean result applies only to the entered model and bounded search.
