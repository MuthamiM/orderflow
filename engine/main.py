from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import uvicorn
from datetime import datetime

import config
from schemas import TradePayload, TradeResponse
# from polymarket_client import PolyClient
# from risk_manager import RiskEngine

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Polymarket Arbitrage Engine")

def verify_webhook_secret(x_webhook_secret: str = Header(...)):
    if x_webhook_secret != config.WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")
    return x_webhook_secret

@app.post("/api/v1/trade", response_model=TradeResponse)
async def execute_trade(payload: TradePayload, secret: str = Depends(verify_webhook_secret)):
    """
    Endpoint called by n8n when a highly confident news event occurs.
    """
    print(f"[{datetime.now().isoformat()}] Received trade signal from n8n: {payload.news_source}")
    print(f"Market ID: {payload.market_id}, Side: {payload.side}, Confidence: {payload.confidence}%")
    
    # Check risk limits
    if payload.confidence < config.MIN_CONFIDENCE_THRESHOLD:
        print(f"Trade rejected: Confidence {payload.confidence} is below threshold {config.MIN_CONFIDENCE_THRESHOLD}")
        return TradeResponse(
            success=False,
            error_message="Confidence below threshold",
            timestamp=datetime.now().isoformat()
        )
        
    # TODO: Initialize Polymarket client and execute trade
    # client = PolyClient()
    # order_result = client.place_order(payload)
    
    # Mock response for now
    return TradeResponse(
        success=True,
        order_id="mock_order_123",
        filled_amount=10.0,
        price_executed=0.45,
        timestamp=datetime.now().isoformat()
    )
    
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
