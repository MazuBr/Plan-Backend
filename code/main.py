from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.config import PORT
from src.logic.auth import update_token
from src.middleware.token import fetch_token
from src.routes.users import user_router

BASE_PATH = '/api'

app = FastAPI(root_path=BASE_PATH)
app.add_middleware(CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def token_middleware(response: Response, request: Request, call_next):
    paths = ["/user/create", "/user/login", '/docs', '/openapi.json']
    excluded_paths = [BASE_PATH + path for path in paths]

    if request.url.path in excluded_paths or request.method == "OPTIONS":
        return await call_next(request)

    token = request.cookies.get("access-token")
    refresh_token = request.cookies.get('refresh-token')

    token_data = await fetch_token(token)
    if token_data == 'Token expired':
        update_token(refresh_token, response)
        return JSONResponse(status_code=401, content={'detail': 'Token expire'})
    if not token_data or token_data == 'Invalid token':
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    print('middleware success')
    return await call_next(request, response)

app.include_router(user_router, prefix='/user', tags=['users'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=PORT,)
