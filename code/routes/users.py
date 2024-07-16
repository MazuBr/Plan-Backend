from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer

from exceptions.users import *

from logic.auth import decode_token, generate_token, hash_pass, verify_password,\
    set_active_auth_coockie, set_unactive_auth_coockie

from logic.auto_gen_sqls import auto_gen
from logic.postgres_connection import Database
from models.users import *
from logic.redis_connection import cache_user_token, remove_cache_user_token

user_router = APIRouter()
aouth2_scheme = OAuth2PasswordBearer(tokenUrl='access-token')
aouth2_refresh_scheme = OAuth2PasswordBearer(tokenUrl='refresh-token')

@user_router.post("/create", response_model=UserResponse)
async def create_user(response: Response, user: UserCreate):
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
    set_active_auth_coockie(response=response, token_data=token_data)
    cache_user_token(user_id=new_user.get('id'), token_data=token_data)

    return UserResponse(id=new_user.get('id'),
                username=new_user.get('username'),
                email=new_user.get('email'),
                first_name=new_user.get('first_name'),
                last_name=new_user.get('last_name'),
                phone=new_user.get('phone'),
                address=new_user.get('address'),
                token_data=token_data, )


@user_router.post("/login", response_model=TokenData)
async def login(response: Response, user: LoginRequest):
    db = Database()
    query = "SELECT * FROM users WHERE username = %(identifier)s OR email = %(identifier)s"
    params = {"identifier": user.identifier}
    db_response = db.fetch_all(query=query, params=params)
    db_user: dict = db_response[0] if db_response else None

    if not db_user or not verify_password(user.password, db_user.get("password")):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token_data = generate_token(db_user["id"])
    
    cache_user_token(user_id=db_user["id"], token_data=token_data)
    set_active_auth_coockie(response=response, token_data=token_data)

    return token_data


@user_router.post("/logout", response_model=LogoutResponse)
async def logout_user(response: Response, token: str = Depends(aouth2_scheme)):
    user_id = decode_token(token)
    set_unactive_auth_coockie(response=response)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    remove_cache_user_token(user_id=user_id)
    return LogoutResponse(detail="Successfully logged out")


@user_router.post('/refresh-token')
async def refresh_token(request: Request):
    access_token = request.cookies.get('access_token')
    if access_token:
        print(access_token)
    else:
        print('Токена нет')
    return None