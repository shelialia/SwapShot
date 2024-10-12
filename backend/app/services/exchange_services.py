import requests
from app.config import BINANCE_URL, BINANCE_HISTORICAL_URL


def calculate_transaction_fee_in_eth_and_usdt(gas_price, gas_used, eth_usdt_price):
    """Calculate the transaction fee in USDT."""
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


def get_historical_eth_usdt_price(epoch_time):
    """Fetch the historical ETH/USDT price from Binance at a specific epoch time."""
    # Convert the epoch time to milliseconds (Binance API uses milliseconds)
    timestamp = epoch_time * 1000

    params = {
        "symbol": "ETHUSDT",
        "interval": "1m",  # Fetching price at a 1-minute interval
        "startTime": timestamp,
        "limit": 1,  # Limit the result to one record
    }

    try:
        response = requests.get(BINANCE_HISTORICAL_URL, params=params)

        # Initialize close_price to None in case the response doesn't meet the conditions
        close_price = None

        # Check if response is successful (status code 200)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()
            close_price = float(data[0][4])  # The 5th element is the 'close' price

        if close_price is None:
            raise Exception("Close price could not be fetched from the API.")

        return close_price

    except Exception as e:
        raise e
