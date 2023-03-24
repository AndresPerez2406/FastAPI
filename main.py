from typing import Optional
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Mi aplicacion con FastAPI"

app.version = '1.1.1.1'

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
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que",
        'year': 2009,
        'rating': 7.8,
        'category': 'Comedia'
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que",
        'year': 2010,
        'rating': 7.8,
        'category': 'Acción'
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World<h1>')

@app.get('/movies', tags=[movies])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=[movies])
def get_movie(id: int = Path(ge=1, le=2000)):
    for i in movies:
        if i['id'] == id:
            return i
    return ['No se encuentra su pelicula en la lista']

@app.get('/movies/', tags=[movies])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15) ):
    for i in movies:
        if i ['category'] == category:
            return i
    return ['Tu pelicula no coincide con ninguna en la lista']

@app.post('/movies', tags=[movies])
def create_movie(movie: Movie):
    movies.append(
        {
        'id': movie.id,
        'tittle': movie.tittle,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
    }
    )
    return movies

@app.put('/movies', tags=['movies'])
def update_movie(id: int, movie: Movie):

    movie = [(idx) for idx, mo in enumerate(movies) if mo['id'] == id]

    if(len(movie) > 0):
        movies[movie[-1]] = {
            "id": movie.id,
            "title": movie.title,
            "overview": movie.overview,
            "year": movie.year,
            "rating": movie.rating,
            "category": movie.category
        }

        return movies

@app.delete('/movies', tags=[movies])
def delete_movie(id: int = Body()):
    for i in movies:
        if i['id'] == id:
            movies.remove(i)
            return movies
    return 'No se encuentra ese id'