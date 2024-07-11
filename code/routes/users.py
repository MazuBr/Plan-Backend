from fastapi import APIRouter, HTTPException

from models.users import UserCreate, UserResponse
from logic.auth import generate_token, hash_pass
from logic.auto_gen_sqls import auto_gen
from logic.db_connector import Database
from exceptions.users import *

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

    if db_response is list:
        pass
    elif 'users_username_key' == db_response.diag.constraint_name:
        raise UsernameAlreadyExistsException
    elif 'users_email_key' == db_response.diag.constraint_name:
        raise EmailAlreadyExistsException
    else:
        raise UnknownRegistrationErrorException
    
    new_user = db_response[0]

    token_data = generate_token(new_user.get('id'))
    return UserResponse(id=new_user.get('id'),
                username=new_user.get('username'),
                email=new_user.get('email'),
                first_name=new_user.get('first_name'),
                last_name=new_user.get('last_name'),
                phone=new_user.get('phone'),
                address=new_user.get('address'),
                token_data=token_data, )
