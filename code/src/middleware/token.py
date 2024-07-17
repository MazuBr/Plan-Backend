import jwt

from src.config import SECRET_KEY, ALGORITHM

async def fetch_token(token: str, refresh_token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return 'Token expired'
    except jwt.InvalidTokenError:
        print("Invalid token")
        return 'Invalid token'

async def fetch_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None