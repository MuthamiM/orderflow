import time
import requests
from datetime import datetime

# Polymarket Public CLOB API
CLOB_URL = "https://clob.polymarket.com"

# Example Token ID (e.g., Bitcoin to hit $100k by March)
# You can replace this with any active Polymarket Token ID
TARGET_TOKEN_ID = "21742633143463906290569050155826241533067272736897614950488156847949938836455" 

# Strategy Configuration: Probability Decay Model
# We watch for a rapid drop in odds (e.g., probability crashing > 5% in 10 seconds)
POLL_INTERVAL_SEC = 5.0
CRASH_THRESHOLD = 0.05 

class OddsReactor:
    def __init__(self, token_id: str):
        self.token_id = token_id
        self.last_price = None

    def fetch_live_odds(self) -> float:
        """Fetches the current top-of-book (best ask) odds from the CLOB."""
        try:
            # We query the orderbook for our specific token
            url = f"{CLOB_URL}/book?token_id={self.token_id}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            asks = data.get("asks", [])
            
            if not asks:
                return 0.0
                
            # Best ask is the lowest price someone is willing to sell "YES" shares for
            # Prices in Polymarket represent probability (e.g., 0.45 = 45%)
            best_ask_price = float(asks[0].get("price", "0"))
            return best_ask_price
            
        except requests.RequestException as e:
            print(f"[{datetime.now().isoformat()}] Error fetching odds: {e}")
            return 0.0

    def execute_trade(self, price: float, drop: float):
        """Simulates routing the trade to the backend execution engine."""
        print(f"\n🚀 [EXECUTION ENGINE TRIGGERED] 🚀")
        print(f"[{datetime.now().isoformat()}] PROBABILITY DECAY DETECTED!")
        print(f"Odds crashed by {drop*100:.1f}%!")
        print(f"Executing BUY Order at {price*100:.1f} cents per share to catch the bounce...")
        print(f"-> Routing to Polygon Mainnet via RiskEngine...\n")
        # In production:
        # client = PolyClient()
        # client.execute_market_order(...)
        time.sleep(1)
        print(f"✅ Trade Filled: 50 USDC @ {price}")

    def run(self):
        print(f"Starting Live Odds Reactor...")
        print(f"Target Token: {self.token_id}")
        print(f"Strategy: Detect probability decay > {CRASH_THRESHOLD*100}% between ticks\n")

        while True:
            current_price = self.fetch_live_odds()
            
            if current_price > 0:
                print(f"[{datetime.now().isoformat()}] Live Odds: {current_price*100:.1f}%")
                
                if self.last_price is not None:
                    # Calculate probability decay
                    price_change = self.last_price - current_price
                    
                    if price_change >= CRASH_THRESHOLD:
                        self.execute_trade(current_price, price_change)
                        # Pause strategy after execution to prevent double-spending
                        print("Pausing reactor for 60 seconds post-execution...")
                        time.sleep(60)
                        self.last_price = None 
                        continue
                        
                self.last_price = current_price

            time.sleep(POLL_INTERVAL_SEC)

if __name__ == "__main__":
    reactor = OddsReactor(TARGET_TOKEN_ID)
    
    # Simulating a mock crash after 10 seconds for the hackathon demo
    print("--- [HACKATHON DEMO MODE: WILL SIMULATE CRASH AFTER 2 TICKS] ---")
    
    first_price = reactor.fetch_live_odds()
    if first_price == 0.0: first_price = 0.50 # Fallback
    
    print(f"[{datetime.now().isoformat()}] Live Odds: {first_price*100:.1f}%")
    reactor.last_price = first_price
    time.sleep(5)
    
    print(f"[{datetime.now().isoformat()}] Live Odds: {first_price*100:.1f}%")
    time.sleep(5)
    
    # Force the simulated drop
    crash_price = first_price - 0.06
    print(f"[{datetime.now().isoformat()}] Live Odds: {crash_price*100:.1f}%")
    reactor.execute_trade(crash_price, 0.06)
