from pydantic import BaseModel

class RiskEngine:
    """Evaluates payload and enforces strict downside protection before hitting CLOB"""
    
    @staticmethod
    def evaluate_payload(confidence: float, size_requested: float, max_allowable: float) -> tuple[bool, float, str]:
        # 1. Hard cutoff for LLM hallucination / low confidence
        if confidence < 80.0:
            return False, 0.0, f"Confidence {confidence}% too low. Rejecting trade."
            
        # 2. Size limitation
        final_size = min(size_requested, max_allowable)
        if final_size <= 0:
            return False, 0.0, "Calculated zero or negative order size."
            
        # 3. Dynamic sizing (Kelly Criterion simplified)
        # If the LLM is 99% confident, bet the max. If it's 81% confident, bet a fraction.
        sizing_multiplier = (confidence - 80.0) / 20.0  # Scales from 0.0 to 1.0
        adjusted_size = round(final_size * sizing_multiplier, 2)
        
        # Enforce minimum Polymarket order size (usually ~5 USDC)
        if adjusted_size < 5.0:
             return False, 0.0, f"Adjusted size {adjusted_size} is below exchange minimum."
             
        return True, adjusted_size, "Risk checks passed."
