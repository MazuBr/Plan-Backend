from typing import Optional

import redis

from models.users import TokenData

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_user_token(user_id: int, token_data: TokenData) -> None:
    redis_client.set(f"token:{user_id}", token_data.model_dump_json())

def get_cached_user_token(user_id: int) -> Optional[str]:
    token_data: Optional[bytes] = redis_client.get(f"token:{user_id}")
    if token_data:
        return token_data.decode('utf-8')
    return None
