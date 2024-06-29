from abc import ABC, abstractmethod

from app.models.model_base import ModelBase


class ServiceBase(ABC):
    @staticmethod
    @abstractmethod
    def cadastrar(dados: dict):
        pass

    @staticmethod
    @abstractmethod
    def atualizar(modelo: ModelBase, dados: dict):
        pass

    @staticmethod
    @abstractmethod
    def remover(id: int):
        pass

    @staticmethod
    @abstractmethod
    def encontrar(id: int):
        pass

    @staticmethod
    @abstractmethod
    def listar(filtros: dict = None):
        pass

    @staticmethod
    def get_id(dados: [ModelBase]):
        ordenado = sorted(dados, key=lambda x: x.id)
        return ordenado[-1].id + 1 if ordenado else 1
