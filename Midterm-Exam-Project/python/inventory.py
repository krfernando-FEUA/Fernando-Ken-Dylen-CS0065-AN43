from pathlib import Path
import argparse
import json
import math
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["stock_level", "daily_usage", "lead_time_days", "urgency", "item_budget_php", "unit_cost_php", "safety_days"]
COLUMNS = ["item_id", "item_name"] + FEATURES
WEIGHTS = {"shortage": 0.60, "urgency": 0.30, "lead_time": 0.10}


def validate_data(frame):

    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    if len(frame) == 0:
        raise ValueError("The dataset has no records.")
    if len(frame) > 10000:
        raise ValueError("Use at most 10,000 rows in this classroom interface.")
    data = frame[COLUMNS].copy()
    for col in ["item_id", "item_name"]:
        if data[col].isna().any():
            raise ValueError(f"{col} contains a missing value.")
        data[col] = data[col].astype(str).str.strip()
        if data[col].eq("").any():
            raise ValueError(f"{col} contains a blank value.")
    if data.item_id.duplicated().any():
        raise ValueError("Duplicate item_id. Resolve duplicate records before ranking.")
    limits = {"stock_level": (0, 1000000), "daily_usage": (0, 10000), "lead_time_days": (0, 365), "urgency": (1, 5), "item_budget_php": (0, 10000000), "unit_cost_php": (0.01, 1000000), "safety_days": (0, 90)}
    for col, (lo, hi) in limits.items():
        raw = data[col]
        if raw.map(lambda v: isinstance(v, (bool, np.bool_))).any():
            raise ValueError(f"{col} must be numeric, not Boolean.")
        data[col] = pd.to_numeric(raw, errors="coerce")
        if not np.isfinite(data[col]).all():
            raise ValueError(f"{col} contains a missing, nonnumeric, or nonfinite value.")
        if not data[col].between(lo, hi).all():
            raise ValueError(f"{col} must be between {lo} and {hi}.")
    for col in ["stock_level", "lead_time_days", "urgency", "safety_days"]:
        if (data[col] != np.floor(data[col])).any():
            raise ValueError(f"{col} must contain whole numbers.")
        data[col] = data[col].astype(int)
    for col in ["unit_cost_php", "item_budget_php"]:
        if not np.isclose(data[col] * 100, np.round(data[col] * 100), atol=1e-7, rtol=0).all():
            raise ValueError(f"{col} allows at most two decimal places.")
    return data


def score_inventory(frame, weights=None):
    data = validate_data(frame)
    w = dict(WEIGHTS if weights is None else weights)
    if set(w) != set(WEIGHTS) or not all(isinstance(v, (int, float)) and math.isfinite(v) and 0 <= v <= 1 for v in w.values()) or not math.isclose(sum(w.values()), 1, abs_tol=1e-9):
        raise ValueError("Provide nonnegative shortage, urgency, and lead_time weights that sum to 1.")
    data["lead_demand"] = data.daily_usage * data.lead_time_days
    data["target_stock"] = np.ceil(data.daily_usage * (data.lead_time_days + data.safety_days)).astype(int)
    data["desired_quantity"] = np.maximum(0, data.target_stock - data.stock_level).astype(int)

    budget_cents = np.rint(data.item_budget_php * 100).astype("int64")
    cost_cents = np.rint(data.unit_cost_php * 100).astype("int64")
    data["affordable_quantity"] = budget_cents // cost_cents
    data["suggested_quantity"] = np.minimum(data.desired_quantity, data.affordable_quantity).astype(int)
    data["order_cost_php"] = data.suggested_quantity * cost_cents / 100
    data["funding_gap_units"] = data.desired_quantity - data.suggested_quantity
    data["shortage_score"] = np.where(data.target_stock > 0, data.desired_quantity / data.target_stock.clip(lower=1), 0.0)
    data["urgency_score"] = (data.urgency - 1) / 4
    data["lead_time_score"] = np.minimum(data.lead_time_days / 30, 1.0)
    data["weighted_score"] = 100 * (w["shortage"] * data.shortage_score + w["urgency"] * data.urgency_score + w["lead_time"] * data.lead_time_score)

    data.loc[data.desired_quantity == 0, "weighted_score"] = 0.0
    data["rule_score"] = np.select([
        data.desired_quantity.eq(0),
        data.stock_level.eq(0) & data.daily_usage.gt(0),
        data.stock_level.lt(data.lead_demand),
    ], [0, 100, 75], default=50)
    data["rule_priority"] = data.rule_score.map({0: "No reorder", 50: "Safety-stock refill", 75: "High", 100: "Critical"})
    data["weighted_priority"] = np.select([data.desired_quantity.eq(0), data.weighted_score.ge(70), data.weighted_score.ge(40)], ["No reorder", "High", "Medium"], default="Low")
    data["decision"] = np.select([data.desired_quantity.eq(0), data.suggested_quantity.eq(0), data.funding_gap_units.gt(0)], ["No reorder needed", "Review funding: cannot buy one unit", "Partial order: funding review needed"], default="Order suggested quantity")
    data["explanation"] = [
        f"Target {t}; stock {s}; shortage {q}. Budget PHP {b:.2f} permits {a} units at PHP {c:.2f}. {d}."
        for t, s, q, b, a, c, d in zip(data.target_stock, data.stock_level, data.desired_quantity, data.item_budget_php, data.affordable_quantity, data.unit_cost_php, data.decision)
    ]
    return data


