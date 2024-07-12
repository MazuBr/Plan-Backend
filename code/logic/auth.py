import datetime

from models.users import TokenData
from config import SECRET_KEY, ALGORITHM

import bcrypt
import jwt

def generate_token(user_id: int) -> TokenData:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    refresh_expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    refresh_token = jwt.encode({"user_id": user_id, "exp": refresh_expire}, SECRET_KEY, algorithm=ALGORITHM)
    return TokenData(
        token=token,
        refresh_token=refresh_token,
        expires_in=3600
    )

def refresh_token(refresh_token: str) -> TokenData:
    try:
        decoded_refresh_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_refresh_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token")

    return generate_token(user_id)

def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        return user_id
    except jwt.PyJWTError:
        return None


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')

def check_hash_pass(password: str, check_password: str) -> bool:
    return bcrypt.checkpw(check_password.encode('utf-8'), password.encode('utf-8'))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
