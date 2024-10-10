from fastapi import APIRouter, HTTPException
from services import get_uniswap_transactions, calculate_transaction_fee_in_usdt
from models import TransactionFee

router = APIRouter()

@router.get("/transactions/{txId}", response_model=TransactionFee)
def get_transaction_fee(txId: str):
    """Get transaction fee for a given txId."""
    try:
        transactions = get_uniswap_transactions()
        transaction = next(
            (txn for txn in transactions["result"] if txn["hash"] == txId), None
        )

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        gas_price = int(transaction["gasPrice"])
        gas_used = int(transaction["gasUsed"])
        fee_in_usdt = calculate_transaction_fee_in_usdt(gas_price, gas_used)

        return {
            "txId": txId,
            "fee_in_usdt": fee_in_usdt,
            "fee_in_eth": (gas_price * gas_used) / (10**18),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(get_transaction_fee("0x8395927f2e5f97b2a31fd63063d12a51fa73438523305b5b30e7bec6afb26f48"))
