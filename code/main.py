from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from logic.path_generator import cert_path, key_path
from middleware.token import fetch_token
from openapi.custom_locations import custom_openapi
from routes.users import user_router

app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def token_middleware(request: Request, call_next):
    excluded_paths = ["/user/create", "/user/login", '/docs', '/openapi.json']

    if request.url.path in excluded_paths or request.method == "OPTIONS":
        return await call_next(request)

    token = request.cookies.get("access-token")
    
    token_data = await fetch_token(token)
    if token_data == 'Token expired':
        return JSONResponse(status_code=401, content={'detail': 'Token expire'})
    if not token_data or token_data == 'Invalid token':
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    print('middleware success')
    return await call_next(request)

app.include_router(user_router, prefix='/user', tags=['users'])
app.openapi = lambda: custom_openapi(app)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, ssl_keyfile=key_path, ssl_certfile=cert_path)
