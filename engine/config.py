import os
from dotenv import load_dotenv

load_dotenv()

# Polymarket / Polygon configuration
POLY_API_KEY = os.getenv("POLY_API_KEY", "")
POLY_API_SECRET = os.getenv("POLY_API_SECRET", "")
POLY_API_PASSPHRASE = os.getenv("POLY_API_PASSPHRASE", "")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

# Webhook Security
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default-dev-secret-change-me")

# Risk limits
MAX_ORDER_SIZE_USDC = float(os.getenv("MAX_ORDER_SIZE_USDC", "50.0"))
MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "85.0"))
