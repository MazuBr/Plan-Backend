from fastapi import APIRouter

from models.users import UserCreate, UserResponse
from logic.auth import generate_token, hash_pass
from logic.auto_gen_sqls import auto_gen
from logic.db_connector import Database

user_router = APIRouter()

@user_router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate):
    db = Database()

    user['password'] = hash_pass(user.password)
    query = auto_gen(user)
    response = db.fetch_all(query=query, params=user)
    token_data = generate_token(user.get('id'))
    print(response)
    return UserResponse(id=user.get('id'),
                username=user.get('username'),
                email=user.get('email'),
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
                phone=user.get('phone'),
                address=user.get('address'),
                token_data=token_data, )
