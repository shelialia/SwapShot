import requests
from app.config import (
    ETHERSCAN_API_KEY,
    ETHERSCAN_URL,
    UNISWAP_POOL_ADDRESS,
    BINANCE_URL,
)

def get_uniswap_transactions(start_block=0, end_block=99999999):
    """Fetch Uniswap transactions from the Etherscan API."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": UNISWAP_POOL_ADDRESS,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error fetching transactions")


def calculate_transaction_fee_in_usdt(gas_price, gas_used):
    """Calculate the transaction fee in USDT."""
    eth_usdt_price = get_eth_usdt_price()
    gas_fee_eth = (gas_price * gas_used) / (10**18)  # Convert to ETH
    gas_fee_usdt = gas_fee_eth * eth_usdt_price
    return gas_fee_usdt


def get_eth_usdt_price():
    """Fetch the latest ETH/USDT price from Binance."""
    params = {"symbol": "ETHUSDT"}
    response = requests.get(BINANCE_URL, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        raise Exception("Error fetching ETH/USDT price")
