import requests
from app.config import (
    ETHERSCAN_API_KEY,
    ETHERSCAN_URL,
    UNISWAP_POOL_ADDRESS,
)


def get_transaction_by_hash(tx_hash: str):
    """Fetch a transaction by its hash from Etherscan."""
    try:
        params = {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": tx_hash,
            "apikey": ETHERSCAN_API_KEY,
        }

        response = requests.get(ETHERSCAN_URL, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("result"):
            return data["result"]
    except Exception as e:
        raise e


def get_block_by_number(block_number_hex: str):
    """Fetch block details by block number in hex to get the timestamp."""
    params = {
        "module": "proxy",
        "action": "eth_getBlockByNumber",
        "tag": block_number_hex,
        "boolean": "true",
        "apikey": ETHERSCAN_API_KEY,
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    return response.json()["result"]


def get_block_by_timestamp(timestamp: int) -> int:
    """
    Fetch the block number for the given Unix timestamp.
    """
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": "before",
        "apikey": ETHERSCAN_API_KEY,
    }

    response = requests.get(ETHERSCAN_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            return int(data["result"])  # Return block number as integer
        else:
            raise ValueError(f"Error fetching block by timestamp: {data['message']}")
    else:
        raise Exception(f"Error fetching block by timestamp: {response.status_code}")


def get_uniswap_transactions(limit: int = 10000):
    """Fetch 10,000 Uniswap transactions."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": UNISWAP_POOL_ADDRESS,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
        "offset": limit,  # Fetch up to 10,000 transactions in one API call
        "page": 1,  # Only fetch the first page (10,000 transactions)
    }

    response = requests.get(ETHERSCAN_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and "result" in data:
            return data["result"]  # Return the transactions
        else:
            raise Exception(f"Etherscan API error: {data.get('message', 'No result')}")
    else:
        raise Exception(f"Error fetching transactions: {response.status_code}")


def get_usdc_eth_transactions_by_block_range(
    start_block: int, end_block: int, page: int, limit: int
):
    """
    Fetch USDC/ETH transactions from the Uniswap V3 pool by block range using the Etherscan API.
    Handles the case where no transactions are found.
    """
    params = {
        "module": "account",
        "action": "tokentx",  # Fetch token transactions (including token swaps)
        "address": UNISWAP_POOL_ADDRESS,  # Uniswap V3 Pool Address for USDC/ETH
        "startblock": start_block,
        "endblock": end_block,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY,
        "offset": limit,
        "page": page,
    }

    response = requests.get(ETHERSCAN_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["status"] == "1":
            transactions = data.get("result", [])
            if transactions:
                return transactions  # Return the list of transactions
            else:
                return []  # Return an empty list if no transactions are found
        else:
            raise ValueError(
                f"Etherscan API error: {data.get('message', 'No transactions found')}"
            )

    else:
        raise Exception(f"Error fetching transactions: {response.status_code}")
