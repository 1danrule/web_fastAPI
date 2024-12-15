import json
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from storage import storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/token')

app = FastAPI(
    description='Tour Agency'
)


class TypeOfTour(str, Enum):
    SEA = 'sea'
    MOUNTAINS = 'mountains'
    DESERT = 'desert'


class NewTour(BaseModel):
    operator: str
    country: str
    price: float = Field(default=100, gt=0.0)
    duration: int
    tags: list[TypeOfTour] = Field(default=[], max_items=2)
    description: str = None


class SavedTour(NewTour):
    id: str = Field(examples=['40de287d36ab48d8a88572b8e98e7312'])


@app.get('/')
def index():
    return {'status': 200}


fake_db_users = [
    {
        'username': 'alex',
        'password': 'admin',
        'is_admin': True,
        'token': 'eb038beaac3f45de8831b9a584da1218',
    },
    {
        'username': 'alice',
        'password': 'secret',
        'is_admin': False,
        'token': 'eb038beafc3f45de8831b9a584da1210',
    },
]


class User(BaseModel):
    username: str
    is_admin: bool
    token: str
    password: str


@app.post('/api/token')
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user_dict = {}
    for user in fake_db_users:
        found_user = user['username'] == form_data.username
        if found_user:
            user_dict = user
            break
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect username or password')

    user = User(**user_dict)
    password = form_data.password
    if password != user.password:
        raise HTTPException(status_code=400, detail='Incorrect username or password')

    return {'access_token': user.token, 'token_type': 'bearer'}


def get_user_by_token(token: str, is_admin: bool = False) -> User:
    user = None
    for user_data in fake_db_users:
        if token == user_data['token']:
            if is_admin:
                if not user_data['is_admin']:
                    raise HTTPException(status_code=403, detail='You do not have enough permissions')
            user = User(**user_data)
            break
    if not user:
        raise HTTPException(status_code=403, detail='Invalid credentials')

    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    user = get_user_by_token(token)
    return user


def get_current_user_admin(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    user = get_user_by_token(token, is_admin=True)
    return user


@app.post('/api/tour/create', status_code=status.HTTP_201_CREATED)
def create_tour(tour: NewTour, admin_user: Annotated[User, Depends(get_current_user)]) -> SavedTour:
    created_tour = storage.create_tour(
        country=tour.country,
        operator=tour.operator,
        price=tour.price,
        duration=tour.duration,
        tags=tour.tags,
        description=tour.description

    )

    return created_tour


@app.get('/api/tour/')
def get_tours(any_user: Annotated[User, Depends(get_current_user)], skip: int = Query(default=0, ge=0),
              limit: int = Query(default=10, gt=0), search_param: str = '') -> list[
    SavedTour]:
    saved_tours = storage.get_tour(skip, limit, search_param)
    return saved_tours


@app.get('/api/tour/{tour_id}')
def get_tour(tour_id: str, any_user: Annotated[User, Depends(get_current_user)]) -> SavedTour:
    saved_tour = storage.get_tour_info(tour_id)
    return saved_tour


@app.delete('/api/tour/{tour_id}')
def delete_tour(tour_id: str, admin_user: Annotated[User, Depends(get_current_user_admin)]) -> dict:
    storage.delete_tour(tour_id=tour_id)
    return {"message": "Tour successfully deleted"}


@app.patch('/api/tours/{tour_id}')
def update_tour(tour_id: str, country: str, operator: str, price: float, duration: int, tags: list[str],
                admin_user: Annotated[User, Depends(get_current_user_admin)], description: str = None, ) -> SavedTour:
    tour = storage.update_tour(
        tour_id=tour_id,
        country=country,
        operator=operator,
        price=price,
        duration=duration,
        tags=tags,
        description=description)
    return tour

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run('main:app', reload=True, host='127.0.0.1', port=5000)
