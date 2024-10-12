# import json
# import os
# import time
# import concurrent.futures
# from datetime import datetime
# from threading import Thread
# from app.services.transaction_services import get_uniswap_transactions
# from app.services.exchange_services import (
#     calculate_transaction_fee_in_eth_and_usdt,
#     get_historical_eth_usdt_price,
# )

# CACHE_FILE = "cache.json"
# CACHE_TTL_SECONDS = 2  # Set TTL to 2 seconds


# # Function to read the cache from a local file
# def read_cache():
#     """Read cache data from a file."""
#     if os.path.exists(CACHE_FILE):
#         try:
#             with open(CACHE_FILE, "r") as f:
#                 return json.load(f)
#         except Exception as e:
#             print(f"Error reading cache: {e}")
#             return {}
#     return {}


# # Function to write the cache to a local file
# def write_cache(cache_data):
#     """Write cache data to a file."""
#     try:
#         with open(CACHE_FILE, "w") as f:
#             json.dump(cache_data, f)
#     except Exception as e:
#         print(f"Error writing cache: {e}")

# # Function to process the transaction by calculating the fees and storing required data in the cache
# def process_transaction(txn, eth_usdt_price):
#     gas_price = int(txn["gasPrice"])
#     gas_used = int(txn["gasUsed"])

#     fee_in_eth, fee_in_usdt = calculate_transaction_fee_in_eth_and_usdt(
#         gas_price, gas_used, eth_usdt_price
#     )

#     return {
#         "txId": txn["hash"],
#         "eth_usdt_price": eth_usdt_price,
#         "fee_in_usdt": fee_in_usdt,
#         "fee_in_eth": fee_in_eth,
#         "gasPrice": gas_price,
#         "gasUsed": gas_used,
#         "timeStamp": txn["timeStamp"],
#     }


# # Function to refresh cache every 2 seconds
# def refresh_cache():
#     while True:
#         try:
#             transactions = get_uniswap_transactions()
#             cache = read_cache()

#             if transactions:
#                 epoch_time = int(transactions[0]["timeStamp"])  # Use the first transaction's time
#                 eth_usdt_price = get_historical_eth_usdt_price(epoch_time)

#                 with concurrent.futures.ThreadPoolExecutor() as executor:
#                     # Pass the fetched price to the process_transaction function
#                     results = list(
#                         executor.map(
#                             lambda txn: process_transaction(txn, eth_usdt_price),
#                             transactions[:10000],
#                         )
#                     )

#                 cache["transactions"] = results
#                 cache["last_updated_time"] = datetime.now().timestamp()
#                 write_cache(cache)

#         except Exception as e:
#             print(f"Error refreshing cache: {e}")

#         time.sleep(CACHE_TTL_SECONDS)


# # Function to get all cached transactions
# def get_all_cached_transactions():
#     """Get all transactions from the cache."""
#     cache = read_cache()
#     return cache["transactions"]


# # Function to get a transaction by its ID
# def get_transaction_by_id(txn_id):
#     cache = read_cache()
#     result = None
#     for txn in cache.get("transactions", []):  # Fixed the key "transactions"
#         if txn["txId"] == txn_id:
#             result = txn
#             break
#     if result:
#         return {
#             "txId": result["txId"],
#             "eth_usdt_price": result["eth_usdt_price"],
#             "fee_in_usdt": result["fee_in_usdt"],
#             "fee_in_eth": result["fee_in_eth"],
#             "timestamp_in_epoch_time": result["timeStamp"]
#         }


# # Start cache refresh in a separate thread
# def start_cache_refresh():
#     """Start the cache refresh thread."""
#     print("Start running cache refresh thread")
#     cache_refresh_thread = Thread(target=refresh_cache, daemon=True)
#     cache_refresh_thread.start()


# # Call this function at the beginning of your FastAPI app to start the cache refreshing task

# start_cache_refresh()
