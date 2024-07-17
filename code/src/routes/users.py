from fastapi import APIRouter, Response, Request
from fastapi.security import HTTPBearer

from src.exceptions.users import *

from src.logic.auth import decode_token, generate_token, hash_pass, verify_password,\
    set_active_auth_coockie, set_unactive_auth_coockie
from src.logic.auto_gen_sqls import auto_gen
from src.logic.postgres_connection import Database
from src.models.users import *

user_router = APIRouter()
auth_scheme = HTTPBearer()

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
    
    return UserResponse(id=new_user.get('id'),
                username=new_user.get('username'),
                email=new_user.get('email'),
                first_name=new_user.get('first_name'),
                last_name=new_user.get('last_name'),
                phone=new_user.get('phone'),
                address=new_user.get('address'),)


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
    
    set_active_auth_coockie(response=response, token_data=token_data)

    return token_data


@user_router.post("/logout", response_model=LogoutResponse)
async def logout_user(request: Request, response: Response):
    token = request.cookies.get("access-token")
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    set_unactive_auth_coockie(response=response)
    return LogoutResponse(detail="Successfully logged out")


@user_router.post("/check-session", response_model=CheckSessionResponse)
async def check_session(request: Request):
    token = request.cookies.get("access-token")
    
    if not token or not decode_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return CheckSessionResponse(detail="Token is valid")

