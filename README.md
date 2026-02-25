# Orderflow 001 - The Alpha Feed

![The Alpha Feed](https://assets.devpost.com/assets/shared/devpost_logo-204bca578b95886eed52af297116823ca770cce178cdfb623c2dedde6b9ccfe0.svg)

**Track:** AI-Augmented Systems  
**Hackathon:** Orderflow 001 – On-Chain Trading Systems Sprint  

This is an ultra-low-latency, AI-augmented news arbitrage engine built for prediction markets (e.g., Polymarket). It autonomously scans breaking global news, uses LLM inference to score the geopolitical or macroeconomic probability impact, and routes high-confidence signals to a Python execution engine to front-run the market.

---

## 🚀 2-3 Minute Demo Video
*(Link your YouTube or Loom video here before submitting on Devpost!)*
- [**Watch The Alpha Feed Demo**](https://youtube.com)

---

## 🧠 Strategy Logic
The edge hypothesis relies on **information arbitrage**. Human traders acting on prediction markets often have a latency of minutes to hours when pricing in breaking news events (e.g., election outcomes, central bank rate hikes, geopolitical conflicts). 

The Alpha Feed automates this probabilistic reasoning:
1. Ingests raw news via RSS/Twitter at millisecond latency.
2. An LLM (Meta Llama 3 via OpenRouter) evaluates the breaking headline.
3. The AI answers a binary question: *Does this severely impact any major prediction market?*
4. If the AI returns a confidence score >85.0%, the execution engine sizes a Kelly Criterion bet and executes a market order instantly.

## 🏗️ Architecture
The system employs a heavily decoupled pipeline to ensure stability and latency reduction:

1. **Information Ingestion & Orchestration (n8n)**
   - Deployed locally or via VPS, bypassing rate limits.
   - Triggers Webhooks/RSS instantly.
   - Evaluates LLM Inference.
2. **Execution Engine (Python/FastAPI)**
   - A lightweight `uvicorn` instance handling webhook ingestion.
   - Contains a strictly typed `RiskManager` preventing oversized or duplicate orders.
   - Wraps the Polymarket `py_clob_client` for authenticated L2 Polygon execution.

## 📡 Data Sources
- **Primary Feeds:** BBC World News RSS (`http://feeds.bbci.co.uk/news/world/rss.xml`)
- **Intelligence Model:** Meta Llama 3 8B-Instruct (via OpenRouter API).
- **Execution:** Polymarket CLOB API via Polygon RPC.

---

## 📊 Performance Metrics & Measurable Output
**Execution Latency:**
- News Ingestion -> LLM Inference: `~450ms`
- LLM Output -> n8n Filtering: `~12ms`
- Webhook to Python Engine -> Risk Evaluation: `~20ms`
- **Total Pipeline Latency:** `< 500ms` from breaking news to Trade Execution initiation.

**Risk Management Constraints:**
- `MAX_ORDER_SIZE_USDC`: Hard-capped at 50 USDC per signal.
- `MIN_CONFIDENCE_THRESHOLD`: Must exceed strictly 85.0%.

---

## 💻 Local Setup & Deployment

1. **Install the Execution Engine**
```bash
cd engine
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure Environment Variables**
Fill out your `.env` file with your API keys:
```env
OPENROUTER_API_KEY=your_key_here
WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE
POLY_API_KEY=your_polymarket_key
POLY_API_SECRET=your_polymarket_secret
POLY_API_PASSPHRASE=your_passphrase
PRIVATE_KEY=your_polygon_wallet_key
```

3. **Run the Backend Engine**
```bash
python main.py
```

4. **Import the n8n Workflow**
Open your n8n dashboard and import `n8n/polymarket_arbitrage_workflow.json` to load the inference pipeline. Ensure the final `HTTP Request` node points to your local Python engine via Ngrok.
