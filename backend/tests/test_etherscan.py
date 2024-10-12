import pytest
import requests
from app.services.etherscan import (
    get_transaction_by_hash,
    get_block_by_number,
    get_block_by_timestamp,
    get_uniswap_transactions,
    get_usdc_eth_transactions_by_block_range,
)

ETHERSCAN_API_KEY = "mock_api_key"
ETHERSCAN_URL = "https://api.etherscan.io/api"
UNISWAP_POOL_ADDRESS = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"


# Test get_transaction_by_hash
def test_get_transaction_by_hash(requests_mock):
    tx_hash = "0x12345"
    mock_response = {
        "status": "1",
        "result": {
            "hash": tx_hash,
            "from": "0xabcde",
            "to": "0xfghij",
            "value": "1000000000000000000",
        },
    }
    requests_mock.get(
        f"{ETHERSCAN_URL}?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={ETHERSCAN_API_KEY}",
        json=mock_response,
    )

    transaction = get_transaction_by_hash(tx_hash)
    assert transaction["hash"] == tx_hash


# Test get_block_by_number
def test_get_block_by_number(requests_mock):
    block_number_hex = "0x10d4f"
    mock_response = {
        "status": "1",
        "result": {
            "timestamp": "1625097600",
            "number": block_number_hex,
        },
    }
    requests_mock.get(
        f"{ETHERSCAN_URL}?module=proxy&action=eth_getBlockByNumber&tag={block_number_hex}&boolean=true&apikey={ETHERSCAN_API_KEY}",
        json=mock_response,
    )

    block = get_block_by_number(block_number_hex)
    assert block["timestamp"] == "1625097600"


# Test get_block_by_timestamp
def test_get_block_by_timestamp(requests_mock):
    timestamp = 1625097600
    block_number = 123456
    mock_response = {
        "status": "1",
        "result": str(block_number),
    }
    requests_mock.get(
        f"{ETHERSCAN_URL}?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={ETHERSCAN_API_KEY}",
        json=mock_response,
    )

    block_num = get_block_by_timestamp(timestamp)
    assert block_num == block_number


# Test get_uniswap_transactions
def test_get_uniswap_transactions(requests_mock):
    mock_response = {
        "status": "1",
        "result": [
            {"hash": "0xabcde", "from": "0x12345", "to": "0x67890", "value": "1000000"}
        ],
    }
    requests_mock.get(
        f"{ETHERSCAN_URL}?module=account&action=tokentx&address={UNISWAP_POOL_ADDRESS}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}&offset=10000&page=1",
        json=mock_response,
    )

    transactions = get_uniswap_transactions()
    assert len(transactions) == 1
    assert transactions[0]["hash"] == "0xabcde"


# Test get_usdc_eth_transactions_by_block_range
def test_get_usdc_eth_transactions_by_block_range(requests_mock):
    start_block = 123456
    end_block = 123460
    mock_response = {
        "status": "1",
        "result": [
            {"hash": "0xabcde", "from": "0x12345", "to": "0x67890", "value": "1000000"}
        ],
    }
    requests_mock.get(
        f"{ETHERSCAN_URL}?module=account&action=tokentx&address={UNISWAP_POOL_ADDRESS}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={ETHERSCAN_API_KEY}&offset=50&page=1",
        json=mock_response,
    )

    transactions = get_usdc_eth_transactions_by_block_range(
        start_block=start_block, end_block=end_block, page=1, limit=50
    )
    assert len(transactions) == 1
    assert transactions[0]["hash"] == "0xabcde"
