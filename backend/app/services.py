import requests
from config import ETHERSCAN_API_KEY, ETHERSCAN_URL, UNISWAP_POOL_ADDRESS

def get_uniswap_transactions(start_block=0, end_block=99999999):
    """Fetch Uniswap transactions from the Etherscan API."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": UNISWAP_POOL_ADDRESS,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error fetching transactions")

if __name__ == '__main__':
    print(get_uniswap_transactions())