#!/usr/bin/env python3
"""
Unit Test Suite for Solana Capital Agent
"""

import unittest
from agent import SolanaCapitalAgent

class TestSolanaCapitalAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SolanaCapitalAgent(treasury_wallet="DuZN1v59Du3A1tXvHSa2W3AA4bGXUVN3Bv3UvBg3C9Rv")

    def test_drift_evaluation(self):
        balances = {
            "SOL": 550.0,
            "USDC": 200.0,
            "JTO": 150.0,
            "PYTH": 100.0
        }
        drift = self.agent.evaluate_portfolio_drift(balances)
        self.assertTrue(drift["rebalance_needed"])
        self.assertEqual(len(drift["actions"]), 2)
        self.assertEqual(drift["actions"][0]["asset"], "SOL")
        self.assertEqual(drift["actions"][0]["action"], "SELL")

    def test_balanced_portfolio(self):
        balanced = {
            "SOL": 400.0,
            "USDC": 350.0,
            "JTO": 150.0,
            "PYTH": 100.0
        }
        drift = self.agent.evaluate_portfolio_drift(balanced)
        self.assertFalse(drift["rebalance_needed"])

if __name__ == "__main__":
    unittest.main()
