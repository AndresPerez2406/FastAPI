from fastapi import  FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import engine, Base
from utils.jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = '1.1.1.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind= engine)


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World<h1>')
