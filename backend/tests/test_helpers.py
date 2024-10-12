import pytest
from app.services.transaction_services import process_transaction, process_transaction_id

# Sample mock transaction data
mock_transaction = {
    "hash": "0x12345",
    "gasPrice": "10000000000",  # In wei
    "gasUsed": "21000",  # Standard gas for simple ETH transfer
    "timeStamp": "1625097600",
}

mock_transaction_with_hex = {
    "hash": "0x12345",
    "gasPrice": "0x2540be400",  # Hex value for 10000000000 wei
    "gas": "0x5208",  # Hex value for 21000 gas
}


# Test for process_transaction
def test_process_transaction(mocker):
    # Mocking the calculate_transaction_fee_in_eth_and_usdt function
    mocker.patch(
        "app.services.exchange_services.calculate_transaction_fee_in_eth_and_usdt",
        return_value=(0.00021, 500),
    )

    eth_usdt_price = 2500  # Example price of ETH in USDT
    processed_tx = process_transaction(mock_transaction, eth_usdt_price)

    assert processed_tx["txId"] == "0x12345"
    assert processed_tx["eth_usdt_price"] == 2500
    assert processed_tx["fee_in_eth"] == 0.00021
    assert processed_tx["fee_in_usdt"] == 500
    assert processed_tx["gasPrice"] == 10000000000
    assert processed_tx["gasUsed"] == 21000
    assert processed_tx["timeStamp"] == "1625097600"


# Test for process_transaction_id
def test_process_transaction_id(mocker):
    # Mocking the calculate_transaction_fee_in_eth_and_usdt function
    mocker.patch(
        "app.services.exchange_services.calculate_transaction_fee_in_eth_and_usdt",
        return_value=(0.00021, 500),
    )

    eth_usdt_price = 2500  # Example price of ETH in USDT
    timestamp = "1625097600"  # Example timestamp

    processed_tx = process_transaction_id(
        mock_transaction_with_hex, eth_usdt_price, timestamp
    )

    assert processed_tx["txId"] == "0x12345"
    assert processed_tx["eth_usdt_price"] == 2500
    assert processed_tx["fee_in_eth"] == 0.00021
    assert processed_tx["fee_in_usdt"] == 500
    assert processed_tx["gasPrice"] == 10000000000
    assert processed_tx["gasUsed"] == 21000
    assert processed_tx["timeStamp"] == "1625097600"
