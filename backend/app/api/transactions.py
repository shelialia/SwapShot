from fastapi import APIRouter, HTTPException
from app.services.exchange_services import get_eth_usdt_price
from app.services.transaction_services import (
    fetch_and_process_transactions,
    fetch_transaction_by_id,
    fetch_and_process_transactions_by_block_range
)

router = APIRouter()

@router.get("/transactions/{txId}")
async def get_transaction_by_hash(txId: str):
    """Fetch a transaction by its hash."""
    transaction = fetch_transaction_by_id(txId)
    return transaction


@router.get("/transaction/{start_time}/{end_time}/{page}/{limit}")
async def get_transaction_by_time_interval(start_time: str, end_time: str, page: int, limit: int = 50):
    """Fetch transactions in the time interval, calculate fees, and return paginated data"""
    try:
        print("Hi I am endpoint 2")
        transactions = await fetch_and_process_transactions_by_block_range(start_time, end_time, page, limit)
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
