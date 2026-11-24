# Six-minute classroom demonstration

## 0:00 — State the decision

Open Streamlit and select **Friendship Fair**. Explain that Sanrio supplies the fictional domain: character-run shops, crafting and rewards. The task is deciding whether profitable exchange routes should be corrected, preserved or investigated.

## 0:40 — Inspect the gift route

In **Audit**, select the Friendship Gift route. Walk through 20 coins → two ribbons → one gift → 24 coins. Show the +4 return and exact execution counts. Open the fired-rule explanation: positive gain alone is insufficient; intent and repetition determine the decision.

## 1:40 — Change a fact

In **Edit economy**, change the gift-buyback output from 24 to 20 and press **Save & audit**. Return to Audit: the gift loop is now break-even. Press **Undo last change** to restore the baseline.

## 2:20 — Preview a decision

In **Test a fix**, select the gift route and **Align the buyback**. Show that the preview leaves the working model intact and rechecks the complete bounded economy. Simulate ten batches over 24 hours: current +40 coins; proposed zero net gain. Apply the fix or discard it by selecting Current economy only.

## 3:20 — Preserve intentional rewards

Restore Friendship Fair. Inspect the Cloud Latte route and simulate it: three complete batches, +12 coins. Explain the entered global cap, cooldown and intended label. Contrast it with the Star Charm route's account-allocation concern.

## 4:00 — Make uncertainty visible

Load **Missing Telemetry**. The gift route needs evidence because the cap/cooldown facts are unknown. Simulation reports **No estimate**, not zero earnings or unlimited earnings. Show the questions that resolve the decision.

## 4:40 — Show KNIME's role

In Streamlit's KNIME section, download the current workflow and import it in KNIME. Follow CSV Reader → classification Rule Engine → severity Rule Engine → CSV Writer. Inspect one rule and its derived fact columns. If the local batch prerequisite is available, run the Streamlit comparison; otherwise execute the workflow manually and upload its `data/decisions.csv` back into Streamlit. Describe exactly which execution was verified, and do not present Python's result as a KNIME run. Prepare this desktop execution before presenting; the installed machine's missing Batch Executor prevents an automatic demo.

## 5:30 — Finish with reproducibility

Open **Rules & exports**, search LG24, and download the project and audit. The input fingerprint ties a report to one economy. State the tested scope and one meaningful limitation: declared controls, simplified recipes or bounded simple paths.
