from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "Mi aplicacion con FastAPI"

app.version = '1.1.1.1'

movies = [
    {
        'id': 4,
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
def get_movie(id: int):
    for i in movies:
        if i['id'] == id:
            return i
    return ['No se encuentra su pelicula en la lista']

@app.get('/movies/', tags=[movies])
def get_movies_by_category(category: str, year: int):
    for i in movies:
        if i ['category'] == category:
          if i ['year'] == year:
              return i
    return ['Tu pelicula no coincide con ninguna en la lista']