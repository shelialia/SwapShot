from pydantic import BaseModel

class TransactionFee(BaseModel):
    txId: str
    fee_in_usdt: float
    fee_in_eth: float