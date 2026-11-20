#!/usr/bin/env python3
"""
Comprehensive Unit Test Suite for Solana Autonomous Capital Agent
Tests drift logic, target invariant enforcement, execution planning, and edge cases.
"""

import unittest
from agent import SolanaCapitalAgent, DEFAULT_TARGETS, MINTS

class TestSolanaCapitalAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SolanaCapitalAgent(
            treasury_wallet="DW2MdHEq3qZ6nh9b5YFUoaPnBuuxC8Gz2785kwbbjSAM",
            max_slippage_bps=50,
            rebalance_threshold_pct=0.05
        )

    def test_target_weight_invariant(self):
        """Invariant: Target weights must sum to exactly 1.0 (100%)."""
        total = sum(self.agent.target_allocation.values())
        self.assertAlmostEqual(total, 1.0, places=4)

        # Invalid weights must raise ValueError
        with self.assertRaises(ValueError):
            SolanaCapitalAgent(target_allocation={"SOL": 0.50, "USDC": 0.30})

    def test_zero_aum_handling(self):
        """Zero AUM portfolio must not trigger division by zero or errors."""
        res = self.agent.evaluate_portfolio_drift({})
        self.assertFalse(res["rebalance_needed"])
        self.assertEqual(res["total_aum_usd"], 0.0)
        self.assertEqual(len(res["actions"]), 0)

    def test_drift_evaluation_and_trigger(self):
        """Verify drift detection when SOL is overweight and USDC is underweight."""
        balances = {
            "SOL": 600.0,   # 60% vs target 40% -> +20% drift
            "USDC": 150.0,  # 15% vs target 35% -> -20% drift
            "JTO": 150.0,   # 15% vs target 15% -> 0% drift
            "PYTH": 100.0   # 10% vs target 10% -> 0% drift
        }
        res = self.agent.evaluate_portfolio_drift(balances)
        self.assertTrue(res["rebalance_needed"])
        self.assertEqual(res["total_aum_usd"], 1000.0)

        # Check SOL action: SELL $200
        sol_action = next(a for a in res["actions"] if a["asset"] == "SOL")
        self.assertEqual(sol_action["action"], "SELL")
        self.assertEqual(sol_action["delta_usd"], 200.0)

        # Check USDC action: BUY $200
        usdc_action = next(a for a in res["actions"] if a["asset"] == "USDC")
        self.assertEqual(usdc_action["action"], "BUY")
        self.assertEqual(usdc_action["delta_usd"], 200.0)

    def test_balanced_portfolio_no_rebalance(self):
        """Balanced portfolio within 5% threshold must not trigger rebalance."""
        balanced = {
            "SOL": 410.0,   # 41% (target 40%, drift +1% < 5%)
            "USDC": 340.0,  # 34% (target 35%, drift -1% < 5%)
            "JTO": 150.0,   # 15% (target 15%)
            "PYTH": 100.0   # 10% (target 10%)
        }
        res = self.agent.evaluate_portfolio_drift(balanced)
        self.assertFalse(res["rebalance_needed"])
        self.assertEqual(len(res["actions"]), 0)

    def test_execution_plan_generation(self):
        """Verify execution plan routes through Jupiter v6 with correct mints."""
        balances = {
            "SOL": 600.0,
            "USDC": 150.0,
            "JTO": 150.0,
            "PYTH": 100.0
        }
        plan = self.agent.execute_rebalance_strategy(balances, dry_run=True)
        self.assertEqual(plan["agent_version"], "2.0.0-superteam")
        self.assertEqual(plan["treasury_wallet"], "DW2MdHEq3qZ6nh9b5YFUoaPnBuuxC8Gz2785kwbbjSAM")
        self.assertTrue(plan["dry_run"])

        steps = plan["execution_plan"]
        self.assertEqual(len(steps), 1)  # SOL -> USDC rebalance (USDC absorbs)
        self.assertEqual(steps[0]["type"], "REBALANCE_SELL")
        self.assertEqual(steps[0]["pair"], "SOL -> USDC")
        self.assertEqual(steps[0]["input_mint"], MINTS["SOL"])
        self.assertEqual(steps[0]["output_mint"], MINTS["USDC"])
        self.assertEqual(steps[0]["max_slippage_bps"], 50)

if __name__ == "__main__":
    unittest.main()
