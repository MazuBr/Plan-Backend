from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
import uvicorn


from src.config import PORT
from src.middleware.token import fetch_token
from src.routes.users import user_router
from src.routes.graphql import graphql_router
from src.graphql.scheme import schema

BASE_PATH = "/api"

app = FastAPI(root_path=BASE_PATH)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://plan-frontend.onrender.com", "https://local.matv.planirun"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def token_middleware(request: Request, call_next):
    paths = [
        "/user/create",
        "/user/login",
        "/docs",
        "/openapi.json",
        "/user/logout",
        "/user/refresh-token",
        "/graphiql",
    ]
    excluded_paths = [BASE_PATH + path for path in paths]

    if request.url.path in excluded_paths or request.method == "OPTIONS":
        return await call_next(request)

    token_errors = ("Invalid token", "Token expired")
    token: str = request.headers.get("Authorization")
    token_data: str
    if token:
        _, token = token.split(" ")
        token_data = await fetch_token(token)
        request.state.user_id = token_data.get("user_id")
        if token_data in token_errors:
            request.state.user_id = None
            return JSONResponse(status_code=401, content={"detail": token_data})
    elif not token:
        request.state.user_id = None
        return JSONResponse(status_code=401, content={"detail": "No token"})
    return await call_next(request)


graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
app.include_router(graphql_router, tags=["graphql"])
app.include_router(user_router, prefix="/user", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
    )
