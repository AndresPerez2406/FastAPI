from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "Mi aplicacion con FastAPI"

app.version = '1.1.1.1'

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

@app.post('/movies', tags=[movies])
def create_movie(id: int = Body(), tittle: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append(
        {
        'id': id,
        'tittle': tittle,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    }
    )
    return movies

@app.put('/movies', tags=['movies'])
def update_movie(id: int, title: str= Body(), overview: str= Body(), year: str= Body(), rating: float= Body(), category: str = Body()):

    movie = [(idx) for idx, mo in enumerate(movies) if mo['id'] == id]

    if(len(movie) > 0):
        movies[movie[-1]] = {
            "id": id,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "category": category
        }

        return movies

@app.delete('/movies', tags=[movies])
def delete_movie(id: int = Body()):
    for i in movies:
        if i['id'] == id:
            movies.remove(i)
            return movies
    return 'No se encuentra ese id'