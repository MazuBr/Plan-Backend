import datetime

from fastapi import Response
import bcrypt
import jwt

from src.models.users import TokenData, AccessTokenData
from src.config import SECRET_KEY, ALGORITHM


def generate_token(user_id: str) -> TokenData:
    access_expires_delta = datetime.timedelta(minutes=15)
    access_expires = datetime.datetime.now(datetime.UTC) + access_expires_delta

    refresh_expires_delta = datetime.timedelta(hours=2)
    refresh_expires = datetime.datetime.now(datetime.UTC) + refresh_expires_delta

    access_token_payload = {"user_id": user_id, "exp": access_expires}

    refresh_token_payload = {"user_id": user_id, "exp": refresh_expires}

    token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return TokenData(
        token=token,
        refresh_token=refresh_token,
        expires_in=int(access_expires_delta.total_seconds()),
        expires_refresh_in=int(refresh_expires_delta.total_seconds()),
    )


def decode_token(token: str) -> int:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except (jwt.InvalidTokenError, jwt.PyJWTError):
        return None


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(
        password=password.encode("utf-8"), salt=bcrypt.gensalt()
    ).decode("utf-8")


def check_hash_pass(password: str, check_password: str) -> bool:
    return bcrypt.checkpw(check_password.encode("utf-8"), password.encode("utf-8"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def set_active_auth_coockie(response: Response, user_id: int) -> AccessTokenData:
    token_data = generate_token(user_id=user_id)
    response.set_cookie(
        key="refresh-token",
        value=token_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=token_data.expires_refresh_in,
    )
    return AccessTokenData(token=token_data.token, expires_in=token_data.expires_in)


def set_unactive_auth_coockie(response: Response) -> None:
    response.delete_cookie(key="refresh-token")
    return None
