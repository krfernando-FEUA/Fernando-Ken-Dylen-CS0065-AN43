# Verification record

Verified on 25 October 2026 with Windows, Python 3.12, Streamlit 1.66.1 and pandas 2.3.3.

Final automated run: **116 tests passed, with 21 subtests passed, in 44.43 seconds**. This comprises 45 engine tests, 35 table/KNIME contract tests and 36 Streamlit AppTest cases. Controlled KNIME-output fixtures test the import contract; they do not count as KNIME execution.

## User story and evidence

A designer edits a fictional Sanrio economy in Streamlit, obtains a Python rule-based decision with explanations, previews a correction, and exports the current facts for a KNIME decision comparison.

| Boundary | Evidence | Status |
| --- | --- | --- |
| Inputs → validated model | Engine and table tests cover malformed numbers/booleans, missing facts, duplicate identifiers and table round trips | Passed |
| Model → arithmetic and decisions | Exact whole-execution batches, independently calculated cases, four scenarios, ordered policy outcomes and search-limit behavior | Passed |
| Decisions → correction and simulation | Immutable previews, complete-model reanalysis, caps, cooldowns, daily boundaries and incomplete batches | Passed |
| Streamlit widgets → session state → rendered elements | Native AppTest exercises navigation, editable tables, scenario replacement, imports, undo, previews, simulation and exports | Passed |
| Current model → portable KNIME inputs | XML structure, relative paths, native node connections, raw-fact contract, rule precedence and model fingerprints | Passed static/contract checks |
| KNIME decisions → Streamlit comparison | Test CSVs exercise complete matching coverage, disagreement, malformed/stale data and prior-result invalidation | Tested with controlled CSVs; not a native KNIME execution |
| Streamlit server | HTTP 200 and `ok` from `/_stcore/health`; startup log identifies port 4180 | Running locally |
| Native KNIME node execution | Installed KNIME 5.12 launcher reports `KNIME Batch Executor is not installed` before loading the workflow | Unverified |

Streamlit AppTest runs the actual application and widget/session logic within Python. It does not establish pixel appearance or browser layout. Browser automation was unavailable for this local address, so no screenshot-based verification is claimed.

## Reproduce the automated checks

From the extracted project, after creating and activating a Python environment:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
python audit.py --scenario friendship-fair --output results
```

The engine regression set also matched the prior prototype across 64 complete analyses and their simulations during migration. This was a one-time migration check; the delivered Python application has no JavaScript runtime dependency. The engine tests include an independent 75-case exact-batch arithmetic oracle.

## Expected baseline outcomes

| Route | Batch input → return | Decision | Ten requested batches over 24 hours |
| --- | --- | --- | --- |
| Friendship Gift | 20 → 24 coins | Critical repeatable profit under the entered controls | 10 complete batches; +40 coins |
| Star Charm | 8 → 12 coins | High-priority account-limit concern | 2 complete batches; +8 coins |
| Cloud Latte | 10 → 14 coins | Intended bounded reward | 3 complete batches; +12 coins |

The baseline has six currency-returning routes; the remaining three have no positive gain. These are modeled outcomes, not observations from a real game or proof that a server enforces the entered controls.

## KNIME verification still required

The portable archive and its two native Rule Engine nodes are supplied. Open the current-model archive in KNIME, execute all four nodes, and upload its generated `data/decisions.csv` in Streamlit. Verify the model fingerprint, complete route coverage and both decision columns. Record any KNIME node-configuration or execution error before claiming a native pass.

The current machine lacks Batch Executor and the optional Python Integration extension. Official extension availability was checked; neither a native execution nor the optional Python Script bridge is reported as successful. See [KNIME instructions](../knime/README.md) for details.

## Scope

The engine covers simple currency-rooted paths of at most six trades, with limits of 3,000 routes and 30,000 expansions. Search truncation is visible. It models one input and output per trade, deterministic quantities, one sequential account, separately funded batches and initially unused global quotas. Unknown controls produce requests for evidence or no simulation estimate. Human usability, real game economics, enforcement correctness and general multi-ingredient crafting remain unevaluated.
