# LoopGuard in KNIME

This folder provides a native KNIME decision workflow for the fictional Sanrio-inspired **Friendship Fair** economy. Python calculates exact conversion-route facts; KNIME's **Rule Engine** nodes independently apply the ordered decision rules. Streamlit is the operator interface. KNIME is therefore a reasoning and comparison stage, not a screenshot or a decorative workflow diagram.

## What is included

- `LoopGuard_Friendship_Fair.knwf`: a portable four-node workflow with baseline input facts.
- `LoopGuard Friendship Fair/`: the same unpacked workflow, with relative data paths.
- `build_workflow.py`: generates those native node settings from the included reader template.
- `export_tables.py`: exports a current model to CSVs and creates a fresh `.knwf`.
- `run_workflow.py`: optional automatic batch execution in an isolated temporary workspace, plus strict comparison of imported manual results.
- `python_script.py`: optional bridge for the **KNIME Python Integration**, using the same Python expert engine as Streamlit.
- `baseline/`: inspectable input model, facts, findings, rule trace and rule catalog.

The native workflow is:

```text
Python exact route facts → CSV Reader → Rule Engine → Rule Engine → CSV Writer
                                      classification   severity    decisions.csv
```

The classification node contains ten ordered rules covering break-even, loss, oversized batches, missing limits, uncertain intent, unbounded intended rewards, repeatable profit, bounded intended rewards, account-limit concerns and bounded arbitrage. The second node maps that conclusion to a decision priority. They do not read Python's classification column: the CSV input contains arithmetic and policy facts only.

## Open and run manually

1. In KNIME Analytics Platform, import `LoopGuard_Friendship_Fair.knwf` using **File → Import KNIME Workflow** (or the import action in the modern interface).
2. Open the workflow. Execute all four nodes from left to right.
3. Inspect the output of **Assign severity**. The baseline has six routes: one `critical`, one `high`, one `intended` and three `healthy`.
4. The writer saves `data/decisions.csv` inside the imported workflow's directory. It overwrites only that workflow-local result file.
5. Import that CSV in Streamlit's KNIME area. A SHA-256 model fingerprint and cycle IDs must match the current economy before the Python/KNIME comparison is accepted.

For an edited economy, export its current-model KNIME bundle from Streamlit and import that new archive. A baseline archive does not reflect later UI edits.

**Validation status:** the four-node baseline was imported and executed successfully in the KNIME Analytics Platform 5.12.0 LTS GUI on 30 October 2026. All four nodes completed, and the exported six decisions matched the Python engine for classification and severity: one critical, one high, one intended and three healthy. The model fingerprint was checked. This GUI verification also revealed missing required node bundle metadata in the original archive; the generator and archive now include it. Screenshots and the actual result CSV are retained in `work/loopguard-presentation/evidence-assets/` in the project workspace. This validates the native baseline only. Automatic execution still requires the missing KNIME Batch Executor extension, and the optional Python Integration extension remains absent; neither integration has been verified. The archive's XML, portable paths, graph connections, rule ordering and parity with the four Python scenarios are separately tested.

## Automatic comparison

From the extracted project directory, with the Python dependencies installed:

```powershell
python knime/run_workflow.py knime/baseline/model.json --output knime/results
```

KNIME is located through `LOOPGUARD_KNIME`, PATH or common Windows installation directories. You can set an explicit executable:

```powershell
python knime/run_workflow.py knime/baseline/model.json --knime "C:\Path\To\KNIME\knimec.exe"
```

Each run uses a new temporary workflow and workspace. It validates the current model, computes a fingerprint, writes fresh facts, runs KNIME, checks the returned cycle set and compares both classification and severity. A timeout, missing output, stale fingerprint or failed process produces an error; none is reported as a successful audit. An economy with no currency return paths returns `empty` and explicitly reports that KNIME was not invoked.

KNIME 5.12 on this machine requires its separate **Batch Executor** extension for this headless command. The official 5.12.0 repository metadata was checked and contained no installable Batch Executor unit; the installation link emitted by the launcher returned HTTP 404 on 25 October 2026. No unofficial extension or licensing workaround was installed. Use manual execution, or obtain the applicable official extension before enabling automatic runs.

## Full KNIME inputs with a Python Script node

Install the **KNIME Python Integration** if your classroom wants the table preparation to happen inside KNIME as well. Follow KNIME's [Python quickstart](https://docs.knime.com/ap/latest/python_installation_guide/tutorials/quickstart) and use its bundled environment.

1. Add two **CSV Reader** nodes for the exported `items.csv` and `transactions.csv`.
2. Keep all identifiers and text columns as strings. Read `enabled`/`transferable` as booleans or explicit `true`/`false` strings. Blank `cap`, `cooldown` and `transferable` cells mean unknown; zero cap/cooldown means explicitly unlimited. Do not replace missing cells with zero.
3. Add a **Python Script** node with **two input tables and three output tables**. Connect items to input 0 and transactions to input 1.
4. Add a **String Configuration** flow variable called `loopguard_project` containing the extracted project folder, and connect its flow-variable port to the Python Script node. For an economy whose name/scenario differs from the baseline, also provide `loopguard_name` and `loopguard_scenario` matching the model JSON.
5. Paste `python_script.py` into the script editor. It uses `knime.scripting.io`, `input_tables[i].to_pandas()` and `Table.from_pandas(...)` as documented in the [official scripting API](https://docs.knime.com/ap/latest/python_installation_guide/reference/scripting-api).
6. Connect output 0 (decision facts) to **Classify route** in the supplied native workflow, replacing the facts CSV Reader. Outputs 1 and 2 contain Python findings and the full rule trace; connect table views or CSV writers to inspect them.

This optional script is syntax-checked and uses the tested table adapter. It has not been run inside KNIME on this machine because Python Integration is absent. `knime.scripting.io` is supplied by KNIME; do not try to install a similarly named PyPI package.

## CSV contract

`items.csv`: `id,name,kind,icon` (`icon` is optional on input).

`transactions.csv`: `id,name,from,to,input,output,fee,enabled,character,kind,cooldown,cap,capScope,transferable,intent`.

The adapter rejects malformed booleans, non-finite numbers, duplicate columns, invalid IDs, missing required values and invalid engine facts. It preserves nullable booleans/numbers and supplies explicit output dtypes even for empty tables. Fees are denominated in the output item, caps are executions per day, and cooldowns are minutes.

`cycle_facts.csv` contains the route ID/title, exact-batch arithmetic converted to report numbers, binary flags for known policy facts, and `model_fingerprint`. Unknown policy data is represented explicitly by uncertainty flags. The native Rule Engine applies those flags before any critical or intended-reward conclusion.

## Configuration provenance

The CSV Reader model follows the settings schema saved by installed KNIME 5.12. The Rule Engine factory is `org.knime.base.node.rules.engine.RuleEngineNodeFactory`; its rules use ordinary KNIME column references and first-match ordering. The CSV Writer uses the legacy factory retained in this installation (`org.knime.base.node.io.csvwriter.CSVWriterNodeFactory`) to keep its configuration small and inspectable. Only configuration structure was used; no unrelated user data is included.

References: [KNIME file handling](https://docs.knime.com/latest/analytics_platform_file_handling_guide/index.html), [KNIME user guide](https://docs.knime.com/latest/analytics_platform_user_guide/index.html), [official 5.12 update repository](https://update.knime.com/analytics-platform/lts/5.12/5.12.0/).
