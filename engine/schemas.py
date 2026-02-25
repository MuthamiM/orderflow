from pydantic import BaseModel, Field
from typing import Optional, Literal

class TradePayload(BaseModel):
    """Payload received from n8n webhook after LLM processing."""
    market_id: str = Field(..., description="The Polymarket condition/market ID")
    token_id: str = Field(..., description="The specific token ID to buy (Yes/No)")
    side: Literal["BUY", "SELL"] = Field(..., description="Trade direction")
    confidence: float = Field(..., ge=0.0, le=100.0, description="LLM derived confidence score (0-100)")
    news_source: str = Field(..., description="The original news headline/source")
    
class TradeResponse(BaseModel):
    """Response sent back to n8n after execution attempt."""
    success: bool
    order_id: Optional[str] = None
    filled_amount: Optional[float] = None
    price_executed: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: str
