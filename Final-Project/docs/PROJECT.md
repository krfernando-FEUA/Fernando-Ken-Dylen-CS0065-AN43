# Project design

**Title:** LoopGuard: Rule-Based Decision Support for a Sanrio-Themed Virtual Economy  
**Course theme:** Expert System Using Rule-Based Reasoning for Decision Support

## Problem and decision

A price can look reasonable in one shop while forming a profitable loop when combined with a recipe and another shop. Some gains are intentional rewards. Others can repeat indefinitely under the entered rules. Missing limits or conflicting design intent create a third case: a designer needs more evidence.

The system accepts explicit economy facts and returns a decision, evidence, fired rules, questions and possible interventions. It supports the designer's judgment. It is not a playable Sanrio game or an audit of an existing game.

## Three-part implementation

1. **Python knowledge and inference:** `loopguard/engine.py` validates input, enumerates simple currency-rooted paths, computes exact lots with `Fraction`, derives facts and executes explicit decision predicates. `rules.json` is the inspectable 35-rule catalog. Unknown values remain distinct from known zeros and false values.
2. **KNIME visual reasoning:** Python exports route facts with numeric flags for uncertainty, intent and restrictions. Native Rule Engine nodes classify the facts and assign severity, then export decisions. `run_workflow.py` compares complete cycle IDs and outcomes against the Python result using the current input fingerprint. This makes disagreement observable.
3. **Streamlit interaction:** `app.py` is a functional workbench: native tables, route diagrams, rule traces, patch previews, simulations and exports. It contains no copied JavaScript inference engine or separate showcase site.

KNIME receives raw decision facts as its inputs. Its decision columns are computed by the workflow; they are not relabeled Python verdicts. Automatic execution requires a compatible batch executor. The workflow can also be imported and executed in KNIME's desktop interface.

## Knowledge representation

Items have stable IDs, names and kinds. Transactions describe an input, output, fee in output units, character, transaction type, enabled flag, daily execution cap and scope, cooldown, output transferability and intent. A null cap/cooldown is unknown; zero is explicitly unrestricted. A transaction executes as a whole; the route uses the smallest exact batch with no leftover assets credited.

For each conversion, `r = (output − fee) / input`. A closed route with a product of rates above one yields a positive return. The resulting arithmetic is then interpreted by domain rules. Examples:

- Positive, unintended gain with explicitly absent limits → critical repeatable profit within the model.
- Positive gain with missing controls → request evidence.
- Intended gain with declared finite restrictions → intentional reward.
- Transferable, account-capped returns → an allocation concern to investigate, not a proven bypass.

Explicit decision precedence resolves competing interpretations. Catalog priority numbers document stages; they are not a dynamic rule scheduler. The policies are authored for this project and still need domain-expert evaluation.

## Intervention and simulation

The system may lower a terminal payout, add a fee, or propose a shared cap. Pricing corrections can remove profit; caps bound the frequency while leaving the gain intact. Previews apply changes to an isolated model and rescan every enumerated route.

Simulation schedules one account sequentially. Each complete batch has separate starting funds. Daily quotas reset at synthetic midnight; cooldowns persist across boundaries. An incomplete batch spends no seed money and realizes no return. Global quotas start unused by other players. Unknown cap/cooldown facts produce no estimate.

## Evaluation

Use independently calculated arithmetic cases, known rule outcomes, missing-data scenarios, immutable-preview checks, input-validation failures and scheduler boundary cases. Native Streamlit AppTest exercises actual widgets and session transitions. KNIME execution and comparison should be reported separately from Python tests or XML/workflow construction; see VERIFICATION.md for measured results.

Human evaluation remains separate: ask peers to explain a finding, distinguish an intended reward, request missing evidence, and justify a correction. Record errors and completion time. Do not invent user-study results.

## Five-member allocation

| Member | Main responsibility | Demonstrable output |
| --- | --- | --- |
| 1 | Knowledge engineering | Rule catalog, decision precedence, evidence questions |
| 2 | Python inference | Exact batches, graph search, simulations and regression tests |
| 3 | KNIME integration | Visual rule workflow, CSV contracts, output comparison |
| 4 | Streamlit interaction | Editable facts, explanations, fixes and input handling |
| 5 | Evaluation and documentation | Independent examples, UI tests, demo and final report |

Map these concepts to the actual Modules 1–6 syllabus supplied by your instructor. No syllabus details or requirements are assumed beyond the given project theme.
