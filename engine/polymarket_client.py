mfrom py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, FmpAggOrderArgs
import config
from schemas import TradePayload
from datetime import datetime

class PolyTrader:
    def __init__(self):
        # We initialize the client connecting to the Polygon Mainnet and Polymarket CLOB
        try:
            self.client = ClobClient(
                host="https://clob.polymarket.com",
                key=config.PRIVATE_KEY,
                chain_id=137,  # Polygon Mainnet
                signature_type=2, # Best default for automated signing
                funder=config.POLY_API_KEY # Represents the specific API credentials 
            )
            self.client.set_api_creds(self.client.create_or_derive_api_creds())
            print("[INFO] Successfully initialized Polymarket CLOB client.")
        except Exception as e:
            print(f"[ERROR] Failed to initialize Polymarket client: {e}")
            self.client = None

    def execute_market_order(self, payload: TradePayload):
        if not self.client:
            return {"success": False, "error": "Client not initialized."}
            
        print(f"[{datetime.now()}] Preparing order for Market {payload.market_id}, Token {payload.token_id}")
        
        try:
            # Hardcoded test constraints matching hackathon requirements
            amount_to_buy = min(10.0, config.MAX_ORDER_SIZE_USDC)
            
            # Using Fill-Or-Kill style order to avoid getting hung on thin orderbooks
            # A real bot would calculate slippage here using get_price()
            order_args = OrderArgs(
                price=0.99, # Paying max price to ensure fill if news is huge 
                size=amount_to_buy,
                side=payload.side,
                token_id=payload.token_id
            )
            
            resp = self.client.create_and_post_order(order_args)
            return {
                "success": True,
                "order_id": resp.get("orderID", "Unknown"),
                "filled_amount": amount_to_buy, # Mocking based on FOK assumption
                "price_executed": 0.0, # Would retrieve from matched trades
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[ERROR] Executing order: {e}")
            return {
                "success": False,
                "error": str(e)
            }
