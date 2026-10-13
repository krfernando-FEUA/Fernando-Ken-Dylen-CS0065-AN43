import unittest
import numpy as np
import pandas as pd
from inventory import COLUMNS, ROOT, score_inventory, rank_inventory, compare_methods


def row(**overrides):
    data = dict(zip(COLUMNS, ["T001", "Test item", 5, 2.0, 7, 4, 1000.0, 100.0, 3]))
    data.update(overrides)
    return pd.DataFrame([data])


class InventoryTests(unittest.TestCase):
    def test_known_calculation(self):
        result = score_inventory(row()).iloc[0]
        self.assertEqual(result.target_stock, 20)
        self.assertEqual(result.desired_quantity, 15)
        self.assertEqual(result.suggested_quantity, 10)
        self.assertEqual(result.rule_score, 75)
        self.assertAlmostEqual(result.weighted_score, 69.8333333333)
        self.assertEqual(result.funding_gap_units, 5)

    def test_no_usage_and_surplus(self):
        for frame in [row(daily_usage=0, stock_level=0), row(stock_level=20), row(stock_level=25)]:
            r = score_inventory(frame).iloc[0]
            self.assertEqual(r.suggested_quantity, 0)
            self.assertEqual(r.weighted_score, 0)
            self.assertEqual(r.rule_score, 0)

    def test_stockout_and_exact_lead_boundary(self):
        self.assertEqual(score_inventory(row(stock_level=0)).iloc[0].rule_score, 100)
        self.assertEqual(score_inventory(row(stock_level=13)).iloc[0].rule_score, 75)
        self.assertEqual(score_inventory(row(stock_level=14)).iloc[0].rule_score, 50)
        self.assertEqual(score_inventory(row(stock_level=15)).iloc[0].rule_score, 50)

    def test_budget_boundaries_and_centavos(self):
        for budget, expected in [(0, 0), (99.99, 0), (100, 1), (100.01, 1), (1500, 15)]:
            self.assertEqual(score_inventory(row(item_budget_php=budget)).iloc[0].suggested_quantity, expected)
        self.assertEqual(score_inventory(row(item_budget_php=0.3, unit_cost_php=0.1)).iloc[0].suggested_quantity, 3)

    def test_fractional_demand_rounds_up(self):
        r = score_inventory(row(daily_usage=0.21, stock_level=0, item_budget_php=10000)).iloc[0]
        self.assertEqual(r.target_stock, 3)
        self.assertEqual(r.suggested_quantity, 3)

    def test_missing_invalid_and_duplicates_rejected(self):
        for bad in [row(stock_level=np.nan), row(daily_usage="unknown"), row(unit_cost_php=0), row(stock_level=-1), row(urgency=6), row(urgency=1.5), row(stock_level=True), row(lead_time_days=np.inf), row(item_name=" "), row(item_budget_php=1.234), pd.concat([row(), row()])]:
            with self.assertRaises(ValueError):
                score_inventory(bad)

    def test_ties_are_stable_across_input_order(self):
        df = pd.concat([row(item_id="Z"), row(item_id="A")], ignore_index=True)
        for method in ["weighted", "rule"]:
            first = rank_inventory(score_inventory(df), method).item_id.tolist()
            second = rank_inventory(score_inventory(df.iloc[::-1]), method).item_id.tolist()
            self.assertEqual(first, ["A", "Z"])
            self.assertEqual(first, second)

    def test_weight_change_and_uncertain_lead_time(self):
        base = row(lead_time_days=7)
        later = row(lead_time_days=14)
        self.assertGreater(score_inventory(later).iloc[0].desired_quantity, score_inventory(base).iloc[0].desired_quantity)
        alternate_input = base.assign(urgency=2)
        self.assertNotEqual(score_inventory(alternate_input).iloc[0].weighted_score, score_inventory(alternate_input, {"shortage": .45, "urgency": .45, "lead_time": .1}).iloc[0].weighted_score)
        with self.assertRaises(ValueError):
            score_inventory(base, {"shortage": 1, "urgency": 1, "lead_time": 1})

    def test_dataset_invariants(self):
        df = pd.read_csv(ROOT / "data" / "inventory.csv")
        self.assertTrue(30 <= len(df) <= 100)
        scores = score_inventory(df)
        self.assertTrue(scores.order_cost_php.le(scores.item_budget_php + 1e-8).all())
        self.assertTrue(scores.suggested_quantity.le(scores.desired_quantity).all())
        self.assertTrue(scores.weighted_score.between(0, 100).all())
        _, metrics = compare_methods(scores)
        self.assertLessEqual(metrics["top_k_overlap"], metrics["top_k"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
