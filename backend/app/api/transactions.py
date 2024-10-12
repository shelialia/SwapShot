from fastapi import APIRouter, HTTPException
# from app.cache.transaction_cache import (
#     get_transaction_by_id,
#     get_all_cached_transactions,
# )
from app.models.transaction import TransactionFee
from app.services.exchange_services import get_eth_usdt_price
from app.services.transaction_services import (
    fetch_and_process_transactions,
    fetch_transaction_by_id,
)

router = APIRouter()

@router.get("/transactions/{txId}")
async def get_transaction_by_hash(txId: str):
    """Fetch a transaction by its hash."""
    transaction = fetch_transaction_by_id(txId)
    return transaction


@router.get("/transactions")
async def get_transactions(
    start_time: str,  # Required start time in Unix
    end_time: str ,  # Required end time in Unix
    page: int,
    limit: int
):
    """
    Fetch transactions within the specified time range using block numbers and return paginated results.
    """

    try:
        # Step 1: Fetch the block numbers for the given start and end times
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
    try:
        transactions = await fetch_and_process_transactions(page, limit)
        return transactions
    except Exception as e:
        raise e


@router.get("/all_transactions/{page}/{limit}")
async def get_all_transactions(page: int, limit: int = 50):
    """Fetch transactions, calculate fees, and return paginated data."""
    try:
        transactions = await fetch_and_process_transactions(page, limit)
        return transactions
    except Exception as e:
        raise e


@router.get("/exchange_rate")
def get_exchange_rate():
    try: 
        rate = get_eth_usdt_price()
        return rate
    except Exception as e:
        raise e
