from app.services.exchange_services import calculate_transaction_fee_in_eth_and_usdt  

def process_transaction(txn, eth_usdt_price):
    gas_price = int(txn["gasPrice"])
    gas_used = int(txn["gasUsed"])

    # Calculate the transaction fee in both ETH and USDT
    fee_in_eth, fee_in_usdt = calculate_transaction_fee_in_eth_and_usdt(
        gas_price, gas_used, eth_usdt_price
    )

    return {
        "txId": txn["hash"],
        "eth_usdt_price": eth_usdt_price,
        "fee_in_usdt": fee_in_usdt,
        "fee_in_eth": fee_in_eth,
        "gasPrice": gas_price,
        "gasUsed": gas_used,
        "timeStamp": txn["timeStamp"],
    }

def process_transaction_id(txn, eth_usdt_price, timestamp):
    gas_price = int(txn["gasPrice"], 16)  # Convert gas price from hex to int
    gas_used = int(txn["gas"], 16)  # Convert gas used from hex to int

    # Calculate the transaction fee in both ETH and USDT
    fee_in_eth, fee_in_usdt = calculate_transaction_fee_in_eth_and_usdt(
        gas_price, gas_used, eth_usdt_price
    )

    # Return the processed transaction data
    return {
        "txId": txn["hash"],
        "eth_usdt_price": eth_usdt_price,
        "fee_in_usdt": fee_in_usdt,
        "fee_in_eth": fee_in_eth,
        "gasPrice": gas_price,
        "gasUsed": gas_used,
        "timeStamp": timestamp
    }
