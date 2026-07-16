from app.services.coingecko import get_coin_price

# Test function for get_coin_price
def test_get_coin_price_valid():
    # Test with a valid cryptocurrency name
    coin_name = "bitcoin"
    price = get_coin_price(coin_name)
    
    # Check if the price is a float and greater than 0
    assert isinstance(price, (int, float)), "The price should be a float."
    assert price > 0, "The price should be greater than 0."
    

def test_get_coin_price_invalid():
    # Test with an invalid cryptocurrency name
    coin_name = "invalidcoin"
    price = get_coin_price(coin_name)
    
    # Check if the price is None for an invalid coin
    assert price is None, "The price should be None for an invalid coin."