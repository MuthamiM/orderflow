# n8n Workflow Files

This directory contains the n8n workflow JSON files that power the LLM inference pipeline.

## Setup

1. Start your local n8n instance:
   ```bash
   npx n8n
   ```
2. Open `http://localhost:5678` in your browser.
3. Go to **Workflows → Import from File** and select the `polymarket_arbitrage_workflow.json` file from this directory.
4. Update the final **HTTP Request** node URL to point to your Python execution engine:
   - Local: `http://localhost:8000/api/v1/trade`
   - Via ngrok: `https://YOUR_NGROK_URL.ngrok-free.app/api/v1/trade`
5. Activate the workflow.

## Workflow Overview

The n8n pipeline performs the following steps:
1. **RSS Trigger** – Polls BBC World News RSS feed for breaking headlines.
2. **LLM Node** – Sends the headline to Meta Llama 3 8B-Instruct (via OpenRouter) with a strict binary question about macroeconomic impact.
3. **IF Node** – Filters for confidence scores > 85%.
4. **HTTP Request** – Fires a webhook to the Python FastAPI engine with the structured trade payload.

## Adding Your Workflow

Export your workflow from n8n:
1. Open the workflow in the n8n editor.
2. Click the **⋮** menu → **Download**.
3. Save the `.json` file into this `n8n/` directory.
4. Commit and push.
