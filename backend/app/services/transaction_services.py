import requests
from app.config import (
    ETHERSCAN_API_KEY,
    ETHERSCAN_URL,
    UNISWAP_POOL_ADDRESS,
)

def get_uniswap_transactions(start_block=0, end_block=99999999, page=1, limit=50):
    """Fetch Uniswap transactions with pagination."""
    # Calculate the offset based on page and limit
    offset = (page - 1) * limit

    # Params for the API request
    params = {
        "module": "account",
        "action": "tokentx",
        "address": UNISWAP_POOL_ADDRESS,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
        "offset": offset,  # Correctly calculate the offset
        "page": page,
    }

    # Send the request to Etherscan
    response = requests.get(ETHERSCAN_URL, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        # Ensure the API returned a valid result
        if data["status"] == "1":
            return data["result"]  # Return the transactions list
        else:
            raise Exception(f"Etherscan API error: {data['message']}")
    else:
        raise Exception(f"Error fetching transactions: {response.status_code}")
