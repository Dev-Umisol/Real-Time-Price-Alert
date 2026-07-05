import httpx

# Fetches the price of a given cryptocurrency in USD
def get_coin_price(coin_name: str) -> float | None:
    response = httpx.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd")
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        return data.get(coin_name, {}).get("usd")
    
    return None