import datetime

from models.users import TokenData
from config import SECRET_KEY, ALGORITHM

import bcrypt
import jwt

def generate_token(user_id: str) -> TokenData:
    access_expires_delta = datetime.timedelta(minutes=15)
    access_expires = datetime.datetime.utcnow() + access_expires_delta

    refresh_expires_delta = datetime.timedelta(hours=2)
    refresh_expires = datetime.datetime.utcnow() + refresh_expires_delta

    access_token_payload = {
        "user_id": user_id,
        "exp": access_expires
    }

    refresh_token_payload = {
        "user_id": user_id,
        "exp": refresh_expires
    }

    token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return TokenData(
        token=token,
        refresh_token=refresh_token,
        expires_in=int(access_expires_delta.total_seconds())
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
        print('start decode')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        
        user_id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("user_id")
        return user_id
    except (jwt.InvalidTokenError, jwt.PyJWTError):
        return None


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')

def check_hash_pass(password: str, check_password: str) -> bool:
    return bcrypt.checkpw(check_password.encode('utf-8'), password.encode('utf-8'))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
