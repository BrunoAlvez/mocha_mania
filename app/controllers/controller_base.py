from abc import ABC

from app.models.model_base import ModelBase


class ControllerBase(ABC):
    @staticmethod
    def _repositorio(modelo: ModelBase) -> dict:
        return modelo.to_dict()

    @staticmethod
    def _sair():
        exit()
