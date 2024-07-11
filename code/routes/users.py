from fastapi import APIRouter

from exceptions.users import *
from logic.auth import generate_token, hash_pass
from logic.auto_gen_sqls import auto_gen
from logic.postgres_connection import Database
from models.users import UserCreate, UserResponse
from logic.redis_connection import cache_user_token, get_cached_user_token

user_router = APIRouter()

@user_router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    db = Database()
    new_user = dict

    user_data = user.model_dump()
    user_data['password'] = hash_pass(user.password)
    query = auto_gen(user_data, '''
    INSERT INTO users ({fields})
    VALUES ({values})
    RETURNING id, username, email, first_name, last_name, phone, address;
        ''')
    
    db_response = db.fetch_all(query=query, params=user_data)

    if isinstance(db_response, list):
        pass
    else:
        if 'users_username_key' == db_response.diag.constraint_name:
            raise UsernameAlreadyExistsException
        elif 'users_email_key' == db_response.diag.constraint_name:
            raise EmailAlreadyExistsException
        else:
            raise UnknownRegistrationErrorException
    
    new_user = db_response[0]

    token_data = generate_token(new_user.get('id'))

    cache_user_token(new_user.get('id'), token_data=token_data)

    return UserResponse(id=new_user.get('id'),
                username=new_user.get('username'),
                email=new_user.get('email'),
                first_name=new_user.get('first_name'),
                last_name=new_user.get('last_name'),
                phone=new_user.get('phone'),
                address=new_user.get('address'),
                token_data=token_data, )
