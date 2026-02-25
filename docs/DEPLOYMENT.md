# Deployment Guide

This project is configured for automated deployment to **Render** using their Infrastructure-as-Code feature and the Render CLI.

## Prerequisites
1.  A Render account (render.com)
2.  The Render CLI (`npm install -g @render/cli` or download the binary)
3.  A connected GitHub Repository.

## Deploying the Execution Engine (Python)

We have provided a `render.yaml` Blueprint file at the root of the repository. This defines all necessary environment variables, start scripts, and build commands.

### Option 1: Render Dashboard
1. Go to the Render Dashboard.
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository containing this project.
4. Render will automatically detect `render.yaml` and prompt you to fill in the missing secrets (e.g., `POLY_API_KEY`, `PRIVATE_KEY`).
5. Click **Apply**.

### Option 2: Render CLI
If you prefer the terminal:
1. Ensure your code is pushed to your Git remote.
2. Run `render login`
3. Link your project: `render init`
4. Deploy using the blueprint:
```bash
render blueprint apply render.yaml
```
5. You will be prompted in the CLI to enter the required secrets for your Polymarket wallet.

## Deploying the n8n Workflow

For the hackathon, the easiest way to run the n8n orchestrator is locally or on a cheap VPS, as n8n can be resource-intensive for standard serverless free tiers.

**To run locally for the demo:**
```bash
npx n8n
```
1. Open `http://localhost:5678`
2. Go to **Workflows** > **Import from File**.
3. Select `n8n/polymarket_arbitrage_workflow.json`
4. Connect the Webhook node to the URL Render generated for your Python engine.
