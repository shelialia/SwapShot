import concurrent 
from app.services.etherscan import get_uniswap_transactions, get_transaction_by_hash, get_block_by_number
from app.services.helpers import process_transaction, process_transaction_id
from app.services.exchange_services import get_historical_eth_usdt_price

def fetch_transaction_by_id(txn_id: int):
    print("Hi Im trying")
    # Fetch the transaction details
    transaction = get_transaction_by_hash(txn_id)
    print(transaction)

    # Extract the block number from the transaction
    block_number = transaction["blockNumber"]

    # Fetch the block details using the block number
    block_details = get_block_by_number(block_number)

    timestamp = int(block_details["timestamp"], 16)
    print(timestamp)

    eth_usdt_price = get_historical_eth_usdt_price(timestamp)

    processed_transaction = process_transaction_id(transaction, eth_usdt_price, timestamp)
    return processed_transaction

async def fetch_transactions_in_time_interval(start_time, end_time):
    start_block = get_block_by_timestamp(start_time)
    end_block = get_block_by_timestamp(end_time)

    if not start_block or not end_block:
        raise HTTPException(status_code=400, detail="Invalid block range")

    # Step 2: Fetch and process transactions based on the block range
    transactions, total_transactions = (
        await fetch_and_process_transactions_by_block_range(
            start_block=start_block,
            end_block=end_block,
            page=page,
            limit=limit,
        )
    )

    # Step 3: Return the paginated transactions and total count
    return {
        "transactions": transactions,
        "total": total_transactions,
        "page": page,
        "limit": limit,
    }


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
