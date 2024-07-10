import datetime

from models.Users import TokenData
from config import SECRET_KEY, ALGORITHM

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