def rank_inventory(scored, method="weighted"):
    if method not in {"weighted", "rule"}:
        raise ValueError("Method must be weighted or rule.")
    key = "weighted_score" if method == "weighted" else "rule_score"

    ranked = scored.sort_values([key, "urgency", "desired_quantity", "item_id"], ascending=[False, False, False, True], kind="mergesort").reset_index(drop=True)
    ranked.insert(0, "rank", np.arange(1, len(ranked) + 1))
    return ranked


def compare_methods(scored):
    weighted = rank_inventory(scored, "weighted")
    rule = rank_inventory(scored, "rule")
    comparison = weighted[["item_id", "item_name", "rank", "weighted_score", "suggested_quantity", "order_cost_php", "funding_gap_units"]].rename(columns={"rank": "weighted_rank"})
    comparison = comparison.merge(rule[["item_id", "rank", "rule_score", "rule_priority"]].rename(columns={"rank": "rule_rank"}), on="item_id", validate="one_to_one")
    comparison["rank_difference"] = comparison.rule_rank - comparison.weighted_rank
    eligible = scored.loc[scored.desired_quantity.gt(0), "item_id"]
    k = min(10, len(eligible))
    wtop = weighted[weighted.desired_quantity.gt(0)].head(k)
    rtop = rule[rule.desired_quantity.gt(0)].head(k)
    overlap = len(set(wtop.item_id) & set(rtop.item_id))
    metrics = {
        "records": len(scored), "items_needing_restock": len(eligible), "top_k": k,
        "top_k_overlap": overlap, "top_k_overlap_fraction": overlap / k if k else None,
        "rank_correlation_all_items": float(comparison.weighted_rank.corr(comparison.rule_rank)) if len(scored) > 1 else None,
        "mean_absolute_rank_difference": float(comparison.rank_difference.abs().mean()),
        "total_suggested_units": int(scored.suggested_quantity.sum()),
        "total_order_cost_php": round(float(scored.order_cost_php.sum()), 2),
        "total_reserved_budget_php": round(float(scored.item_budget_php.sum()), 2),
        "items_with_funding_gap": int(scored.funding_gap_units.gt(0).sum()),
        "unfunded_units": int(scored.funding_gap_units.sum()),
        "weighted_top_k_stockouts": int(wtop.stock_level.eq(0).sum()),
        "rule_top_k_stockouts": int(rtop.stock_level.eq(0).sum()),
    }
    return comparison, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "inventory.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    data = pd.read_csv(args.input)
    scored = score_inventory(data)
    comparison, metrics = compare_methods(scored)
    args.output.mkdir(parents=True, exist_ok=True)
    for method in ["weighted", "rule"]:
        rank_inventory(scored, method).to_csv(args.output / f"{method}_ranking.csv", index=False)
    comparison.to_csv(args.output / "comparison.csv", index=False)
    alternative = score_inventory(data, {"shortage": 0.45, "urgency": 0.45, "lead_time": 0.10})
    sensitivity = comparison[["item_id", "weighted_rank"]].merge(rank_inventory(alternative)[["item_id", "rank"]].rename(columns={"rank": "alternative_rank"}), on="item_id")
    sensitivity["absolute_rank_change"] = abs(sensitivity.weighted_rank - sensitivity.alternative_rank)
    sensitivity.to_csv(args.output / "weight_sensitivity.csv", index=False)
    metrics["weight_sensitivity_mean_rank_change"] = float(sensitivity.absolute_rank_change.mean())
    metrics["weight_sensitivity_max_rank_change"] = int(sensitivity.absolute_rank_change.max())
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2, allow_nan=False), encoding="utf-8")
    (args.output / "settings.json").write_text(json.dumps({"weights": WEIGHTS, "lead_time_cap_days": 30, "currency": "PHP", "budget_scope": "earmarked separately for each item", "tie_break": ["urgency descending", "desired quantity descending", "item ID ascending"]}, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
