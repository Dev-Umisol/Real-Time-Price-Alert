import jwt
import os

from dotenv import load_dotenv
from app.auth.auth import create_access_token

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

# Test function for create_access_token
def test_create_access_token():
    user_name = "testuser"
    
    # Create an access token using the provided username
    token = create_access_token(user_name)
    
    # Decode the token to verify its contents
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Check if the subject in the payload matches the provided username
    assert decoded_payload["sub"] == user_name, "The subject in the token does not match the provided username."
    
    # Check if the action in the payload is 'login'
    assert decoded_payload["action"] == "login", "The action in the token is not 'login'."
    
    # Check if the expiration time in the payload is set correctly
    assert decoded_payload["exp"] > 0, "The expiration time in the token is not set correctly."