import concurrent 
from app.services.etherscan import (
    get_uniswap_transactions,
    get_transaction_by_hash,
    get_block_by_number,
    get_block_by_timestamp,
    get_usdc_eth_transactions_by_block_range,
)
from app.services.helpers import process_transaction, process_transaction_id
from app.services.exchange_services import get_historical_eth_usdt_price

def fetch_transaction_by_id(txn_id: int):
    # Fetch the transaction details
    transaction = get_transaction_by_hash(txn_id)

    # Extract the block number from the transaction
    block_number = transaction["blockNumber"]

    # Fetch the block details using the block number
    block_details = get_block_by_number(block_number)

    timestamp = int(block_details["timestamp"], 16)

    eth_usdt_price = get_historical_eth_usdt_price(timestamp)

    processed_transaction = process_transaction_id(transaction, eth_usdt_price, timestamp)
    return processed_transaction


async def fetch_and_process_transactions(page: int, limit: int = 50):
    """Fetch and process transactions with server-side pagination."""
    # Fetch all 10,000 transactions in one API call
    transactions = get_uniswap_transactions(limit=10000)

    if not transactions:
        raise ValueError("No transactions found")

    # Calculate the slice for the current page
    start = (page - 1) * limit
    end = start + limit
    paginated_transactions = transactions[start:end]

    # Get ETH/USDT price based on the first transaction's timestamp
    epoch_time = int(paginated_transactions[0]["timeStamp"])
    eth_usdt_price = get_historical_eth_usdt_price(epoch_time)

    # Process transactions and calculate fees
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                lambda txn: process_transaction(txn, eth_usdt_price),
                paginated_transactions,
            )
        )

    return {
        "transactions": results,
        "total": len(transactions),  # Total number of transactions (10,000)
        "page": page,
        "limit": limit,
    }


async def fetch_and_process_transactions_by_block_range(
    start_time: int, end_time: int, page: int, limit: int=50
):
    """
    Fetch and process USDC/ETH transactions within a block range, paginate them,
    and calculate the exchange rate based on the first transaction's timestamp.
    """

    # Step 1: Convert the start and end times to block numbers
    start_block = get_block_by_timestamp(start_time)
    end_block = get_block_by_timestamp(end_time)

    # Step 2: Fetch all transactions within the block range
    transactions = get_usdc_eth_transactions_by_block_range(
        start_block=start_block,
        end_block=end_block,
        page=1,
        limit=10000,  # Fetch up to 10,000 transactions
    )
    # Step 3: Calculate the slice for the current page (pagination)
    start = (page - 1) * limit
    end = start + limit
    paginated_transactions = transactions[start:end]

    if not paginated_transactions:
        raise ValueError(f"No transactions found for page {page}")

    # Step 4: Fetch the exchange rate (ETH/USDT) only once based on the first transaction's timestamp
    epoch_time = int(paginated_transactions[0]["timeStamp"])
    eth_usdt_price = get_historical_eth_usdt_price(epoch_time)

    # Step 5: Process the paginated transactions and calculate fees using the exchange rate
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                lambda txn: process_transaction(txn, eth_usdt_price),
                paginated_transactions,
            )
        )

    # Step 6: Return paginated results and total transaction count
    return {
        "transactions": results,
        "total": len(transactions),  # Total number of transactions (from block range)
        "page": page,
        "limit": limit,
    }
