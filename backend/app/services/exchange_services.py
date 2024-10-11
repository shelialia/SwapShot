import requests
from app.config import BINANCE_URL

def calculate_transaction_fee_in_eth_and_usdt(gas_price, gas_used):
    """Calculate the transaction fee in USDT."""
    eth_usdt_price = get_eth_usdt_price()
    gas_fee_eth = (gas_price * gas_used) / (10**18)  # Convert to ETH
    gas_fee_usdt = gas_fee_eth * eth_usdt_price
    return gas_fee_eth, gas_fee_usdt


def get_eth_usdt_price():
    """Fetch the latest ETH/USDT price from Binance."""
    params = {"symbol": "ETHUSDT"}
    response = requests.get(BINANCE_URL, params=params)
    
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        raise Exception("Error fetching ETH/USDT price")
