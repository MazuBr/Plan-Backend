from fastapi import FastAPI
import uvicorn

from routes.users import user_router


app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['users'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
