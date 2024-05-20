from abc import ABC, abstractmethod

from app.models.model_base import ModelBase


class ServiceBase(ABC):
    @abstractmethod
    def cadastrar(self, dados: dict):
        pass

    @abstractmethod
    def atualizar(self, modelo: ModelBase, dados: dict):
        pass

    @abstractmethod
    def remover(self, id: int):
        pass

    @abstractmethod
    def encontrar(self, id: int):
        pass

    @abstractmethod
    def listar(self, filtros: dict = None):
        pass

    @staticmethod
    def get_id(dados: [ModelBase]):
        ordenado = sorted(dados, key=lambda x: x.id)
        return ordenado[-1].id + 1 if ordenado else 1
