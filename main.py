from typing import List, Optional
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()

app.title = "Mi aplicacion con FastAPI"

app.version = '1.1.1.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=404, detail='Credencial error')


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
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven los Navi, seres que',
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
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for i in movies:
        if i['id'] == id:
            return JSONResponse(statuscode=200,content=i)
    return ['No se encuentra su pelicula en la lista']

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie:
    data = [ i for i in movies if i ['category'] == category]
    return JSONResponse(statuscode=200,content=[data])

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@app.put('/movies', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    movie = [(idx) for idx, mo in enumerate(movies) if mo['id'] == id]

    if(len(movie) > 0):
        movies[movie[-1]] = {
            "id": id,
            "title": movie.title,
            "overview": movie.overview,
            "year": movie.year,
            "rating": movie.rating,
            "category": movie.category
        }
        return JSONResponse(status_code=200, content={"message":'Se modifico la pelicula'})

@app.delete('/movies', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int = Body()) -> dict:
    for i in movies:
        if i['id'] == id:
            movies.remove(i)
            return JSONResponse(status_code=200, content={"message":'Se elimino la pelicula'})
    return JSONResponse(status_code=404,content={"message":'No se encuentra ese id'})