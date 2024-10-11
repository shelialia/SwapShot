from fastapi import APIRouter, HTTPException
from app.services.transaction_services import get_uniswap_transactions
from app.cache.transaction_cache import (
    get_cached_transaction,
    cache_transaction,
    get_all_cached_transactions,
    process_new_transactions,
)
from app.models.models import TransactionFee

router = APIRouter()


@router.get("/transactions/{txId}", response_model=TransactionFee)
def get_transaction_fee(txId: str):
    """Get transaction fee for a given txId."""
    try:
        # Try fetching the transaction from the cache
        cached_transaction = get_cached_transaction(txId)

        if cached_transaction:
            # If the transaction is cached, return it
            return cached_transaction

        # If not in cache, fetch transactions from Uniswap API
        transactions = get_uniswap_transactions()

        # Search for the transaction by txId
        transaction = next((txn for txn in transactions if txn["hash"] == txId), None)

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Process and cache the transaction
        processed_transaction = process_new_transactions([transaction])
        cache_transaction(processed_transaction[0])

        return processed_transaction[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions")
def get_transactions(
    start_time: int = None,  # start time in Unix timestamp
    end_time: int = None,  # end time in Unix timestamp
    page: int = 1,
    limit: int = 50,
):
    """Get paginated transactions within the time range."""
    try:
        # Try fetching transactions from the cache
        transactions = get_all_cached_transactions()

        # If cache is empty, fetch from Uniswap API and cache the data
        if not transactions:
            transactions = get_uniswap_transactions()
            processed_transactions = process_new_transactions(transactions)
            for txn in processed_transactions:
                cache_transaction(txn)
            transactions = processed_transactions

        # Filter transactions by timestamp if start_time and end_time are provided
        if start_time is not None and end_time is not None:
            filtered_transactions = [
                txn
                for txn in transactions
                if start_time <= int(txn["timeStamp"]) <= end_time
            ]
        else:
            filtered_transactions = transactions

        # Pagination logic: Calculate the start and end indexes for the current page
        start_index = (page - 1) * limit
        end_index = start_index + limit

        # Ensure indices are within bounds
        total_count = len(filtered_transactions)
        paginated_transactions = filtered_transactions[start_index:end_index]

        return {
            "transactions": paginated_transactions,
            "total": total_count,
            "page": page,
            "limit": limit,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
