from typing import List, Optional
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_beater import JWTBearer

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = '1.1.1.1'

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind= engine)

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):

    id: Optional[int] = None
    tittle: str = Field(max_length=15)
    overview: str = Field(max_length=15)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(max_length=15)

    class Config:
        schema_extra = {
            'example': {

            'id': 1,
            'tittle': 'Mi pelicula',
            'overview': 'Mi descripcion',
            'year': 2000,
            'rating': 5.5,
            'category': 'Mi categoria'

            }
        }

movies = [
    {
        'id': 1,
        'title': 'Sherk',
        'overview': 'Verde',
        'year': 2009,
        'rating': 7.8,
        'category': 'Comedia'
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Navi, seres que",
        'year': 2010,
        'rating': 7.8,
        'category': 'Acción'
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World<h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code = 200, content=token)

@app.get('/movies', tags=['movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    result.tittle = movie.tittle
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se a modificado'})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message":'Se a eliminado correctamente'})