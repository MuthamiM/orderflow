# Orderflow 001: The Alpha Feed - Demo Voiceover Script

*(Time: ~2 minutes)*

**[0:00 - 0:15] Visual: Display the GitHub README Architecture section or the n8n canvas.**
"Hello judges, welcome to **The Alpha Feed**. This is our submission for the Orderflow 001 Hackathon, targeting the AI-Augmented Systems track. We built a production-ready, ultra-low-latency arbitrage engine that executes trades on Polymarket."

**[0:15 - 0:40] Visual: Slowly pan across the n8n workflow nodes (left to right).**
"Our edge hypothesis relies on information arbitrage. Human traders often have a latency of minutes to hours when pricing in breaking global news. Our system automates this probabilistic reasoning. On screen is our n8n inference pipeline. It ingests raw BBC and Twitter feeds at millisecond latency, and routes the breaking headlines directly into an OpenRouter Meta Llama 3 model."

**[0:40 - 0:55] Visual: Open the 'Test Step' data panel on the final Trigger Execution Engine node.**
"The AI answers a strict binary question: Does this news severely impact a major macroeconomic prediction market? If the confidence score exceeds our strict 85% threshold, the pipeline fires a securely authenticated webhook directly into our Python FastAPI execution server."

**[0:55 - 1:20] Visual: Switch to the terminal window showing the 'main.py' logs (Webhook interception).**
"As you can see here in the server logs, the Python engine intercepts the webhook. It validates the payload against our Risk Management constraints, ensuring the trade size does not exceed our fixed 50 USDC limit, before wrapping the Polymarket `py_clob_client` to sign and execute a market order on the Polygon blockchain."

**[1:20 - 1:45] Visual: Switch to the second terminal window running `odds_reactor.py`**
"But we didn't stop at just news arbitrage. We also built a standalone live execution engine reacting directly to Polymarket odds dynamically across assets like Gold, Bitcoin, and the S&P 500. This is our Probability Decay Model. It aggressively polls the Limit Order Book. Watch what happens here as it scans the odds..."

**[1:45 - 2:05] Visual: Let the terminal run until the "PROBABILITY DECAY DETECTED!" block prints.**
"...and suddenly we detect an artificial market crash of 6%. The Reactor instantly intercepts the probability decay, sizes a Kelly Criterion bet, and executes a 'buy the dip' order at 44 cents to capture the spread bounce. Finally, it tracks the execution to calculate the post-trade PnL, successfully closing the trade for a profit."

**[2:05 - 2:20] Visual: Show the GitHub repo URL or a 'Thank You' slide.**
"Everything you see is powered by fully decoupled Python pipelines for maximum execution speed, and the entire architecture is live and open-source in our GitHub repository right now. Thank you for your time, and happy building."
