# API Reference

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### `GET /health`
Health check endpoint to verify the execution engine is online.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-22T14:30:00.000000"
}
```

---

### `POST /api/v1/trade`
Receives a trade signal from the n8n inference pipeline and executes it against the Polymarket CLOB after risk validation.

**Headers:**
| Header | Required | Description |
| :--- | :---: | :--- |
| `x-webhook-secret` | ✅ | Must match the `WEBHOOK_SECRET` environment variable. Prevents unauthorized trade execution. |

**Request Body:**
```json
{
  "market_id": "string  — The Polymarket condition/market ID",
  "token_id": "string  — The specific token ID (Yes/No share)",
  "side": "BUY | SELL",
  "confidence": 92.5,
  "news_source": "string — The original headline that triggered the signal"
}
```

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `market_id` | `string` | required | Polymarket market identifier |
| `token_id` | `string` | required | Token ID of the share to trade |
| `side` | `enum` | `BUY` or `SELL` | Trade direction |
| `confidence` | `float` | `0.0 – 100.0` | LLM-derived probability score |
| `news_source` | `string` | required | Originating news headline |

**Success Response (`200 OK`):**
```json
{
  "success": true,
  "order_id": "0xabc123...",
  "filled_amount": 10.0,
  "price_executed": 0.45,
  "error_message": null,
  "timestamp": "2026-03-22T14:30:01.000000"
}
```

**Rejection Response (`200 OK`, confidence below threshold):**
```json
{
  "success": false,
  "order_id": null,
  "filled_amount": null,
  "price_executed": null,
  "error_message": "Confidence below threshold",
  "timestamp": "2026-03-22T14:30:01.000000"
}
```

**Error Responses:**
| Status | Cause |
| :--- | :--- |
| `401 Unauthorized` | Invalid or wrong `x-webhook-secret` header |
| `422 Unprocessable Entity` | Missing required header or malformed request body |

---

## Risk Management Rules
All trade payloads are evaluated against these rules before order routing:

| Rule | Value | Effect |
| :--- | :--- | :--- |
| Min Confidence | `85.0%` (configurable) | Payloads below this are rejected |
| Max Order Size | `50.0 USDC` (configurable) | Orders are capped at this ceiling |
| Dynamic Sizing | Kelly Criterion (simplified) | Size scales linearly from 80%–100% confidence |
| Exchange Minimum | `5.0 USDC` | Orders below this are discarded |
