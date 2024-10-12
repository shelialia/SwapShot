from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Keys
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# API URLs
ETHERSCAN_URL = "https://api.etherscan.io/api"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_HISTORICAL_URL = "https://api.binance.com/api/v3/klines"
UNISWAP_POOL_ADDRESS = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
