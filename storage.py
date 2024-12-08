import json
from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4


class BaseStorage(ABC):

    @abstractmethod
    def create_tour(self, tour: dict, country: str, operator: str, price: float, duration: int):
        pass

    @abstractmethod
    def get_tour(self, skip: int = 0, limit: int = 5, search_param: str = ''):
        pass

    @abstractmethod
    def get_tour_info(self, tour_id: str):
        pass

    @abstractmethod
    def update_tour(self, tour_id: str, country: str, operator: str, price: float, duration: int):
        pass

    @abstractmethod
    def delete_tour(self, tour_id: str):
        pass


class JSONStorage(BaseStorage, ABC):
    def __init__(self):
        self.file_name = 'storage.json'

        my_file = Path(self.file_name)
        if not my_file.is_file():
            with open(self.file_name, mode='w', encoding='utf-8') as file:
                json.dump([], file, indent=4)

    def create_tour(self, tour: dict, country: str, operator: str, price: float, duration: int):
        with open(self.file_name, mode='r') as file:
            content: list[dict] = json.load(file)

        tour['id'] = uuid4().hex
        content.append(tour)
        with open(self.file_name, mode='w', encoding='utf-8') as file:
            json.dump(content, file, indent=4)

    def get_tour(self, skip: int = 0, limit: int = 10, search_param: str = ''):
        with open(self.file_name, mode='r') as file:
            content: list[dict] = json.load(file)

        if search_param:
            data = []
            for tour in content:
                if search_param in tour['country']:
                    data.append(tour)
            sliced = data[skip:][:limit]
            return sliced

        sliced = content[skip:][:limit]
        return sliced

    def get_tour_info(self, tour_id: str):
        with open(self.file_name, mode='r') as file:
            content: list[dict] = json.load(file)
        for tour in content:
            if tour_id == tour['id']:
                return tour
        return {}

    def update_tour(self, tour_id: str, country: str, operator: str, price: float, duration: int):
        with open(self.file_name, mode='r') as file:
            content: list[dict] = json.load(file)
        was_found = False
        for tour in content:
            if tour_id == tour['id']:
                tour['country'] = country
                was_found = True
                break
        if was_found:
            with open(self.file_name, mode='w', encoding='utf-8') as file:
                json.dump(content, file, indent=4)
        raise ValueError()

    def delete_tour(self, tour_id: str):
        with open(self.file_name, mode='r') as file:
            content: list[dict] = json.load(file)
        was_found = False
        for tour in content:
            if tour_id == tour['id']:
                content.remove(tour)
                was_found = True
                break
        if was_found:
            with open(self.file_name, mode='w', encoding='utf-8') as file:
                json.dump(content, file, indent=4)
        raise ValueError()


storage = JSONStorage()
