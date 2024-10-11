import json
import os
import time  # Using time.sleep for periodic updates
from datetime import datetime
from app.services.transaction_services import get_uniswap_transactions
from app.services.exchange_services import calculate_transaction_fee_in_eth_and_usdt

CACHE_FILE = "cache.json"


# Function to read the cache from a local file
def read_cache():
    """Read cache data from a file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


# Function to write the cache to a local file
def write_cache(cache_data):
    """Write cache data to a file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f)


# Function to cache a single transaction
def cache_transaction(transaction):
    """Cache each transaction individually using its txId as the key."""
    cache = read_cache()
    cache[f"txn_{transaction['txId']}"] = transaction
    write_cache(cache)


# Function to update the latest retrieval date in cache
def update_lastest_retrieval_date(new_date):
    cache = read_cache()
    cache["last_transaction_date"] = new_date
    write_cache(cache)


# Function to get a cached transaction by txId
def get_cached_transaction(txId):
    """Retrieve a single transaction from the cache using its txId."""
    cache = read_cache()
    return cache.get(f"txn_{txId}")


# Function to detect and cache new transactions
def detect_and_cache_new_transactions():
    cache = read_cache()
    last_transaction_date = cache.get(
        "last_transaction_date", 0
    )  # Default to 0 if no date is present in the cache

    transactions = get_uniswap_transactions()  # Fetch new transactions from the source
    new_transactions = [
        txn
        for txn in transactions
        if int(txn["timeStamp"]) > int(last_transaction_date)
    ]

    if new_transactions:
        # Process new transactions and cache them
        processed_transactions = process_new_transactions(new_transactions)

        for txn in processed_transactions:
            cache_transaction(txn)

        # Update the last transaction date in cache
        latest_transaction_date = new_transactions[-1]["timeStamp"]
        update_lastest_retrieval_date(latest_transaction_date)

    return new_transactions


def process_new_transactions(new_transactions):
    """Loop through new transactions, calculate fees, and return processed transactions."""
    processed_transactions = []

    for txn in new_transactions:
        # Extract gas price and gas used for fee calculation
        gas_price = int(txn["gasPrice"])
        gas_used = int(txn["gasUsed"])

        # Calculate the fee in USDT using the exchange rate
        fee_in_eth, fee_in_usdt = calculate_transaction_fee_in_eth_and_usdt(
            gas_price, gas_used
        )

        # Prepare transaction fee data
        transaction_fee_data = {
            "txId": txn["hash"],
            "fee_in_usdt": fee_in_usdt,
            "fee_in_eth": fee_in_eth,
            "gasPrice": gas_price,
            "gasUsed": gas_used,
            "timeStamp": txn["timeStamp"],  # Include timestamp for future reference
        }

        processed_transactions.append(transaction_fee_data)

    return processed_transactions


# Periodically update the cache (every minute)
def update_cache_periodically():
    while True:
        detect_and_cache_new_transactions()
        time.sleep(60)  # Update every 60 seconds


# Function to retrieve all cached transactions
def get_all_cached_transactions():
    """Retrieve all transactions from the cache."""
    cache = read_cache()
    # Exclude non-transaction keys
    transactions = [value for key, value in cache.items() if key.startswith("txn_")]
    return transactions
