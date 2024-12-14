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


@app.post('/api/tour/create', status_code=status.HTTP_201_CREATED)
def create_tour(tour: NewTour) -> SavedTour:
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
def get_tours(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, gt=0), search_param: str = '') -> list[
    SavedTour]:
    saved_tours = storage.get_tour(skip, limit, search_param)
    return saved_tours


@app.get('/api/tour/{tour_id}')
def get_tour(tour_id: str) -> SavedTour:
    saved_tour = storage.get_tour_info(tour_id)
    return saved_tour


@app.delete('/api/tour/{tour_id}')
def delete_tour(tour_id: str) -> dict:
    storage.delete_tour(tour_id=tour_id)
    return {"message": "Tour successfully deleted"}


@app.patch('/api/tours/{tour_id}')
def update_tour(tour_id: str, country: str, operator: str, price: float, duration: int, tags: list[str],
                description: str = None) -> SavedTour:
    tour = storage.update_tour(
        tour_id=tour_id,
        country=country,
        operator=operator,
        price=price,
        duration=duration,
        tags=tags,
        description=description)
    return tour
