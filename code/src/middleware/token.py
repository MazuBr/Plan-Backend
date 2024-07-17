import jwt

from src.config import SECRET_KEY, ALGORITHM

async def fetch_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return 'Token expired'
    except jwt.InvalidTokenError:
        print("Invalid token")
        return 'Invalid token'
