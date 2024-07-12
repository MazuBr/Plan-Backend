from typing import Optional

import redis

from models.users import TokenData

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_user_token(user_id: int, token_data: TokenData) -> bool:
    try:
        redis_client.set(f"token:{user_id}", token_data.model_dump_json())
        return True
    except Exception as e:
        print(f"Error caching token for user {user_id}: {e}")
        return False

def get_cached_user_token(user_id: int) -> Optional[str]:
    token_data: Optional[bytes] = redis_client.get(f"token:{user_id}")
    if token_data:
        return token_data.decode('utf-8')
    return None

def remove_cache_user_token(user_id: int) -> bool:
    try:
        redis_client.delete(f"token:{user_id}")
        return True
    except Exception as e:
        print(f"Error removing token for user {user_id}: {e}")
        return False
    