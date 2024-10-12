from pydantic import BaseModel

class TransactionFee(BaseModel):
    txId: str
    timestamp_in_epoch_time: str
    eth_usdt_price: float
    fee_in_usdt: float
    fee_in_eth: float
