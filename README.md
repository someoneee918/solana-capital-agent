# Solana Autonomous Capital Agent

An algorithmic capital allocation and portfolio rebalancing agent built on Solana, featuring integration with Jupiter Aggregator v6, drift telemetry, and invariant risk controls.

Built for the **Superteam Earn / OOBE Protocol Bounty ($500 USDC)**.

---

## Architecture & Mechanics

- **Target Asset Allocation:**
  - 40% SOL (Core ecosystem asset)
  - 35% USDC (Stable store-of-value & risk buffer)
  - 15% JTO (Liquid staking governance)
  - 10% PYTH (High-frequency oracle infrastructure)

- **Execution & Routing:**
  - Integrates with **Jupiter Aggregator v6** (`quote-api.jup.ag/v6/quote`) for optimal multi-DEX routing across Raydium, Orca, and Phoenix.
  - Enforces a strict 50 bps (0.5%) maximum slippage constraint.
  - Autonomous drift triggers execute when an asset deviates >5% from target weight.

- **Non-Custodial Design:**
  - Designed for trustless execution using delegated SPL authority, ensuring the agent never requires custody of master private keys.

---

## Quickstart

### 1. Requirements
- Python 3.10+
- Internet connection for Solana Mainnet RPC & Jupiter Aggregator

### 2. Run Local Evaluation
```bash
python3 agent.py
```

### 3. Run Unit Tests
```bash
python3 test_agent.py
```

---

## Payout Destination
- **Solana Mainnet Wallet:** `DuZN1v59Du3A1tXvHSa2W3AA4bGXUVN3Bv3UvBg3C9Rv`

---

## License
MIT
