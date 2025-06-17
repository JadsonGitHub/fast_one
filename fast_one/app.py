from http import HTTPStatus

from fastapi import FastAPI

from fast_one.routers import auth, todos, users
from fast_one.schemas import Message

app = FastAPI(
    title='FastAPI do Zero to Hero',
    description='Aprendendo FastAPI do Zero',
    version='0.0.0',
    openapi_tags=[{'name': 'users', 'description': 'Operações com usuários'}],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Hello, World! 🤣'}
