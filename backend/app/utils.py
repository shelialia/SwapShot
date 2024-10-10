import requests
from config import BINANCE_URL

def get_eth_usdt_price():
    """Fetch the latest ETH/USDT price from Binance."""
    params = {"symbol": "ETHUSDT"}
    response = requests.get(BINANCE_URL, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        raise Exception("Error fetching ETH/USDT price")

if __name__ == "__main__":
    print(get_eth_usdt_price())
