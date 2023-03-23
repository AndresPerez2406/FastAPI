from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def message():
    return"Hola Mundo"