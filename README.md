# Orderflow 001 - The Alpha Feed (Execution Engine)

This is a high-speed prediction market execution engine designed for the **Orderflow 001 Hackathon (AI-Augmented Systems Track)**.

## Architecture

1.  **n8n Orchestrator:** Located in the `n8n/` folder. Import this JSON into your n8n instance. It listens to breaking news (RSS), uses OpenAI to score geopolitical/macro impact, and routes high-confidence signals to the engine.
2.  **FastAPI Execution Engine:** Located in `engine/`. Handles risk constraints (sizing, sanity checks) and executes orders on Polygon via the Polymarket `py_clob_client`.

## Running the Engine

1. `cd engine`
2. `python -m venv venv`
3. Windows: `venv\Scripts\activate` (Mac/Linux: `source venv/bin/activate`)
4. `pip install -r requirements.txt`
5. Fill out your `.env` file with your Polymarket API keys and Polygon Private Key.
6. Run the server: `python main.py`

## Next Steps for Hackathon Submission
- Create a 2-3 minute video showing the n8n flow capturing a simulated news event, the webhook firing to the terminal, and the Python engine parsing the payload.
