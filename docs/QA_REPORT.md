# Quality Assurance & Testing Report

## 1. Executive Summary
This document outlines the Quality Assurance (QA) strategy and testing procedures for **The Alpha Feed**, an ultra-low-latency, AI-augmented news arbitrage engine built for the Orderflow 001 Hackathon. 

Given the high-risk nature of autonomous trading on prediction markets (Polymarket), the QA strategy emphasizes strict downside protection, secure data ingestion, and deterministic risk management. 

## 2. Testing Strategy
The testing approach is broken down into two primary components:
1. **API & Security Testing:** Ensuring that the webhook ingestion endpoint is secure, authenticated, and resilient to unauthorized or malformatted payloads.
2. **Risk Management Evaluation:** Validating that the `RiskManager` strictly enforces sizing limits, confidence thresholds, and minimum exchange bounds before triggering any orders to the Central Limit Order Book (CLOB).

---

## 3. Unit Test Coverage (`test_main.py`)
The FastApi execution engine is backed by a suite of unit tests utilizing `pytest` and `fastapi.testclient`.

| Test Case | Description | Expected Outcome |
| :--- | :--- | :--- |
| `test_health_check` | Validates that the engine is online and responding to basic uptime pings. | Returns `200 OK` with status `healthy`. |
| `test_missing_webhook_secret` | Submits a valid trade payload but omits the `x-webhook-secret` header to test endpoint security. | Returns `422 Unprocessable Entity` (Missing Authorization). |
| `test_invalid_webhook_secret` | Submits a trade payload with an incorrect `x-webhook-secret` to test authentication constraints. | Returns `401 Unauthorized`. |
| `test_valid_trade_payload` | Simulates an incoming LLM inference signal with high confidence (>90%) and correct credentials. | Returns `200 OK` with `success: True`. |
| `test_low_confidence_rejection` | Simulates an incoming LLM inference signal that fails the mandatory confidence threshold (e.g., 85% when 90% is required). | Returns `200 OK`, but payload parsing completes with `success: False` and an error message identifying the rejection reason. |

---

## 4. Risk Engine Constraints (`risk_manager.py`)
The `RiskEngine.evaluate_payload` method acts as a firewall between the LLM and the Polymarket exchange. The following rules are deterministically enforced and continually QA tested:

1. **Hard Confidence Cutoff:** Any probability score below **80.0%** is outright rejected to prevent autonomous hallucination trading.
2. **Dynamic Position Sizing (Simplified Kelly Criterion):** Order size scales linearly bounded between 80.0% (minimum) and 100% (maximum) confidence mapping to a fractional allocation. If the confidence is exactly 80.0%, no trade executes. If confidence is 90.0%, 50% of the max allowable size is executed.
3. **Cap Limitation:** Order size will mathematically never exceed the `max_allowable` value passed by the environment configurations (hard-capped).
4. **Exchange Minimums Validation:** If the dynamically calculated size falls below Polymarket's exchange minimum limit (e.g., `5.0 USDC`), the payload is discarded to avoid CLOB routing errors.

---

## 5. How to Run the Tests Locally

Before deploying the execution engine, it is highly recommended to run the full QA suite to verify environmental configurations and risk logic.

**Steps:**
1. Navigate to the `engine` directory.
```bash
cd engine
```
2. Activate your virtual environment.
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
3. Install the testing dependencies (if not already installed).
```bash
pip install pytest httpx
```
4. Run the suite against `test_main.py`.
```bash
pytest test_main.py -v
```

Upon a successful test run, all 5 cases should pass, confirming that both the API security middleware and risk manager logic are functioning as expected.
