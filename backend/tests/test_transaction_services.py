import pytest
from app.services.transaction_services import fetch_and_process_transactions
from unittest.mock import patch

# Mock data for testing
mock_transactions = [
    {
        "timeStamp": "1625097600",
        "gasPrice": "20000000000",
        "gasUsed": "21000",
        "hash": "0x1",
    },
    {
        "timeStamp": "1625097601",
        "gasPrice": "20000000000",
        "gasUsed": "22000",
        "hash": "0x2",
    },
    # Add more transactions as needed for tests
]


# Test fetch_and_process_transactions
@patch(
    "app.services.etherscan.get_uniswap_transactions", return_value=mock_transactions
)
@patch(
    "app.services.exchange_services.get_historical_eth_usdt_price", return_value=3000.0
)
@patch("app.services.helpers.process_transaction")
def test_fetch_and_process_transactions(
    mock_process_transaction, mock_get_historical_price, mock_get_transactions
):
    page = 1
    limit = 50
    mock_process_transaction.side_effect = (
        lambda txn, price: txn
    )  # Just return the transaction itself

    result = fetch_and_process_transactions(page=page, limit=limit)

    assert len(result["transactions"]) == len(mock_transactions)
    assert result["total"] == len(mock_transactions)
    assert result["page"] == page
    assert result["limit"] == limit
    mock_process_transaction.assert_called_with(mock_transactions[0], 3000.0)
