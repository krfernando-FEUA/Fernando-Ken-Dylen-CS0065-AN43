import pandas as pd
import streamlit as st
from inventory import ROOT, COLUMNS, score_inventory, rank_inventory, compare_methods

st.set_page_config(page_title="Inventory Restocking • Group 6", layout="wide")
st.title("Inventory Restocking Decision Support")
st.caption("CS0065 · Group 6 · AN43 · Ken Dylen Fernando, group leader")
st.write("Rank UGREEN inventory items using weighted scoring or rule-based scoring. Budgets are reserved separately for each item. Sample records are synthetic.")
method = st.radio("Ranking method", ["Weighted scoring", "Rule-based scoring"], horizontal=True)
source = st.radio("Inventory input", ["Sample dataset", "Upload CSV", "Enter one item"], horizontal=True)
frame = None
if source == "Sample dataset":
    frame = pd.read_csv(ROOT / "data" / "inventory.csv")
elif source == "Upload CSV":
    st.caption("Required columns: " + ", ".join(COLUMNS))
    uploaded = st.file_uploader("Inventory CSV", type="csv")
    if uploaded:
        if uploaded.size > 2_000_000:
            st.error("Please use a CSV smaller than 2 MB.")
            st.stop()
        try:
            frame = pd.read_csv(uploaded)
        except (ValueError, UnicodeError, pd.errors.ParserError) as exc:
            st.error(f"Could not read the CSV: {exc}")
            st.stop()
else:
    with st.form("single_item"):
        item_name = st.text_input("Item name", "UGREEN Nexode 240W USB-C Cable with Digital Display 1M")
        a, b, c = st.columns(3)
        stock = a.number_input("Stock level (units)", 0, 1000000, 5)
        usage = a.number_input("Daily usage (units/day)", 0.0, 10000.0, 2.0)
        lead = b.number_input("Lead time (days)", 0, 365, 7)
        urgency = b.select_slider("Urgency (1 = routine, 5 = essential)", [1, 2, 3, 4, 5], value=4)
        budget = c.number_input("Budget reserved for this item (PHP)", 0.0, 10000000.0, 3000.0, step=1.0)
        cost = c.number_input("Cost per unit (PHP)", 0.01, 1000000.0, 250.0, step=1.0)
        safety = b.number_input("Safety-stock coverage (days)", 0, 90, 7)
        submitted = st.form_submit_button("Calculate reorder")
    if submitted:
        frame = pd.DataFrame([["MANUAL-001", item_name, stock, usage, lead, urgency, budget, cost, safety]], columns=COLUMNS)
if frame is None:
    st.info("Upload a dataset or submit the item form to calculate results.")
    st.stop()
try:
    scored = score_inventory(frame)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
ranked = rank_inventory(scored, "weighted" if method == "Weighted scoring" else "rule")
comparison, metrics = compare_methods(scored)
a, b, c, d = st.columns(4)
a.metric("Items needing restock", metrics["items_needing_restock"])
b.metric("Suggested units", metrics["total_suggested_units"])
c.metric("Order cost (PHP)", f"{metrics['total_order_cost_php']:,.2f}")
d.metric("Items needing more funding", metrics["items_with_funding_gap"])
if metrics["items_with_funding_gap"]:
    st.warning("Some shortages cannot be fully funded. Review the funding gaps before placing orders.")
st.subheader("Reorder recommendations")
st.dataframe(ranked[["rank", "item_id", "item_name", "weighted_score", "rule_priority", "suggested_quantity", "order_cost_php", "funding_gap_units", "decision"]], hide_index=True, width="stretch")
st.download_button("Download ranked results", ranked.to_csv(index=False), "restocking_results.csv", "text/csv")
if len(frame) > 1:
    st.subheader("Method comparison")
    st.write(f"Top-{metrics['top_k']} overlap: {metrics['top_k_overlap']}. Rank correlation: {metrics['rank_correlation_all_items']:.3f}. Both methods use the same quantity and budget rules.")
    st.dataframe(comparison, hide_index=True, width="stretch")
with st.expander("How scores and quantities are calculated"):
    st.write("Target = ceiling(daily usage × (lead time + safety days)). Desired quantity = max(0, target − stock). Suggested quantity is the smaller of desired quantity and the whole units affordable from the item budget.")
    st.write("Weighted score = 100 × (0.60 × shortage fraction + 0.30 × normalized urgency + 0.10 × capped lead time). An item with no shortage scores zero. Lead times of 30 days or more get the maximum lead-time score.")
    st.write("Rules: no shortage = 0; out of stock with active usage = 100; stock below lead-time demand = 75; otherwise safety-stock refill = 50. Ties use higher urgency, larger shortage, then item ID.")
    st.dataframe(ranked[["item_id", "explanation"]], hide_index=True, width="stretch")
st.caption("Demonstration only: constant usage, known prices and independent item budgets are assumed. Human review is needed for supplier availability, changing demand, and funding transfers.")
