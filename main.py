import json
from enum import Enum

from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

from storage import storage

app = FastAPI(
    description='First site'
)


class TypeOfTour(str, Enum):
    SEA = 'sea'
    MOUNTAINS = 'mountains'
    DESERT = 'desert'


class NewTour(BaseModel):
    title: str = Field(min_length=3, examples=['JoinUp'])
    country: str
    price: float = Field(default=100, gt=0.0)
    cover: str
    tags: list[TypeOfTour] = Field(default=[], max_items=2)
    description: str


class SavedTour(NewTour):
    id: str = Field(examples=['40de287d36ab48d8a88572b8e98e7312'])


@app.get('/')
def index():
    return {'status': 200}


@app.post('/api/create', status_code=status.HTTP_201_CREATED)
def create_tour(tour: NewTour) -> SavedTour:
    created_tour = storage.create_tour(json.loads(tour.json()))
    return created_tour


@app.get('/api/get-tour/')
def get_tour(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, gt=0), search_param: str = '') -> list[
    SavedTour]:
    saved_tours = storage.get_tours(skip, limit, search_param)
    return saved_tours


@app.get('/api/get-tour/{tour_id}')
def get_tour(tour_id: str) -> SavedTour:
    saved_tour = storage.get_tour_info(tour_id)
    return saved_tour


@app.delete('/api/get-tour/{tour_id}')
def delete_tour(tour_id: str) -> dict:
    storage.delete_tour(tour_id)
    return {}


@app.patch('/api/get-tours/{tour_id}')
def delete_tour(tour_id: str, country: str) -> SavedTour:
    tour = storage.update_tour(tour_id, country=country)
    return tour
