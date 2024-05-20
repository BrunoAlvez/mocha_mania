from abc import ABC, abstractmethod

from app.models.model_base import ModelBase


class Seeder(ABC):
    @staticmethod
    @abstractmethod
    def run() -> [ModelBase]:
        pass
