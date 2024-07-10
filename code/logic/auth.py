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


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')
