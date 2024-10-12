import requests
from app.config import BINANCE_URL, BINANCE_HISTORICAL_URL
import time

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


def get_historical_eth_usdt_price(epoch_time, retries=3, fallback_price=2000.0):
    """
    Fetch the historical ETH/USDT price from Binance at a specific epoch time.
    If the fetch fails, retry up to `retries` times and use a fallback price if necessary.
    """
    # Convert the epoch time to milliseconds (Binance API uses milliseconds)
    timestamp = epoch_time * 1000

    params = {
        "symbol": "ETHUSDT",
        "interval": "1m",  # Fetching price at a 1-minute interval
        "startTime": timestamp,
        "limit": 1,  # Limit the result to one record
    }

    attempt = 0
    close_price = None

    # Retry logic in case of failures
    while attempt < retries:
        try:
            response = requests.get(BINANCE_HISTORICAL_URL, params=params)

            # Check if response is successful (status code 200)
            if response.status_code == 200 and len(response.json()) > 0:
                data = response.json()
                close_price = float(data[0][4])  # The 5th element is the 'close' price

            if close_price is not None:
                return close_price  # Return the fetched price if successful

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")

        # Wait before retrying
        attempt += 1
        time.sleep(1)  # Optional delay between retries

    # If all retries fail, return the fallback price
    print(f"All attempts failed. Returning fallback price: {fallback_price}")
    return fallback_price
