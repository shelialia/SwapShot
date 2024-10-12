import pytest
import requests_mock
from app.services.exchange_services import (
    calculate_transaction_fee_in_eth_and_usdt,
    get_eth_usdt_price,
    get_historical_eth_usdt_price,
)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_HISTORICAL_URL = "https://api.binance.com/api/v3/klines"


# Test calculate_transaction_fee_in_eth_and_usdt
def test_calculate_transaction_fee_in_eth_and_usdt():
    gas_price = 20000000000  # 20 Gwei
    gas_used = 21000  # Standard gas limit for ETH transfer
    eth_usdt_price = 3000.0  # Example ETH price in USDT

    fee_in_eth, fee_in_usdt = calculate_transaction_fee_in_eth_and_usdt(
        gas_price, gas_used, eth_usdt_price
    )

    assert fee_in_eth == pytest.approx(0.00042, 0.00001)  # 0.00042 ETH
    assert fee_in_usdt == pytest.approx(1.26, 0.01)  # 1.26 USDT (0.00042 * 3000)


# Test get_eth_usdt_price
def test_get_eth_usdt_price(requests_mock):
    mock_response = {"symbol": "ETHUSDT", "price": "2500.00"}
    requests_mock.get(BINANCE_URL, json=mock_response)

    eth_usdt_price = get_eth_usdt_price()
    assert eth_usdt_price == 2500.00


# Test get_historical_eth_usdt_price (success case)
def test_get_historical_eth_usdt_price_success(requests_mock):
    epoch_time = 1625097600
    mock_response = [
        [1625097600000, "3000.00", "3100.00", "2990.00", "3050.00", "100.0"]
    ]
    requests_mock.get(BINANCE_HISTORICAL_URL, json=mock_response)

    price = get_historical_eth_usdt_price(epoch_time)
    assert price == 3050.00  # Close price is the 5th element in the list


# Test get_historical_eth_usdt_price with retries
def test_get_historical_eth_usdt_price_with_retries(requests_mock):
    epoch_time = 1625097600
    mock_response = [
        [1625097600000, "3000.00", "3100.00", "2990.00", "3050.00", "100.0"]
    ]
    requests_mock.get(
        BINANCE_HISTORICAL_URL, status_code=500
    )  # Simulate failure on first try
    requests_mock.get(
        BINANCE_HISTORICAL_URL, json=mock_response
    )  # Success on second try

    price = get_historical_eth_usdt_price(epoch_time, retries=2)
    assert price == 3050.00


# Test get_historical_eth_usdt_price fallback case
def test_get_historical_eth_usdt_price_fallback(requests_mock):
    epoch_time = 1625097600
    requests_mock.get(
        BINANCE_HISTORICAL_URL, status_code=500
    )  # Simulate failure for all retries

    fallback_price = 2000.0
    price = get_historical_eth_usdt_price(
        epoch_time, retries=3, fallback_price=fallback_price
    )
    assert price == fallback_price
